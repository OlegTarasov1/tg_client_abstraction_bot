from pydantic import BaseModel



class UserTemplate(BaseModel):
    
    id: int
    name: str | None = ""
    username: str | None = ""
    is_sent_to: bool | None = False

