from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)

with app.app_context():
    db.create_all()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        task_content = request.form["content"]

        new_task = Task(content=task_content)

        db.session.add(new_task)
        db.session.commit()

        return redirect("/")

    tasks = Task.query.all()
    return render_template("index.html", tasks=tasks)

@app.route("/delete/<int:id>")
def delete(id):
    task = Task.query.get_or_404(id)

    db.session.delete(task)
    db.session.commit()

    return redirect("/")

@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    task = Task.query.get_or_404(id)

    if request.method == "POST":
        task.content = request.form["content"]
        db.session.commit()
        return redirect("/")

    return render_template("edit.html", task=task)

if __name__ == "__main__":
    app.run(debug=True)