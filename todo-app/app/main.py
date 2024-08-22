from typing import  Annotated
from sqlmodel import Session, select
from fastapi import FastAPI, Depends, HTTPException

from fastapi.middleware.cors import CORSMiddleware

from app.models.models import Todo, TodoCreate, TodoUpdate
from app.database.db import get_session, lifespan
from app.middleware.middleware import HostCheckMiddleware
    


app = FastAPI(
    lifespan=lifespan,
    title="todo app API",
    version="0.0.1",
    servers=[
        {
            "url": "https://patients-thompson-father-ford.trycloudflare.com/",
            "description": "Development Server"
        }
    ]
)



# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, you can restrict to specific origins if needed
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.add_middleware(HostCheckMiddleware)

@app.get("/")
def read_root():
    return {"message": "todo app"}

@app.get("/todos/", response_model=list[Todo])
def read_todos(session: Annotated[Session, Depends(get_session)]):
        todos = session.exec(select(Todo)).all()
        return todos

@app.get("/todos/{product_id}", response_model=Todo)
def read_product(product_id: int, session: Annotated[Session, Depends(get_session)]):
    product = session.get(Todo, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="todo not found")
    return product

    
@app.post("/todos/", response_model=Todo)
def create_todo(todo_create: TodoCreate, session: Annotated[Session, Depends(get_session)]):
        todo = Todo.model_validate(todo_create)  # Convert TodoCreate to Todo
        session.add(todo)
        session.commit()
        session.refresh(todo)
        return todo

@app.put("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, updated_todo: TodoUpdate, session: Annotated[Session, Depends(get_session)]):
        # Fetch existing todo from DB
        existing_todo = session.get(Todo, todo_id)

        # If the todo does not exist - raise an HTTPException 
        if existing_todo is None:
            raise HTTPException(status_code=404, detail="todo not found")

        # Update the content
        existing_todo.content = updated_todo.content
        session.commit()
        session.refresh(existing_todo)
        return existing_todo


@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, session: Annotated[Session, Depends(get_session)]):
        #Fetch existing todo from DB
        existing_todo = session.get(Todo, todo_id)

        if existing_todo is None:
            raise HTTPException(status_code=404, detail="todo not found")

        # Delete the todo from DB
        session.delete(existing_todo)
        session.commit()
        return {"message": "Todo deleted"}



