from.interfaces import IAuthorRepository, IComicRepository, IReaderRepository
from.django_repositories import DjangoAuthorRepository, DjangoComicRepository, DjangoReaderRepository

class RepositoryFacade:
    def __init__(self):
        self._author_repo: IAuthorRepository = DjangoAuthorRepository()
        self._comic_repo: IComicRepository = DjangoComicRepository()
        self._reader_repo: IReaderRepository = DjangoReaderRepository()


    @property
    def authors(self) -> IAuthorRepository:
        return self._author_repo

    @property
    def comics(self) -> IComicRepository:
        return self._comic_repo

    @property
    def readers(self) -> IReaderRepository:
        return self._reader_repo

