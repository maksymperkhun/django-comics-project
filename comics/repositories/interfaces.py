from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional
from comics.models import Author, Comic, Reader, Genre, Borrowing, Review, Publisher

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


class IAuthorRepository(IRepository[Author]):
    pass

class IComicRepository(IRepository[Comic]):
    pass

class IReaderRepository(IRepository[Reader]):
    pass

class IGenreRepository(IRepository[Genre]):
    pass

class IBorrowingRepository(IRepository[Borrowing]): # <- Виправлено
    pass

class IReviewRepository(IRepository[Review]): # <- Виправлено
    pass

class IPublisherRepository(IRepository[Publisher]):
    pass