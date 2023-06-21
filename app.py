from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db = SQLAlchemy(app)

class Todo(db.Model):
    sn = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    time = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sn} - {self.title}"


@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method== 'POST':
        todo_title = request.form['title']
        desc_todo = request.form['desc']
        data = Todo(title=todo_title, desc=desc_todo)
        db.session.add(data)
        db.session.commit()
    alltodo = Todo.query.all()
    return render_template('index.html',alltodo=alltodo)

@app.route("/update/<int:sn>", methods=['GET', 'POST'])
def update(sn):
    if request.method == 'POST':
        todo_title = request.form['title']
        desc_todo = request.form['desc']
        data = Todo.query.filter_by(sn=sn).first()
        data.title = todo_title
        data.desc = desc_todo
        db.session.add(data)
        db.session.commit()
        return redirect("/")
    todo = Todo.query.filter_by(sn=sn).first()
    return render_template("update.html", todo=todo)

@app.route("/delete/<int:sn>")
def delete(sn):
    todo = Todo.query.filter_by(sn=sn).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug = True)
