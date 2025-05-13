import time
from datadog import initialize, api
from config import Config

options = {
    "api_key": Config.DATADOG_API_KEY,
    "api_host": "https://api.us5.datadoghq.com"
}

initialize(**options)

# Custom metric: simulate CPU spike
for i in range(20):
    api.Metric.send(
        metric='custom.lambda.invocations',
        points=[(time.time(), 10000 + i * 1000)],
        type='gauge',
        tags=["env:test"]
    )
    time.sleep(1)
