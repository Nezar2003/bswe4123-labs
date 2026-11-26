\# Lab 3: Exam Scheduler Service



\## 1. Project Description



The Exam Scheduler Service is a REST API built with FastAPI.

It communicates with the Room Booking Service using HTTPX to find

suitable rooms and book them for university exams.



\## 2. Technologies Used



\- Python

\- FastAPI

\- Pydantic

\- HTTPX

\- Uvicorn



\## 3. Services



\### Room Booking Service

Runs on port 8001.



\### Exam Scheduler Service

Runs on port 8000.



\## 4. How to Run



\### Run Room Booking Service



```powershell

$env:ROOMS\_DELAY="0"

uvicorn room\_booking\_service:app --port 8001

