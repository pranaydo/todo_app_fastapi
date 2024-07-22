

from pydantic import BaseModel

class ToDos(BaseModel):
    title : str
    description : str
    is_active : bool
