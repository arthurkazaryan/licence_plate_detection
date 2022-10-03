from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.router import detection_v1
import uvicorn

app = FastAPI(openapi_url='/api/v1/detection/openapi.json', docs_url='/api/v1/detection/docs')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

app.include_router(detection_v1, prefix='/api/v1/detection')

if __name__ == '__main__':
    uvicorn.run(app, host="localhost", port=7861)
