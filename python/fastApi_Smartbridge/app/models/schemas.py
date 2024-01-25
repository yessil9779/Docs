from pydantic import BaseModel

class form_iin(BaseModel):
    IIN: str

class form_bin(BaseModel):
    BIN: str