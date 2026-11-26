# Lab 3: Exam Scheduler Service

## 1. Project Description

The Exam Scheduler Service is a REST API built with FastAPI. It communicates with the Room Booking Service using HTTPX to find suitable rooms and book them for university exams.

## 2. Technologies Used

- Python
- FastAPI
- Pydantic
- HTTPX
- Uvicorn

## 3. Services

### Room Booking Service

Runs on port 8001.

### Exam Scheduler Service

Runs on port 8000.

## 4. How to Run

### Run Room Booking Service

Open a terminal inside the `lab3-assignment` folder and run:

```powershell
$env:ROOMS_DELAY="0"
uvicorn room_booking_service:app --port 8001
```

### Run Exam Scheduler Service

Open another terminal in the same folder and run:

```powershell
$env:ROOMS_URL="http://localhost:8001"
$env:ROOMS_TIMEOUT="2"
$env:MAX_RETRIES="3"
uvicorn exam_scheduler_service:app --port 8000
```

## 5. API Endpoints

| Method | Endpoint | Description                  |
| ------ | -------- | ---------------------------- |
| GET    | /config  | View scheduler configuration |
| POST   | /exams   | Schedule an exam             |

## 6. Retry Mechanism

The Exam Scheduler Service retries requests when a timeout, connection error, or server error (5xx) occurs.

The maximum number of retries is configurable.

The retry delays use exponential backoff:

- First retry: 0.5 seconds
- Second retry: 1 second
- Third retry: 2 seconds

HTTP 404 and 409 responses are not retried.

## 7. Why PUT Is Safe to Retry

The scheduler uses PUT with a consistent booking ID for each exam and room. The Room Booking Service handles repeated requests with the same ID and same data idempotently. This prevents duplicate bookings when a request is retried.

## 8. Retry Testing Log

| Test | Scenario                     | Result                  |
| ---- | ---------------------------- | ----------------------- |
| 1    | Successful exam booking      | 201 Created             |
| 2    | No free suitable room        | 409 Conflict            |
| 3    | Room Booking Service timeout | 503 Service Unavailable |
| 4    | Room Booking Service stopped | 503 Service Unavailable |
| 5    | Services restored            | 201 Created             |

## 9. Delay and Timeout Experiments

| Experiment | Room Delay | Scheduler Timeout | Response Time | Status |
| ---------- | ---------: | ----------------: | ------------: | ------ |
| 1          |    0.5 sec |             2 sec |     6.011 sec | 201    |
| 2          |      1 sec |             2 sec |     6.784 sec | 201    |
| 3          |      3 sec |             1 sec |    13.150 sec | 503    |

### Explanation

In experiments 1 and 2, the requests succeeded because the timeout was greater than the Room Booking Service delay.

In experiment 3, the request failed because the service delay was greater than the configured timeout. The scheduler retried the request, which increased the total response time.

A longer timeout can allow slower requests to succeed, but it makes the client wait longer. A shorter timeout detects delays faster, but may cause requests to fail even when the service is still running.

The measured response times include request processing, retries, backoff delays, and local execution overhead.

## 10. Configuration

The scheduler uses these environment variables:

| Variable      | Default Value         | Description              |
| ------------- | --------------------- | ------------------------ |
| ROOMS_URL     | http://localhost:8001 | Room Booking Service URL |
| ROOMS_TIMEOUT | 2.0                   | Request timeout          |
| MAX_RETRIES   | 3                     | Maximum retry attempts   |

The Room Booking Service uses:

| Variable    | Default Value | Description               |
| ----------- | ------------- | ------------------------- |
| ROOMS_DELAY | 0             | Artificial response delay |
