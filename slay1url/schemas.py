#slay1url/schemas.py

from pydantic import BaseModel

class URLBase(BaseModel):
    target_url:str

class URL(URLBase):
    is_active: bool
    clicks : int
    class Config :
        orm_mode= True #lets u treat db rows as python objs

class URLInfo(URLBase): #uses data directly w/o storing in db
    url: str
    admin_url: str