from pydantic import BaseModel, Field, model_validator

from typing_extensions import Self

from shemas.main_shemas import FactoryRank


class Worker(BaseModel):
    username: str | None #Думаю сделать так чтобы не обязательно указывать
    name: str = Field(max_length=50)
    surname: str = Field(max_length=50)
    password: str = Field(max_length=20, min_length=8)
    password_confirm: str
    grades: FactoryRank

    @model_validator(mode='after')
    def check_password(self) -> Self:
        if self.password != self.password_confirm:
            raise ValueError("Passwords do not match")
        return self


class WorkerAuth(Worker):
    username: str
    password: str