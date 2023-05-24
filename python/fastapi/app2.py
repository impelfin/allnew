# pip install pydantic[email]

import uvicorn
from fastapi import FastAPI, status
from fastapi.responses import PlainTextResponse, JSONResponse
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from typing import Optional

app = FastAPI()

class RequestUserDto(BaseModel):
    nickname:str=Field(title="사용자 닉네임")
    email:EmailStr=Field(title="사용자 이메일 주소")
    phone:str=Field(title="사용자 휴대폰 번호", regex="^010-([0-9]{4})-([0-9]{4})$")
    description:Optional[str]=Field(title="자기소개")

class ResponseUserDto(BaseModel):
    nickname:str=Field(title="사용자 닉네임")
    email:EmailStr=Field(title="사용자 이메일 주소")
    phone:str=Field(title="사용자 휴대폰 번호", regex="^010-([0-9]{4})-([0-9]{4})$")
    description:Optional[str]=Field(title="자기소개")
    class Config:
        schema_extra={
            "example":{
                "nickname": "왓슨",
                "email": "watson@buzzni.com",
                "phone": "010-1234-5678",
                "description":"버즈니 왓슨입니다."    
            }        
        }

@app.get(
    path='/', description="healthcheck용 포인트입니다.",
    status_code=status.HTTP_200_OK,
    response_class=PlainTextResponse,
    responses={200:{"description" : "Health check 응답"}}
)
async def health_check():
    return "OK"

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3000)

@app.post (
    path='/registerReq', description="회원가입 API입니다.", status_code=201,
    response_class=JSONResponse,
    responses={
        201: {
            "description":"가입 사용자 정보",
            "content": {
                "application/json": {
                    "example": {
                        "nickname": "왓슨",
                        "email": "watson@buzzni.com",
                        "phone": "010-1234-5678",
                        "description":"버즈니 왓슨입니다."
                    }
                }
            }
        }
    }
)
async def register_req_user(req: RequestUserDto):
    return req.dict()

@app.post (
    path='/registerRes', description="회원가입 API입니다.", status_code=201,
    response_model = ResponseUserDto,
    responses = {
        201: {
            "description":"가입 사용자 정보",
        }
    }
)
async def register_res_user(req: ResponseUserDto):
    return req.dict()
    