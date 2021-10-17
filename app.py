from flask import Flask, render_template, request
from summarizer import summarize

app = Flask(__name__)

@app.route('/')
def index():
   return render_template('upload.html') 
@app.route('/uploader', methods = ['GET', 'POST'])

def uploads_file():
    if request.method == 'POST':
        # f = request.files['file']
        # filepath=secure_filename(f.filename)
        # f.save(filepath)
        # with open(filepath,'r') as w:
        #     text=w.read()
        #text=request.form['file123']
        text=request.form.get('file123')
        test=summarize(text)
        x=test['summary']
        str = ""
        for i in x: 
            str += i
        return render_template('summary.html',result=str)

if __name__ == '__main__':
    app.run(debug=True)