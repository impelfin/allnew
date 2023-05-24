import uvicorn
from fastapi import FastAPI, status
from fastapi.responses import PlainTextResponse

app = FastAPI ( )

@app.get(
    path='/',description="healthcheck용 포인트입니다.",
    status_code=status.HTTP_200_OK,
    response_class=PlainTextResponse,
    responses={200:{"description" : "Health check 응답"}}
)
async def health_check():
    return "OK"

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3000)
