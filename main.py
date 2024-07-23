from fastapi import Depends, FastAPI, HTTPException ,status
from sqlalchemy.orm import Session

import models, schemas
from database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware


models.Base.metadata.create_all(bind=engine)




app = FastAPI()


app = FastAPI()

# origins = [
#     "http://localhost.tiangolo.com",
#     "https://localhost.tiangolo.com",
#     "http://localhost",
#     "http://localhost:8080",
# ]

origins = ["http://localhost:3000"] 

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/create_todo")
async def createTodo(todo: schemas.ToDos,  db: Session = Depends(get_db)):
    replace_todo = db.query(models.ToDos).filter(models.ToDos.title == todo.title).first()
    if replace_todo :
        raise  HTTPException(status_code=400 , detail="Todo with same title already exists")
    newTodo = models.ToDos(title=todo.title, description = todo.description)
    db.add(newTodo)
    db.commit()
    db.refresh(newTodo)
    return newTodo


@app.get('/getAllToDo')
def getAllTodos(db: Session = Depends(get_db)):
    allTodos = db.query(models.ToDos).all()
    return allTodos

@app.get('/getTodo/{id}')
def get_Todo_by_Id(id, db : Session = Depends(get_db)):
    singleTodo = db.query(models.ToDos).filter(models.ToDos.id==id).first()
    if not singleTodo:
        raise HTTPException(status_code =  status.HTTP_404_NOT_FOUND , details=f"Todo with given{id} is not exisit in the db")
    return singleTodo

@app.delete('/todo/delete/{id}')
def deleteTodo(id, db: Session = Depends(get_db)):
    todo_to_delete = db.query(models.ToDos).filter(models.ToDos.id == id).first()
    db.delete(todo_to_delete)
    db.commit()
    return { 'deleted': f"{todo_to_delete.title} todo deleted succesfully"}




