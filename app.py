from flask import Flask, render_template, redirect, url_for
from flask_restful import Api

app = Flask(__name__)
api = Api(app)

# Part 1
from part1.app import part1_app
app.register_blueprint(part1_app, subdomain='part1', url_prefix='/part1')

# Part 2
from part2.app import part2_app
app.register_blueprint(part2_app, subdomain='part2', url_prefix='/part2')

@app.route('/')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)
