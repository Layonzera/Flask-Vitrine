from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db = SQLAlchemy(app)

class Vitrini(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100))
    price = db.Column(db.String(7))

@app.route('/')
def index():
    vitrini = Vitrini.query.all()
    return render_template('index.html', vitrini = vitrini)

@app.route('/create', methods=['POST'])
def create():
    title = request.form.get('title')
    price = request.form.get('price')
    newVitrini = Vitrini(title=title, price=price)
    db.session.add(newVitrini)
    db.session.commit()
    return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):
    vitrini = Vitrini.query.filter_by(id=id).first()
    db.session.delete(vitrini)
    db.session.commit()
    return redirect('/')

@app.route("/update/<int:id>", methods=['POST'])
def update(id):
    title = request.form.get('title')
    price = request.form.get('price')
    vitrini = Vitrini.query.filter_by(id=id).first()
    vitrini.title = title
    vitrini.price = price
    db.session.commit()
    return redirect("/")

if __name__ == '__main__':
    db.create_all()
    app.run(host='0.0.0.0')