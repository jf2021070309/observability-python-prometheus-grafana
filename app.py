from prometheus_client import start_http_server, Summary, Counter, Gauge
import random
import time

REQUEST_TIME = Summary(
    'request_processing_seconds',
    'Tiempo de procesamiento de la solicitud'
)
REQUEST_COUNTER = Counter(
    'request_count',
    'Número de peticiones procesadas'
)
TEMPERATURE = Gauge(
    'room_temperature_celsius',
    'Temperatura de la habitación en Celsius'
)


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
