from person.domain.models.person import Person
from common.base_repository import BaseRepository
from person.domain.commands.person_register import PersonRegisterCommand


class PersonRepository(BaseRepository):
    model = Person

    @classmethod
    def register(cls, person_register_command: PersonRegisterCommand) -> Person:
        person = cls.model(
            **person_register_command.dict(),
        )
        person.save()
        return person
