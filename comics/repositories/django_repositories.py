# comics/repositories.py
from typing import List, Optional
from comics.models import Author, Comic, Reader, Genre, Review, Borrowing, ComicAuthor, Publisher
from .interfaces import (
    IAuthorRepository, IComicRepository, IReaderRepository, IGenreRepository,
    IReviewRepository, IBorrowingRepository, IComicAuthorRepository, IPublisherRepository
)

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

    def update(self, entity: Author) -> Author:
        entity.save()
        return entity

    def delete(self, entity: Author) -> None:
        entity.delete()


class DjangoComicRepository(IComicRepository):
    def get_by_id(self, id: int) -> Optional[Comic]:
        try:
            return Comic.objects.select_related('publisher', 'genre').get(pk=id)
        except Comic.DoesNotExist:
            return None

    def get_all(self) -> List[Comic]:
        return list(Comic.objects.select_related('publisher', 'genre').all())

    def add(self, entity: Comic) -> Comic:
        entity.save()
        return entity

    def update(self, entity: Comic) -> Comic:
        entity.save()
        return entity

    def delete(self, entity: Comic) -> None:
        entity.delete()


class DjangoReaderRepository(IReaderRepository):
    def get_by_id(self, id: int) -> Optional[Reader]:
        try:
            return Reader.objects.get(pk=id)
        except Reader.DoesNotExist:
            return None

    def get_all(self) -> List[Reader]:
        return list(Reader.objects.all())

    def add(self, entity: Reader) -> Reader:
        entity.save()
        return entity

    def update(self, entity: Reader) -> Reader:
        entity.save()
        return entity

    def delete(self, entity: Reader) -> None:
        entity.delete()


class DjangoGenreRepository(IGenreRepository):
    def get_by_id(self, id: int) -> Optional[Genre]:
        try:
            return Genre.objects.get(pk=id)
        except Genre.DoesNotExist:
            return None

    def get_all(self) -> List[Genre]:
        return list(Genre.objects.all())

    def add(self, entity: Genre) -> Genre:
        entity.save()
        return entity

    def update(self, entity: Genre) -> Genre:
        entity.save()
        return entity

    def delete(self, entity: Genre) -> None:
        entity.delete()


class DjangoReviewRepository(IReviewRepository):
    def get_by_id(self, id: int) -> Optional[Review]:
        try:
            return Review.objects.get(pk=id)
        except Review.DoesNotExist:
            return None

    def get_all(self) -> List[Review]:
        return list(Review.objects.all())

    def add(self, entity: Review) -> Review:
        entity.save()
        return entity

    def update(self, entity: Review) -> Review:
        entity.save()
        return entity

    def delete(self, entity: Review) -> None:
        entity.delete()


class DjangoBorrowingRepository(IBorrowingRepository):
    def get_by_id(self, id: int) -> Optional[Borrowing]:
        try:
            return Borrowing.objects.get(pk=id)
        except Borrowing.DoesNotExist:
            return None

    def get_all(self) -> List[Borrowing]:
        return list(Borrowing.objects.all())

    def add(self, entity: Borrowing) -> Borrowing:
        entity.save()
        return entity

    def update(self, entity: Borrowing) -> Borrowing:
        entity.save()
        return entity

    def delete(self, entity: Borrowing) -> None:
        entity.delete()


class DjangoComicAuthorRepository(IComicAuthorRepository):
    def get_by_id(self, id: int) -> Optional[ComicAuthor]:
        try:
            return ComicAuthor.objects.get(pk=id)
        except ComicAuthor.DoesNotExist:
            return None

    def get_all(self) -> List[ComicAuthor]:
        return list(ComicAuthor.objects.all())

    def add(self, entity: ComicAuthor) -> ComicAuthor:
        entity.save()
        return entity

    def update(self, entity: ComicAuthor) -> ComicAuthor:
        entity.save()
        return entity

    def delete(self, entity: ComicAuthor) -> None:
        entity.delete()

    # Додаткові зручні методи
    def delete_by_comic(self, comic: Comic) -> None:
        ComicAuthor.objects.filter(comic=comic).delete()

    def get_authors_for_comic(self, comic: Comic) -> List[ComicAuthor]:
        return list(ComicAuthor.objects.filter(comic=comic))


class DjangoPublisherRepository(IPublisherRepository):
    def get_by_id(self, id: int) -> Optional[Publisher]:
        try:
            return Publisher.objects.get(pk=id)
        except Publisher.DoesNotExist:
            return None

    def get_all(self) -> List[Publisher]:
        return list(Publisher.objects.all())

    def add(self, entity: Publisher) -> Publisher:
        entity.save()
        return entity

    def update(self, entity: Publisher) -> Publisher:
        entity.save()
        return entity

    def delete(self, entity: Publisher) -> None:
        entity.delete()
