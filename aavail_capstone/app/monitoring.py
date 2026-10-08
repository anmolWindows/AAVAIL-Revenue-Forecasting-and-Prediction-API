from collections import defaultdict
import time

REQUESTS = 0
ERRORS = 0
LATENCIES = []

def record_request(seconds, error=False):
    global REQUESTS, ERRORS
    REQUESTS += 1
    LATENCIES.append(seconds)
    if error:
        ERRORS += 1

def metrics():
    avg = sum(LATENCIES) / len(LATENCIES) if LATENCIES else 0.0
    return {
        "requests": REQUESTS,
        "errors": ERRORS,
        "average_latency_seconds": round(avg, 6),
        "error_rate": round(ERRORS / REQUESTS, 4) if REQUESTS else 0.0,
    }
