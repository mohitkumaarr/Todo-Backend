from fastapi import FastAPI,Depends 
from sqlalchemy.orm import Session


from database import engine, Base, sessionLocal
from models import Todo
from schemas import TodoCreate, TodoUpdate
Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")

def home():
    return {"message ": "TOdo api is working"}

def get_db():
    db = sessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.post("/todos")
def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    new_todo = Todo(
        title = todo.title,
        description = todo.description
    )

    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo

@app.get("/todos")
def get_todos(db: Session = Depends(get_db)):
    todos = db.query(Todo).all()

    return todos

@app.get("/todos/{todo_id}")
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()

    return todo


@app.put("/todos/{todo_id}")
def update_todo(
    todo_id:int,
    todo_data: TodoUpdate,
    db: Session = Depends(get_db)

):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()

    if todo is None:
        return{ "message": "Todo not found"}

    todo.title = todo_data.title
    todo.description = todo_data.description
    todo.completed = todo_data.completed


    db.commit()
    db.refresh(todo)
    return todo