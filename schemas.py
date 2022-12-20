from pydantic import BaseModel

class phoneBookRequest(BaseModel):
    name: str
    phoneNumber: str
    class Config:
        orm_model = True

class deleteByNameRequest(BaseModel):
    name: str
    class Config:
        orm_mode = True

class deleteByNumberRequest(BaseModel):
    phoneNumber: str
    class Config:
        orm_mode = True