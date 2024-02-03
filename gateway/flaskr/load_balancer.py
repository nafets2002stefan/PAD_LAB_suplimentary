import requests
from pybreaker import CircuitBreaker, CircuitBreakerError

# load_balancer
BETS_SERVICE_URLS = ["http://bets:3010", "http://bets2:3011", "http://bets3:3012"]
VIDEO_SERVICE_URLS = ["http://video:4000", "http://video2:4001", "http://video3:4002"]

def round_robin(iterable):
    while True:
        for item in iterable:
            yield item

bets_url_generator = round_robin(BETS_SERVICE_URLS)
video_url_generator = round_robin(VIDEO_SERVICE_URLS)


#circuit breaker
CIRCUIT_BREAKER_FAILURE_THRESHOLD = 1  # Number of consecutive failures to trip the circuit breaker
CIRCUIT_BREAKER_RECOVERY_TIMEOUT = 30  # Recovery timeout in seconds    

def create_circuit_breaker():
    return CircuitBreaker(
        fail_max=CIRCUIT_BREAKER_FAILURE_THRESHOLD,
        reset_timeout=CIRCUIT_BREAKER_RECOVERY_TIMEOUT
    )

bets_circuit_breaker = create_circuit_breaker()
video_circuit_breaker = create_circuit_breaker()


# re-routing function if microservice fails
MAX_RETRIES = 3  # maximum number of retries before rerouting
@bets_circuit_breaker
def get_healthy_bets_url(url_generator, retries=0):
    try:
        url = next(url_generator)
        response = requests.get(f'{url}/status')
        response.raise_for_status()
        return url
    except requests.exceptions.RequestException as e:
        if retries < MAX_RETRIES:
            # Retry with the next available URL
            return get_healthy_bets_url(url_generator, retries=retries + 1)
        else:
            raise CircuitBreakerError(f"All retries failed. No healthy server found. Error: {str(e)}")

        

@video_circuit_breaker
def get_healthy_video_url(url_generator, retries=0):
    try:
        url = next(url_generator)
        response = requests.get(f'{url}/status')
        response.raise_for_status()
        return url
    except requests.exceptions.RequestException as e:
        if retries < MAX_RETRIES:
            # Retry with the next available URL
            return get_healthy_video_url(url_generator, retries=retries + 1)
        else:
            raise CircuitBreakerError(f"All retries failed. No healthy server found. Error: {str(e)}")
