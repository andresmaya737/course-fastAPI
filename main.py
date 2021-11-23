#python
from typing import Optional
from enum import Enum

#pydantic
from pydantic import BaseModel
from pydantic import Field
from pydantic import EmailStr

#FastAPI
from fastapi import FastAPI, responses
from fastapi import Body, Query, Path, Form, Cookie, Header, File, UploadFile
from fastapi import status
from fastapi import HTTPException

app = FastAPI()

#------------------------------------------------------------------------------------------
# Models
#------------------------------------------------------------------------------------------

class HairColor(Enum):
    white = "white"
    black = "black"


class PersonBase(BaseModel):
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


class Person(PersonBase):
    password:str = Field(...,min_length=8)
    
    
class PersonOut(PersonBase):
    pass


class Location(BaseModel):
    city:str = Field()
    country:str = Field(...
                )


class LoginOut(BaseModel):
    username: str = Field(
                        ...,
                        max_length=20,
                        example="andresmaya737"
                    )


#------------------------------------------------------------------------------------------
# Path Operations
#------------------------------------------------------------------------------------------


@app.get(
        path="/", 
        status_code=status.HTTP_200_OK,
        tags=["Home"]
    ) #path operation decorator
def home(): #path operation function
    return {"Hello":"world"}


#Request and response body
@app.post(
        path="/person",
        response_model=PersonOut,
        status_code=status.HTTP_201_CREATED,
        tags=["Persons"],
        summary="Create Person in the app"
    )
def create_person(person: Person = Body(...)):
    """
    Create Person

    This path operation creates a person in the app and save the informacion in the database

    Parameters:
    - Request body parameter:
        - **person: Person** -> A person model with name, last name, age, hair color and marital status

    Returns a person model with first name, last name, age, hair color and marital status
    """
    return person


#Validaciones query parameters
@app.get(
        path="/person/detail",
        status_code=status.HTTP_200_OK,
        tags=["Persons"],
        deprecated=True
    )
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
    """
    Show all persons created in the app

    This path operation shows all persons created in the app and satisfy some optional query parameters

    Parameters:
    - Request query parameter:
        - **name: str** -> Name of the person to filter
        - **age: str** -> Age of the person ti filter

    Returns the name and age of the person
    """
    return {name:age}


#Validaciones path parameters

persons = [1,2,3,4,5] #Simulando base de datos de id's

@app.get(
        path="/person/detail/{person_id}",
        status_code=status.HTTP_200_OK,
        tags=["Persons"])
def show_person(
        person_id: int = Path(
                            ...,
                            ge=1,
                            title="Person Id",
                            description="Identificador del usuario",
                            example=117
                        )
    ):
    """
    Find a person by id created in the app

    This path operation shows a persons created in the app and satisfy a path parameter

    Parameters:
    - Request path parameter:
        - **person_id: int** -> Id of the person created in the app 

    Returns the id of the person
    """

    if(person_id not in persons):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This person doesn't exist!"
        )
    return {"created":person_id}


#Validaciones request body
@app.put(
        path="/person/{person_id}",
        status_code=status.HTTP_201_CREATED,
        tags=["Persons"]
    )
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


#Formularios
@app.post(
    path="/login",
    response_model=LoginOut,
    status_code=status.HTTP_200_OK,
    tags=["Login"]
)
def login(
    username:str = Form(...),
    password:str = Form(...)
    ):
    return LoginOut(username=username)

    
#Cookies and headers parameters
@app.post(
    path="/contact",
    status_code=status.HTTP_200_OK,
    tags=["Contact"]
)
def contact(
        first_name: str = Form(
                            ...,
                            max_length=20,
                            min_length=1
                        ),
        last_name: str = Form(
                            ...,
                            max_length=20,
                            min_length=1
                        ),
        email: EmailStr = Form(...),
        message: str = Form(
            ...,
            min_length=20
        ),
        user_agent: Optional[str] = Header(default=None),
        ads: Optional[str] = Cookie(default=None) #Para controlar las cookies
        
    ):
    return user_agent


@app.post(
    path="/post-image",
    tags=["Files"]
)
def post_image(
        image: UploadFile = File(...)
    ):
    return {
        "Filename":image.filename,
        "Format":image.content_type,
        "Size(Kb)":round(len(image.file.read())/1024,2)
    }
