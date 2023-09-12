from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from datetime import datetime

DB_NAME = "database.db"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   title = db.Column(db.String(1000))
   description = db.Column(db.String(5000))
   date_create = db.Column(db.String(15))
   date_deadline = db.Column(db.String(15))
   date_complete = db.Column(db.String(15))
   complete = db.Column(db.Boolean)
   

@app.route("/")
def todo():
  todo_list = Todo.query.all()
  table_size = len(todo_list)
  true_complete = count_true_rows()

  current_time = datetime.now()
  if true_complete == 0:
     progres = 0
  else:
    progres = round((true_complete/table_size)*100, 2)
  for todo in todo_list:
        if todo.date_deadline is None or todo.date_deadline == '':
            continue 
        todo.date_deadline = datetime.strptime(todo.date_deadline, '%Y-%m-%d')  
    

  return render_template("todo.html", todo_list=todo_list, 
                         table_size=table_size, 
                         true_complete=true_complete,
                         progres=progres,
                         current_time=current_time)


@app.route("/add", methods=["POST"])
def add():
  title = request.form.get('title')
  description = request.form.get('description')
  date_create = datetime.now()
  date_create = date_create.strftime("%Y-%m-%d")
  date_deadline = request.form.get('date')
  
  new_todo = Todo(title=title, 
                  description=description, 
                  date_deadline=date_deadline, 
                  date_create=date_create, 
                  complete=False)
  db.session.add(new_todo)
  db.session.commit()
  return redirect(url_for("todo"))


@app.route("/complete/<int:todo_id>")
def complete (todo_id):
  current_time = datetime.now()
  todo = Todo.query.filter_by(id=todo_id).first()
  todo.complete = not todo.complete
  todo.date_complete = current_time.strftime('%Y-%m-%d %H:%M')
  db.session.commit()
  return redirect(url_for("todo"))


@app.route("/delete/<int:todo_id>")
def delete(todo_id):
  todo = Todo.query.filter_by(id=todo_id).first()
  db.session.delete(todo)
  db.session.commit()
  return redirect(url_for("todo"))


@app.route("/edit/<int:todo_id>", methods = ['POST'])
def edit(todo_id):
  pass

def count_true_rows():
    count = db.session.query(func.count()).filter(Todo.complete == True).scalar()
    return count

if __name__ == "__main__":
 with app.app_context():
        db.create_all()
        app.run(debug=True, port=2137)