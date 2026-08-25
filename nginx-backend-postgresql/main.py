from fastapi import FastAPI

app = FastAPI()

@app.get('/task')
async def root():
    return {"message": "Task completed"}