from flask import Flask, request
from gensim.models import word2vec

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route("/gensim")
def gensim():
    model = word2vec.Word2Vec.load("result.model")

    if request.args.get("positive") is not None and request.args.get("negative") is not None:
        flag = True
        positive = request.args.get("positive").split(",")
        negative = request.args.get("negative").split(",")

        for i in positive:
            if not model.wv.has_index_for(i):
                print(i + " was not in positive")
                flag = False

        for i in negative:
            if not model.wv.has_index_for(i):
                print(i + " was not in negative")
                flag = False

        if flag:
            return str(
                model.wv.most_similar(positive=positive, negative=negative))

        else:
            return "NotFound"
    else:
        return "Error: Please check query parameters"


if __name__ == '__main__':
    app.run()
