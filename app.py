from flask import Flask, jsonify
import threading
import os
import movies 

app = Flask(__name__)

@app.route('/')
def home():
    return "Movie Tracker is Live!", 200

@app.route('/run-movies')
def trigger_movies():
    # Background-la process start aagum
    thread = threading.Thread(target=movies.run_all)
    thread.start()
    
    # Very small JSON response to avoid 'Output too large' error
    return jsonify({"status": "triggered"}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
