# app.py
import os
import time

from flask import Flask, Response
from prometheus_client import (
    CollectorRegistry, Gauge, generate_latest, CONTENT_TYPE_LATEST,
    ProcessCollector, PlatformCollector, GCCollector
)

app = Flask(__name__)

# ---- envs (same names you already use) ----
DESIRED_PATH = os.getenv("DESIRED_PATH", "/")   # e.g. "/work"
PORT         = int(os.getenv("PORT", "8080"))
NUMBER       = os.getenv("NUMBER", "0")

# ---- Prometheus metrics ----
REG = CollectorRegistry()
# default process/runtime metrics (includes process_resident_memory_bytes)
ProcessCollector(registry=REG)
PlatformCollector(registry=REG)
GCCollector(registry=REG)

pending = Gauge(
    "myapp_pending_requests",
    "In-flight HTTP requests being processed",
    labelnames=("service_number",),
    registry=REG,
)

mem_limit = Gauge(
    "myapp_memory_limit_bytes",
    "Container memory limit (bytes) read from cgroup",
    labelnames=("service_number",),
    registry=REG,
)

def read_mem_limit_bytes():
    paths = [
        "/sys/fs/cgroup/memory.max",                  # cgroup v2
        "/sys/fs/cgroup/memory/memory.limit_in_bytes" # cgroup v1
    ]
    for p in paths:
        try:
            raw = open(p, "r").read().strip()
            if raw == "max":
                return float("inf")
            return float(int(raw))
        except Exception:
            pass
    return float("nan")

mem_limit.labels(NUMBER).set(read_mem_limit_bytes())

@app.route("/metrics")
def metrics():
    data = generate_latest(REG)
    return Response(data, mimetype=CONTENT_TYPE_LATEST)

@app.route("/healthcheck")
def healthcheck():
    pending.labels(NUMBER).inc()
    try:
        time.sleep(2)
        return "It ...slowly... works!", 200
    finally:
        pending.labels(NUMBER).dec()

@app.route(DESIRED_PATH)
def greeting():
    pending.labels(NUMBER).inc()
    try:
        time.sleep(2)
        return f"<h1>Hello (slowly) from cool server {DESIRED_PATH} number {NUMBER}!</h1>"
    finally:
        pending.labels(NUMBER).dec()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
