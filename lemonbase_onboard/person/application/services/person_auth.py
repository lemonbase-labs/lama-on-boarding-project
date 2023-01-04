from typing import Optional, Any

from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate

from person.application.requests.person_register import PersonRegisterRequest
from person.application.requests.person_login import PersonLoginRequest
from person.application.dtos.basic_person import BasicPersonDTO
from person.domain.repositories.person import PersonRepository
from person.domain.commands.person_register import PersonRegisterCommand
from person.domain.models.person import Person

class PersonAuthAppService:
    @classmethod
    def register(cls, person_register_request: PersonRegisterRequest) -> BasicPersonDTO:
        person_register_command = PersonRegisterCommand(
            email=person_register_request.email,
            password=make_password(person_register_request.password),
            name=person_register_request.name,
        )
        person = PersonRepository.create(person_register_command)
        return BasicPersonDTO(person)

    @classmethod
    def login(cls, person_login_request: PersonLoginRequest) -> Optional[Person]:
        return authenticate(
            email=person_login_request.email,
            password=person_login_request.password,
        )
