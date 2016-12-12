from flask import Flask, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/similar/<string:subreddit>')
def test(subreddit):
    # TODO: cache this query somewhere so it's faster in the future
    return jsonify({"foo": subreddit})

if __name__ == '__main__':
    app.run(debug=True)
