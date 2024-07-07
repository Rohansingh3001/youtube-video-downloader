from flask import Flask, request, render_template, redirect, url_for
import os
from pytube import YouTube

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        if not url:
            return render_template('index.html', error='Please provide a URL.')

        try:
            yt = YouTube(url)
            stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
            stream.download(output_path='downloads', filename=f'{yt.title}.mp4')
            return render_template('index.html', success=True, title=yt.title, filename=f'{yt.title}.mp4')
        except Exception as e:
            return render_template('index.html', error=str(e))
    return render_template('index.html')

@app.route('/downloads/<filename>')
def download_file(filename):
    return redirect(url_for('static', filename=f'downloads/{filename}'))

if __name__ == '__main__':
    app.run(debug=True)
