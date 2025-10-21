# comics/repositories/django_repositories.py
from typing import List, Optional
from comics.models import Author, Comic, Reader
from.interfaces import IAuthorRepository, IComicRepository, IReaderRepository

class DjangoAuthorRepository(IAuthorRepository):
    def get_by_id(self, id: int) -> Optional[Author]:
        try:
            return Author.objects.get(pk=id)
        except Author.DoesNotExist:
            return None

    def get_all(self) -> List[Author]:
        return list(Author.objects.all())

    def add(self, entity: Author) -> Author:
        entity.save()
        return entity

class DjangoComicRepository(IComicRepository):
    def get_by_id(self, id: int) -> Optional[Comic]:
        try:
            # Використовуємо select_related для оптимізації
            return Comic.objects.select_related('publisher', 'genre').get(pk=id)
        except Comic.DoesNotExist:
            return None

    def get_all(self) -> List[Comic]:
        return list(Comic.objects.select_related('publisher', 'genre').all())

    def add(self, entity: Comic) -> Comic:
        entity.save()
        return entity

class DjangoReaderRepository(IReaderRepository):
    def get_by_id(self, id: int) -> Optional:
        try:
            return Reader.objects.get(pk=id)
        except Reader.DoesNotExist:
            return None

    def get_all(self) -> List:
        return list(Reader.objects.all())

    def add(self, entity: Reader) -> Reader:
        entity.save()
        return entity

#... і так далі