from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

class Stats(Resource):
    def get(self):
        return {"msg": "This is the Stats resource."}

class Recommend(Resource):
    def get(self, subreddit):
        return {"msg": "Here is a subreddit recommendation for %s." % subreddit}

api.add_resource(Stats, "/api/stats")
api.add_resource(Recommend, "/api/recommend/<string:subreddit>")

if __name__ == "__main__":
    app.run(debug=True)
