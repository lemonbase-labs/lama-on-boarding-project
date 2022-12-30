from typing import List

from common.exceptions import ObjectNotExactCountError
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

    @classmethod
    def find_by_entitiy_ids_exact(cls, entity_ids: List[str]) -> List[Person]:
        person_list = cls.model.objects.filter(entity_id__in=entity_ids)
        if len(person_list) != len(entity_ids):
            raise ObjectNotExactCountError()

        return person_list
