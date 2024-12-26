from flask import Flask, render_template, request
from flask_restful import Api
import sys
import os


from translator import main3

part1_app = Flask(__name__, instance_relative_config=True)
api = Api(part1_app)
port = 5102

if __name__ == '__main__':
    if sys.argv.__len__() > 1:
        port = sys.argv[1]
    print("Api running on port : {} ".format(port))

@part1_app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        sentence = request.form["sentence"]
        print(sentence)
        reordered_sentence, isl_sentence, hindi_sentence = main3(sentence)
        return render_template("part1_template.html", sentence=sentence, reordered_sentence=reordered_sentence, isl_sentence=isl_sentence, hindi_sentence=hindi_sentence)
    return render_template("part1_template.html")
