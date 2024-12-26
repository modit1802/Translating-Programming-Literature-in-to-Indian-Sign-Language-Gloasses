from flask import Flask, render_template, request, send_file, redirect, url_for
from flask_restful import Api
import sys
from translator import main4

part2_app = Flask(__name__, subdomain='part2', static_url_path='/static')
api = Api(part2_app)
port = 5101

if __name__ == '__main__':
    if sys.argv.__len__() > 1:
        port = sys.argv[1]
    print("Api running on port : {} ".format(port))

@part2_app.route("/", methods=["GET", "POST"])
def index():
    return render_template('part2_template.html')

@part2_app.route('/upload', methods=['POST'])
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
        download_link = url_for('download_file', filename='output_file.txt')
        return render_template('part2_template.html', download_link=download_link)

@part2_app.route('/download/<filename>')
def download_file(filename):
    return send_file(filename, as_attachment=True)
