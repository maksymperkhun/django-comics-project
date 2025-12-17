
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional
from comics.models import Author, Comic, Reader, Review, Publisher, ComicAuthor, Borrowing, Genre

T = TypeVar('T')

class IRepository(ABC, Generic[T]):
    @abstractmethod
    def get_by_id(self, id: int) -> Optional[T]:
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> List[T]:
        raise NotImplementedError

    @abstractmethod
    def add(self, entity: T) -> T:
        raise NotImplementedError

    # Додано: update та delete, бо вони потрібні у view/serializer-ах
    @abstractmethod
    def update(self, entity: T) -> T:
        raise NotImplementedError

    @abstractmethod
    def delete(self, entity: T) -> None:
        raise NotImplementedError


class IAuthorRepository(IRepository[Author]):
    pass

class IComicRepository(IRepository[Comic]):
    pass

class IReaderRepository(IRepository[Reader]):
    pass

class IReviewRepository(IRepository[Review]):
    pass

class IPublisherRepository(IRepository[Publisher]):
    pass

class IComicAuthorRepository(IRepository[ComicAuthor]):
    pass

class IBorrowingRepository(IRepository[Borrowing]):
    pass

class IGenreRepository(IRepository[Genre]):
    pass
