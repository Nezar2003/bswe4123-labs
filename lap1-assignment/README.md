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

The `monitor.py` program checks all three services repeatedly.

- Monitoring interval: 2 seconds (sleep after each monitoring round).
- HTTP timeout: 1.5 seconds.
- SLOW threshold: 500 milliseconds.
- Maximum consecutive failures: 3.

The monitor uses HTTPX to send requests and measure response times.

## 5. Experiment 1: Normal Service Operation

When all services were running normally, the monitor reported:

- Service 1: UP
- Service 2: SLOW
- Service 3: UP

Service 2 was intentionally configured with a delay of 0.8 seconds.

Its measured response time was approximately 804–806 ms.

## 6. Experiment 2: Stopping a Service

Service 1 was stopped using Ctrl+C.

The monitor detected consecutive failures:

- First failure: SUSPECT (1/3)
- Second failure: SUSPECT (2/3)
- Third failure: DOWN

This confirms that the failure counter works correctly.

## 7. Experiment 3: Restarting the Service

After restarting Service 1 on port 8001, its health endpoint returned:

`{"status":"ok","uptime":34.97}`

The monitor subsequently reported Service 1 as UP again.

## 8. Experiment 4: Slow Service

Service 2 was configured with a delay of 0.8 seconds.

The monitor consistently reported SLOW because its response time exceeded the 500 ms threshold.

Services 1 and 3 remained UP during normal operation.

## 9. Failure Detection and Timeout

The monitor uses a timeout of 1.5 seconds and requires three consecutive failed checks before marking a service as DOWN.

This approach reduces false alarms caused by temporary network problems.

A shorter timeout detects failures faster but may produce false alarms. A longer timeout gives services more time to respond but delays failure detection.

The monitor checks services sequentially. Therefore, a timeout on one service can delay checks of the following services.

## 10. Conclusion

The assignment successfully demonstrates how to monitor multiple services, measure response times, detect slow services, identify unavailable services, and detect service recovery after restarting.
