from flask import Flask, render_template, request, send_file
from flask_restful import Resource, Api
import sys
import os
from translator import main4  # Import your translate function

app = Flask(__name__,static_url_path='/static')
api = Api(app)
port = 5101


if sys.argv.__len__() > 1:
    port = sys.argv[1]
print("Api running on port : {} ".format(port))
@app.route("/", methods=["GET", "POST"])

def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        # Handle no file uploaded case
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        # Handle no selected file case
        return redirect(request.url)

    if file:
        # Save the file
        file.save('uploaded_file.txt')

        # Call your translator script
        main4('uploaded_file.txt', 'output_file.txt')

        # Provide a download link for the generated file
        download_link = '/download/output_file.txt'
        with open('output_file.txt', 'r') as output_file:
            output_content = output_file.read()
        return render_template('index.html', download_link=download_link, output_content=output_content)

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(filename, as_attachment=True)

if __name__ == "__main__":
    app.config['TIMEOUT'] = 300  # Set timeout to 5 minutes (adjust as needed)
    app.run(host="0.0.0.0", port=5101)
