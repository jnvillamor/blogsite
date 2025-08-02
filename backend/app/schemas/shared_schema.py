from typing import Generic, TypeVar, List
from pydantic import BaseModel, computed_field

T = TypeVar('T')

class PaginatedResponse(BaseModel, Generic[T]):
  total: int
  limit: int
  offset: int
  items: List[T]
  
  @computed_field
  @property
  def max_page(self) -> int:
    return (self.total + self.limit - 1) // self.limit
  
  @computed_field
  @property
  def page(self) -> int:
    return (self.offset // self.limit) + 1 if self.limit > 0 else 1
  
  @computed_field
  @property
  def has_next(self) -> bool:
    return self.page < self.max_page
  
  @computed_field
  @property
  def has_prev(self) -> bool:
    return self.page > 1

  model_config = {
    "from_attributes": True,
  }