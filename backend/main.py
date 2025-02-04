from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from utils import process_repo, answer_question
import os

app = FastAPI()

class RepoURL(BaseModel):
    url: str

class Question(BaseModel):
    question: str

# In-memory storage for vector DB
vector_db = None

@app.post("/process_repo")
async def process_repo_endpoint(repo: RepoURL):
    global vector_db
    try:
        vector_db = process_repo(repo.url)
        return {"message": "Repository processed successfully!"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/chat")
async def chat_endpoint(question: Question):
    global vector_db
    if not vector_db:
        raise HTTPException(status_code=400, detail="No repository processed yet.")
    try:
        answer = answer_question(vector_db, question.question)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)