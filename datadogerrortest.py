import time
from datadog import initialize, api

options = {
    "api_key": "635bd0d12cbaa98f3b1069b455aa6df3",
    "api_host": "https://api.us5.datadoghq.com"
}

initialize(**options)

# Custom metric: simulate CPU spike
for i in range(10):
    api.Metric.send(
        metric='custom.lambda.invocations',
        points=[(time.time(), 10000 + i * 1000)],
        type='gauge',
        tags=["env:test"]
    )
    time.sleep(1)
