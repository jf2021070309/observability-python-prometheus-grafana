# Python Observability Example with Prometheus, Grafana Cloud & GitHub Actions

This repository is a practical example of **modern observability** for Python applications, using **Prometheus** for monitoring, **Grafana Cloud** for visualization, and **GitHub Actions** for CI/CD automation.

# Created by: Jaime Elias Flores Quispe

---

## 🚀 What does this project do?

- Exposes **custom metrics** (requests, timings, temperature) at `/metrics` using `prometheus_client`.
- Allows **Prometheus** to scrape metrics and send them to **Grafana Cloud** for dashboards and alerts.
- Integrates **automation** with GitHub Actions: every push runs lint and checks that the `/metrics` endpoint works properly.

---

## 🛠️ Repository Structure

```
/your-repo
  |-- app.py                # Python code exposing metrics
  |-- prometheus.yml        # Prometheus configuration (scrape + remote_write)
  |-- requirements.txt      # Python dependencies
  |-- .github/workflows/
        |-- ci.yml         # GitHub Actions workflow for automation
```

---

## 🐍 app.py

```python
from prometheus_client import start_http_server, Summary, Counter, Gauge
import random
import time

REQUEST_TIME = Summary('request_processing_seconds', 'Tiempo de procesamiento de la solicitud')
REQUEST_COUNTER = Counter('request_count', 'Número de peticiones procesadas')
TEMPERATURE = Gauge('room_temperature_celsius', 'Temperatura de la habitación en Celsius')

@REQUEST_TIME.time()
def process_request():
    t = random.uniform(0.5, 2.0)
    time.sleep(t)
    TEMPERATURE.set(random.uniform(20.0, 30.0))
    REQUEST_COUNTER.inc()

if __name__ == '__main__':
    start_http_server(8000)
    print("Servidor de métricas corriendo en http://localhost:8000/metrics")
    while True:
        process_request()
```

---

## 📊 prometheus.yml

```yaml
global:
  scrape_interval: 5s

scrape_configs:
  - job_name: 'python_app'
    static_configs:
      - targets: ['localhost:8000']

remote_write:
  - url: "https://prometheus-prod-56-prod-us-east-2.grafana.net/api/prom/push"
    basic_auth:
      username: "YOUR_USERNAME"
      password: "YOUR_API_KEY"
```

> ⚠️ **Important:** Use your own Grafana Cloud credentials.

---

## 📦 requirements.txt

```
prometheus_client
```

---

## ⚙️ Automation with GitHub Actions

Every push or pull request automatically runs:

1. Linter (`flake8`) on `app.py`
2. Runs the app and checks the `/metrics` endpoint

File `.github/workflows/ci.yml`:

```yaml
name: CI - Python Metrics App

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Lint code
        run: |
          pip install flake8
          flake8 app.py

      - name: Run app and test /metrics endpoint
        run: |
          nohup python app.py &
          sleep 5
          curl http://localhost:8000/metrics
```

---

## 🚦 How to run the project locally?

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the application:
   ```bash
   python app.py
   ```
3. Go to [http://localhost:8000/metrics](http://localhost:8000/metrics) to see the metrics.

---

## 🔗 Integration with Prometheus & Grafana Cloud

1. **Prometheus** reads your app's metrics using the `prometheus.yml` file.
2. Metrics are automatically sent to **Grafana Cloud** for advanced visualization.
3. You can create dashboards and alerts in Grafana Cloud with your custom metrics.

---
