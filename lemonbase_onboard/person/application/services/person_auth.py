from typing import Optional

from django.contrib.auth import authenticate

from person.application.requests.person_register import PersonRegisterRequest
from person.application.requests.person_login import PersonLoginRequest
from person.application.serializers.basic_person import BasicPersonSerializer
from person.domain.repositories.person import PersonRepository
from person.domain.commands.person_register import PersonRegisterCommand
from person.domain.models.person import Person


class PersonAuthAppService:
    @classmethod
    def register(
        cls, person_register_request: PersonRegisterRequest
    ) -> BasicPersonSerializer:
        person_register_command = PersonRegisterCommand(
            email=person_register_request.email,
            password=person_register_request.password,
            name=person_register_request.name,
        )
        person = PersonRepository.create(person_register_command)
        return BasicPersonSerializer(person)

    @classmethod
    def login(cls, person_login_request: PersonLoginRequest) -> Optional[Person]:
        return authenticate(
            email=person_login_request.email,
            password=person_login_request.password,
        )
