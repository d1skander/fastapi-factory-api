from pydantic import BaseModel, Field, model_validator

from typing_extensions import Self

from schemas.main_shemas import FactoryRank


class Worker(BaseModel):
    name: str = Field(max_length=50)
    surname: str = Field(max_length=50)
    password: str = Field(max_length=8, min_length=3)
    password_confirm: str = Field(exclude=True)
    grades: FactoryRank

    @model_validator(mode='after')
    def check_password(self) -> Self:
        if self.password != self.password_confirm:
            raise ValueError("Passwords do not match")
        return self


class WorkerAuth(Worker):
    id: str
    password: str