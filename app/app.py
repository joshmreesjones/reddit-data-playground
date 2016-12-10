from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello, Mitch! This is a test.'

if __name__ == '__main__':
    app.run(debug=True)
