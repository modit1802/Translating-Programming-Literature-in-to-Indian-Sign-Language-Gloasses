from flask import Flask, render_template, request
from flask_restful import Resource, Api
import sys
import os
import translator
reordered_sentence, isl_sentence, hindi_sentence="","",""
app = Flask(__name__)
api = Api(app)
port = 5100
if sys.argv.__len__() > 1:
    port = sys.argv[1]
print("Api running on port : {} ".format(port))

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        sentence = request.form["sentence"]
        print(sentence)
        reordered_sentence, isl_sentence, hindi_sentence = translator.main3(sentence)
        return render_template("index.html", sentence=sentence, reordered_sentence=reordered_sentence, isl_sentence=isl_sentence, hindi_sentence=hindi_sentence)
    return render_template("index.html")
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5100)
