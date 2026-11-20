# Lab Assignment 1: Service Health Monitor

## 1. Objective

The objective of this assignment is to build a simple health monitoring system that checks whether multiple services are UP, SLOW, or DOWN.

## 2. Environment Setup

- Operating System: Windows
- Programming Language: Python
- Framework: FastAPI
- HTTP Client: HTTPX
- Code Editor: Visual Studio Code

## 3. Service Configuration

Three service instances were started on different ports:

| Service   | Port | Endpoint |
| --------- | ---: | -------- |
| Service 1 | 8001 | /health  |
| Service 2 | 8002 | /health  |
| Service 3 | 8003 | /health  |

The `/health` endpoint returns the service status and uptime in seconds.

## 4. Monitoring Implementation

The `monitor.py` program checks all three services repeatedly using HTTPX.

The monitoring configuration is:

- Monitoring interval: 2 seconds (sleep after each monitoring round).
- HTTP timeout: 1.5 seconds.
- SLOW threshold: 500 milliseconds.
- Maximum consecutive failures: 3.

The program measures the response time of each service and determines its health status.

## 5. Experiment 1: Normal Service Operation

When all three services were running, the monitor produced the following results:

```text
Service 1: UP | Response Time: 3.11 ms
Service 2: SLOW | Response Time: 803.85 ms
Service 3: UP | Response Time: 5.99 ms
```

Service 2 was intentionally configured with a delay of 0.8 seconds. Therefore, its response time exceeded the 500 ms threshold and it was classified as SLOW.

## 6. Experiment 2: Stopping a Service

Service 1 was stopped using Ctrl+C while the monitoring program was running.

The monitor detected consecutive failures:

```text
Service 1: SUSPECT (1/3) | No response
Service 1: SUSPECT (2/3) | No response
Service 1: DOWN | No response
```

The service was classified as DOWN after three consecutive failed checks.

This mechanism helps avoid declaring a service unavailable because of one temporary failure.

## 7. Experiment 3: Restarting the Service

After restarting Service 1 on port 8001, its health endpoint returned:

```json
{
  "status": "ok",
  "uptime": 34.97
}
```

The monitor subsequently detected the service again:

```text
Service 1: UP | Response Time: 3.11 ms
```

This confirms that the monitoring system can detect service recovery after restarting it.

## 8. Experiment 4: Slow Service

Service 2 was configured with a delay of 0.8 seconds using the `/health?delay=0.8` endpoint.

The monitor consistently reported SLOW because its response time was greater than 500 milliseconds.

Services 1 and 3 were UP during normal operation.

## 9. Failure Detection and Timeout

The monitor uses an HTTP timeout of 1.5 seconds and requires three consecutive failed checks before marking a service as DOWN.

The failure counter increases whenever a request fails. If the service responds successfully, the counter resets to zero.

This approach reduces false alarms caused by temporary network problems.

A shorter timeout detects failures faster but may incorrectly classify a slow service as unavailable. A longer timeout gives services more time to respond but delays failure detection.

The monitor checks services sequentially. Therefore, a timeout on one service can delay checks of the following services.

## 10. Conclusion

This assignment demonstrates how to monitor multiple service instances using Python, FastAPI, and HTTPX.

The monitoring system can measure response times, identify slow services, detect unavailable services after consecutive failures, and recognize when a stopped service becomes available again.
