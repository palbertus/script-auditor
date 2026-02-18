# Gunicorn configuration for script-auditor
# SSE requires long-lived connections → use sync workers with long timeout

bind = "127.0.0.1:8080"
workers = 2          # each worker handles one audit at a time (Playwright is heavy)
threads = 4          # threads per worker for concurrent SSE streams
timeout = 180        # seconds — must exceed max audit timeout (120s) + buffer
keepalive = 5
worker_class = "sync"

# Logging
accesslog = "/var/log/script-auditor/access.log"
errorlog  = "/var/log/script-auditor/error.log"
loglevel  = "info"
