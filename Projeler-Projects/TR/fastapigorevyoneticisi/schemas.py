from pydantic import BaseModel
from typing import Optional

# Kullanıcıdan yeni görev oluştururken isteyeceğimiz veriler
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None

# Kullanıcıya veriyi geri gösterirken (Response) ID'yi de içeren model
class TaskResponse(TaskCreate):
    id: int
    completed: bool

    class Config:
        from_attributes = True
        
class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
