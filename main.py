from flask import Flask, render_template

app = Flask(__name__)
  
@app.route('/')
def home():
    return render_template('index.html')
@app.route('/projectionvectorielle')
def projvect():
    return render_template('cours/projectionvectorielle.html')
@app.route('/exercices') 
def exercices():
    return render_template('exercices/newton.html')

if __name__ == '__main__':
    app.run()