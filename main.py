#python
from typing import Optional
from fastapi.param_functions import Path
from enum import Enum

#pydantic
from pydantic import BaseModel
from pydantic import Field
from pydantic import EmailStr

#FastAPI
from fastapi import FastAPI, responses
from fastapi import Body, Query, Path

app = FastAPI()

#Models

class HairColor(Enum):
    white = "white"
    black = "black"

class Person(BaseModel):
    first_name: str =  Field(
                        ...,
                        min_length=1,
                        max_length=50,
                        example="Andres"
                    )
    last_name: str = Field(
                        ...,
                        min_length=1,
                        max_length=50,
                        example="Maya"
                    )
    age: int = Field(
                ge=18,
                le=100,
                example=24
                )
    hair_color: Optional[HairColor] = Field(default=None,example="black")
    is_married: Optional[bool] = Field(default=None,example=False)
    email:EmailStr = Field(...,example="andresmaya737@gmail.com")

class Location(BaseModel):
    city:str = Field()
    country:str = Field(...
                )



@app.get("/") #path operation decorator
def home(): #path operation function
    return {"Hello":"world"}


#Request and response body
@app.post("/person")
def create_person(person: Person = Body(...)):
    return person


#Validaciones query parameters
@app.get("/person")
def show_person(
        name: Optional[str] = Query(
                                None,
                                min_length=1,
                                max_length=50,
                                title="Nombre",
                                description="Indica el nombre del usuario",
                                example="Andres"
                            ),
        age:Optional[int] = Query(
                                None,
                                gt=18,
                                title="Edad",
                                description="Indica la edad del usuario",
                                example=23
                            )
    ):
    return {name:age}


#Validaciones path parameters
@app.get("/person/{person_id}")
def show_person(
        person_id: int = Path(
                            ...,
                            ge=1,
                            title="Person Id",
                            description="Identificador del usuario",
                            example=117
                        )
    ):
    return {"created":person_id}


#Validaciones request body
@app.put("/person/{person_id}")
def update_person(
        person_id: int = Path(
            ...,
            ge=1,
            title="Person Id",
            description="Identificador del usuario",
            example=117
        ),
        person: Person = Body(...),
        location: Location = Body(...)
    ):
    result = person.dict()
    result.update(location)
    return result

