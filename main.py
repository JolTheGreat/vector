from flask import Flask, request
from gensim.models import word2vec
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/')
@cross_origin()
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route("/gensim", methods=["post"])
@cross_origin()
def gensim():
    print(request.origin)
    if request.origin == "https://vectormaths.netlify.app":
        model = word2vec.Word2Vec.load("result.model")

        if request.args.get("positive") is not None and request.args.get("negative") is not None:
            flag = True
            p = request.args.get("positive")
            n = request.args.get("negative")

            positive = p.split(",")
            negative = n.split(",")

            if p.lower() != "_none_":
                for i in positive:
                    if not model.wv.has_index_for(i):
                        print(i + " was not in positive")
                        flag = False

            print(request.args.get("negative").lower())
            if n.lower() != "_none_":
                for i in negative:
                    if not model.wv.has_index_for(i):
                        print(i + " was not in negative")
                        flag = False

            if flag:

                similar = model.wv.most_similar(positive=positive if p != "_none_" else [],
                                                negative=negative if n != "_none_" else [])
                entries = []
                for value in similar:
                    entries.append(value[0])
                return {"entries": entries}

            else:
                return "NotFound"
        else:
            return "Error: Please check query parameters"
    else:
        return "Error"


if __name__ == '__main__':
    app.run()
