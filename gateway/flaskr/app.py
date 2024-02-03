from flask import Flask, jsonify, request, redirect
from flask_caching import Cache
from circuitbreaker import circuit
from prometheus_flask_exporter import PrometheusMetrics
import requests
from load_balancer import get_healthy_bets_url, get_healthy_video_url, bets_url_generator, video_url_generator

app = Flask(__name__)
# initializing Flask Cache
cache = Cache(app, config={'CACHE_TYPE': 'redis', 'CACHE_REDIS_URL': 'redis://redis-master:6379/0'})
#cache = Cache(app, config={'CACHE_TYPE': 'simple'})

metrics = PrometheusMetrics(app)
# static information as metric
metrics.info('app_info', 'Application info', version='1.0.3')

by_path_counter = metrics.counter(
    'by_path_counter', 'Request count by request paths',
    labels={'path': lambda: request.path}
)

# BETS_SERVICE_URL = "http://localhost:3000" 
# VIDEO_SERVICE_URL = "http://localhost:4000" 
# Configuration for microservice endpoints
# BETS_SERVICE_URL = "http://bets" 
# VIDEO_SERVICE_URL = "http://videos:4000" 

# load balancer implementation
BETS_SERVICE_URLS = ["http://bets:3010", "http://bets2:3011", "http://bets3:3012"]
VIDEO_SERVICE_URLS = ["http://video:4000", "http://video2:4001", "http://video3:4002"]


#health check endpoint 
@app.route('/health', methods=['GET'])
def get_health():
    return jsonify({"status": "ok"})


# routes for the bets service
@app.route('/sports/status', methods=['GET'])
def get_status_sports():
    try:
        bets_url = next(bets_url_generator)
        #response = requests.get('http://localhost:3010/status')
        response = requests.get(f'{bets_url}/status')
        return jsonify(response.json())
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@app.route('/sports', methods=['POST'])
# @circuit(failure_threshold=5, recovery_timeout=30)
def log_view_sport():
    sport_data = request.get_json()
    bets_url = next(bets_url_generator)
    response = requests.post(f"{bets_url}/sports", json=sport_data)
    return response.json(), response.status_code

@by_path_counter
@app.route('/sports', methods=['GET'])
@cache.cached(timeout = 60)
def get_all_sports():
    bets_url = get_healthy_bets_url(bets_url_generator)
    response = requests.get(f"{bets_url}/sports")
    return response.json(), response.status_code

@by_path_counter
@app.route('/sports/<registrationId>', methods=['GET'])
@cache.cached(timeout = 60)
# @circuit(failure_threshold=5, recovery_timeout=30)
def get_sports(registrationId):
    bets_url = next(bets_url_generator)
    response = requests.get(f"{bets_url}/sports/{registrationId}")
    return response.json(), response.status_code



@by_path_counter
@app.route('/sports/<registrationId>', methods=['DELETE'])
#@cache.clear()
# @circuit(failure_threshold=5, recovery_timeout=30)
def delete_sports(registrationId):
    bets_url = next(bets_url_generator)
    response = requests.delete(f"{bets_url}/sports/{registrationId}")
    return response.json(), response.status_code




@app.route('/videos/status', methods=['GET'])
def get_status_bets():
    try:
        video_url = next(video_url_generator)
        response = requests.get(f'{video_url}/status')
        return jsonify(response.json())
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@app.route('/videos', methods=['POST'])
# @circuit(failure_threshold=5, recovery_timeout=30)
def log_view_video():
    video_data = request.get_json()
    video_url = next(video_url_generator)
    response = requests.post(f"{video_url}/videos", json=video_data)
    return response.json(), response.status_code

@by_path_counter
@app.route('/videos', methods=['GET'])
@cache.cached(timeout = 60)
def get_all_videos():
    video_url = get_healthy_video_url(video_url_generator)
    response = requests.get(f"{video_url}/videos")
    return response.json(), response.status_code

@by_path_counter
@app.route('/videos/<videoId>', methods=['GET'])
@cache.cached(timeout = 60)
# @circuit(failure_threshold=5, recovery_timeout=30)
def get_videos(videoId):
    video_url = next(video_url_generator)
    response = requests.get(f"{video_url}/videos/{videoId}")
    return response.json(), response.status_code



@by_path_counter
@app.route('/videos/<videoId>', methods=['DELETE'])
#@cache.clear()
# @circuit(failure_threshold=5, recovery_timeout=30)
def delete_videos(videoId):
    video_url = next(video_url_generator)
    response = requests.delete(f"{video_url}/videos/{videoId}")
    return response.json(), response.status_code


if __name__ == '__main__':
    app.run(debug=False, port=5050, host="0.0.0.0")