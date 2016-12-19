import dataset
import os

from config import config
from flask import Flask, jsonify, render_template

app = Flask(__name__)
config_name = os.getenv('FLASK_CONFIG') or 'default'
app.config.from_object(config[config_name])

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/similar/<string:subreddit>')
def test(subreddit):
    data = dataset.similar_subreddits(subreddit)
    return jsonify(data)

if __name__ == '__main__':
    app.run()
