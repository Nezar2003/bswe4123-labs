
import time
import httpx

services = {
    "Service 1": "http://localhost:8001/health",
"Service 2": "http://localhost:8002/health?delay=0.8", 
   "Service 3": "http://localhost:8003/health",
}

failures = {
    name: 0 for name in services
}

MAX_FAILURES = 3
duration = 60
monitor_start = time.perf_counter()
with httpx.Client(timeout=1.5) as client:

    # Warm-up
    for url in services.values():
        try:
            client.get(url)
        except httpx.RequestError:
            pass

    # while True:
    #     print("\n--- Health Monitor ---")
    while time.perf_counter() - monitor_start < duration:

        for name, url in services.items():

            try:
                start = time.perf_counter()
                response = client.get(url)
                end = time.perf_counter()

                response_time = (end - start) * 1000

                if response.status_code == 200:
                    failures[name] = 0

                    if response_time > 500:
                        status = "SLOW"
                    else:
                        status = "UP"

                else:
                    failures[name] += 1

                    if failures[name] >= MAX_FAILURES:
                        status = "DOWN"
                    else:
                        status = f"SUSPECT ({failures[name]}/3)"

                print(
                    f"{name}: {status} | "
                    f"Response Time: {response_time:.2f} ms"
                )

            except httpx.RequestError:
                failures[name] += 1

                if failures[name] >= MAX_FAILURES:
                    status = "DOWN"
                else:
                    status = f"SUSPECT ({failures[name]}/3)"

                print(f"{name}: {status} | No response")

        time.sleep(2)
