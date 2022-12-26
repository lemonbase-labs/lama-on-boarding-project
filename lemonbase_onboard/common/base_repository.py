from django.db import models


class BaseRepository:
    model: models.Model = None

    @classmethod
    def get_queryset(cls):
        return cls.model.objects

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