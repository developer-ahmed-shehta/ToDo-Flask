from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)


@app.route("/")
def home():
    todo_list = Todo.query.all()
    return render_template("base.html", todo_list=todo_list)


@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")
    if title and title.strip():  # Only add if title is not empty
        new_todo = Todo(title=title.strip(), complete=False)
        db.session.add(new_todo)
        db.session.commit()
    return redirect(url_for("home"))


@app.route("/update/<int:todo_id>")
def update_status(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    if todo:
        todo.complete = not todo.complete
        db.session.commit()
    return redirect(url_for("home"))


@app.route("/edit/<int:todo_id>", methods=["POST"])
def edit(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    if todo:
        new_title = request.form.get("title")
        if new_title and new_title.strip():  # Only update if new title is not empty
            todo.title = new_title.strip()
            db.session.commit()
            return jsonify({'success': True})
    return jsonify({'success': False})


@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    if todo:
        db.session.delete(todo)
        db.session.commit()
    return redirect(url_for("home"))


with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
