from fastapi import FastAPI
from src.processing import compute_loads_from_request
import uvicorn

app = FastAPI()

@app.post('/productionplant')
async def productionplant(payload: dict):
    return compute_loads_from_request(payload)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8888)