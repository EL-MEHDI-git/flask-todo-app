from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# /// = relative path, //// = absolute path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)

class SubTask(db.Model):
    __tablename__ = 'subtask'
    id = db.Column(db.Integer, primary_key=True)
    id_task = db.Column(db.Integer, db.ForeignKey('todo.id'))
    sub_title = db.Column(db.String(100))
    sub_complete = db.Column(db.Boolean)


@app.route("/")
def home():
    tasks = {}
    todo_list = Todo.query.all()
    # print(type(todo_list[0]))
    for todo in todo_list:
        sub_task = SubTask.query.filter_by(id_task=todo.id).all()
        
        if len(sub_task) > 0 :
            # for sub in sub_task:
            tasks[todo] = sub_task
        else :
            tasks[todo] = []

    tasks_keys = list(tasks.keys())
    return render_template("base.html", tasks = tasks, tasks_keys = tasks_keys)


@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")
    new_todo = Todo(title=title, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/add_sub/<int:todo_id>", methods=["POST"])
def add_sub(todo_id):
    title = request.form.get("title")
    print(title)
    # todo = Todo.query.filter_by(id=todo_id).first()
    sub_todo = SubTask(sub_title=title, sub_complete=False, id_task=todo_id)
    db.session.add(sub_todo)
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/update/<int:todo_id>")
def update(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    sub_tasks = SubTask.query.filter_by(id_task=todo_id).all()
    # Deleting sub-tasks
    for sub_task in sub_tasks:
        db.session.delete(sub_task)
        
    # Deleting the main todo item    
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("home"))

# @app.route("/patch/<int:todo_id>", methods=["POST"])
# def patch(todo_id):
#     title = request.form.get("Name")
#     print(title)
#     todo = Todo.query.filter_by(id=todo_id).first()
#     todo.title = title
#     db.session.commit()
#     return redirect(url_for("home"))

if __name__ == "__main__":
    #db.create_all()
    app.run(debug=True)
