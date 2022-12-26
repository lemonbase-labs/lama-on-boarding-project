from django.contrib.auth.hashers import make_password

from person.application.requests.person_register import PersonRegisterRequest
from person.application.dtos.basic_person import BasicPersonDTO
from person.domain.repositories.person import PersonRepository
from person.domain.commands.person_register import PersonRegisterCommand


class PersonAuthAppService:
    @classmethod
    def register(cls, person_register_request: PersonRegisterRequest) -> BasicPersonDTO:
        person_register_command = PersonRegisterCommand(
            username=person_register_request.username,
            password=make_password(person_register_request.password),
            name=person_register_request.name,
        )
        person = PersonRepository.register(person_register_command)
        return BasicPersonDTO(**person.__dict__)
