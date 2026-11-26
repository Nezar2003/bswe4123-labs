import os
import httpx
from datetime import date
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, model_validator
import time
app = FastAPI(title="Exam Scheduler Service")

ROOMS_URL = os.getenv("ROOMS_URL", "http://localhost:8001")
TIMEOUT = float(os.getenv("ROOMS_TIMEOUT", "2.0"))
MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))
class ExamRequest(BaseModel):
    exam_id: str
    course_code: str
    day: date
    start_hour: int = Field(ge=8, le=20)
    end_hour: int = Field(ge=8, le=20)
    students: int = Field(gt=0)

    @model_validator(mode="after")
    def check_hours(self):
        if self.end_hour <= self.start_hour:
            raise ValueError("End hour must be after start hour")
        return self
def request_with_retry(method, url, **kwargs):
    for attempt in range(MAX_RETRIES + 1):
        try:
            response = httpx.request(
                method,
                url,
                timeout=TIMEOUT,
                **kwargs
            )

            if response.status_code in (404, 409):
                return response

            if 500 <= response.status_code < 600:
                if attempt < MAX_RETRIES:
                    time.sleep(0.5 * (2 ** attempt))
                    continue

                raise HTTPException(
                    status_code=503,
                    detail="Room Booking Service is unavailable"
                )

            return response

        except (httpx.TimeoutException, httpx.ConnectError):
            if attempt < MAX_RETRIES:
                time.sleep(0.5 * (2 ** attempt))
            else:
                raise HTTPException(    status_code=503,
                                    detail="Room Booking Service is unavailable"
                                    )
                
@app.get("/config")
def get_config():
    return {
        "rooms_url": ROOMS_URL,
        "timeout": TIMEOUT,
        "max_retries": MAX_RETRIES
    }
def get_rooms():
    response = request_with_retry(
        "GET",
        f"{ROOMS_URL}/rooms"
    )

    if response.status_code != 200:
        raise HTTPException(
            status_code=503,
            detail="Could not retrieve rooms"
        )

    return response.json()     
def find_suitable_rooms(students):
    rooms = get_rooms()

    suitable_rooms = [
        room for room in rooms
        if room["capacity"] >= students
    ]

    return suitable_rooms      
@app.post("/exams", status_code=201)
def schedule_exam(exam: ExamRequest):
    suitable_rooms = find_suitable_rooms(exam.students)

    if not suitable_rooms:
        raise HTTPException(
            status_code=409,
            detail="No suitable room available"
        ) 
    for room in suitable_rooms:
        booking_data = {
            "room_id": room["id"],
            "date": exam.day.isoformat(),
            "start_hour": exam.start_hour,
            "end_hour": exam.end_hour,
            "purpose": exam.course_code
        }

        response = request_with_retry(
            "PUT",
            f"{ROOMS_URL}/bookings/{exam.exam_id}-{room['id']}",
            json=booking_data
        )

        if response.status_code in (200, 201):
            return {
                "message": "Exam scheduled successfully",
                "exam_id": exam.exam_id,
                "room": room,
                "booking": response.json()
            }

        if response.status_code == 409:
            continue

        if response.status_code == 404:
            continue

    raise HTTPException(
        status_code=409,
        detail="No free suitable room available"
    )    