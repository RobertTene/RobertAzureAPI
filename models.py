from pydantic import BaseModel

class Order(BaseModel):
    vm_name: str
    resource_group: str
    location: str
    user_id: int
    recipient_id: int

class User(BaseModel):
    username: str
    first_name: str
    last_name: str