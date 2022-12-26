from django.db import models


class BaseRepositoryBuilder:
    model: models.Model = None
    query: models.QuerySet = None

    def __init__(self, model):
        self.model = model
        self.query = model.objects

    def execute(self):
        return self.query


class BaseRepository:
    model: models.Model = None
    builder = BaseRepositoryBuilder

    @classmethod
    def build(cls):
        return cls.builder(cls.model)

    @classmethod
    def find_one_or_none(cls, *args, **kwargs):
        try:
            return cls._find_one(**kwargs)
        except models.ObjectDoesNotExist:
            return None

    @classmethod
    def find_one(cls, *args, **kwargs) -> model:
        return cls._find_one(**kwargs)

    @classmethod
    def _find_one(cls, *args, **kwargs):
        return cls.model.objects.get(**kwargs)

    @classmethod
    def find(cls, *args, **kwargs):
        return cls._find(**kwargs)

    @classmethod
    def _find(cls, *args, **kwargs):
        return cls.model.objects.filter(**kwargs)

    @classmethod
    def delete(cls, *args, **kwargs):
        cls.model.objects.filter(**kwargs).delete()