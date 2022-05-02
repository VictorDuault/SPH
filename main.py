from flask import Flask, render_template, request

#Format de la liste exo:
# [[nom, image(boolean), image(path en string), texte, points], ...]

app = Flask(__name__)
@app.route('/')
def home():
    return render_template('index.html')
@app.route('/c/projectionvectorielle')
def projvect():
    return render_template('cours/projectionvectorielle.html')
@app.route('/ex/newton') 
def exercices():
    n = request.args.get('n', type=int)
    print(n)
    return render_template('exercices/newton.html', 
                           exo =  [["Nom", False, "", "Lorem Ipsum", ""],
                                ["Nom2", False, "", "Lorem Ipsum2", ""],
                                ["Nom3", False, "", "Lorem Ipsum3", ""]], 
                           n=n, path="/ex/newton")

if __name__ == '__main__':
    app.run()