from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action, api_view
from .serializers import *
from comics.repositories.django_repositories import *
from comics.models import Comic, Review, Borrowing

author_repo = DjangoAuthorRepository()
comic_repo = DjangoComicRepository()
reader_repo = DjangoReaderRepository()
genre_repo = DjangoGenreRepository()
review_repo = DjangoReviewRepository()
borrowing_repo = DjangoBorrowingRepository()
comicauthor_repo = DjangoComicAuthorRepository()
publisher_repo = DjangoPublisherRepository()


class GenericRepoViewSet(viewsets.ViewSet):

    repo = None
    serializer_class = None

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]


    def list(self, request):
        objs = self.repo.get_all()
        serializer = self.serializer_class(objs, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        obj = self.repo.get_by_id(pk)
        if obj is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(obj)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()
        return Response(self.serializer_class(obj).data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        obj = self.repo.get_by_id(pk)
        if obj is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()
        return Response(self.serializer_class(obj).data)


    def partial_update(self, request, pk=None):
        obj = self.repo.get_by_id(pk)
        if obj is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()
        return Response(self.serializer_class(obj).data)

    def destroy(self, request, pk=None):
        obj = self.repo.get_by_id(pk)
        if obj is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            self.repo.delete(obj)
        except Exception:
            # fallback
            obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GenreViewSet(GenericRepoViewSet):
    repo = genre_repo
    serializer_class = GenreSerializer


class PublisherViewSet(GenericRepoViewSet):
    repo = publisher_repo
    serializer_class = PublisherSerializer


class AuthorViewSet(GenericRepoViewSet):
    repo = author_repo
    serializer_class = AuthorSerializer


class ReaderViewSet(GenericRepoViewSet):
    repo = reader_repo
    serializer_class = ReaderSerializer


class ComicAuthorViewSet(GenericRepoViewSet):
    repo = comicauthor_repo
    serializer_class = ComicAuthorSerializer


class ComicViewSet(GenericRepoViewSet):
    repo = comic_repo
    serializer_class = ComicSerializer


class ReviewViewSet(GenericRepoViewSet):
    repo = review_repo
    serializer_class = ReviewSerializer


class BorrowingViewSet(GenericRepoViewSet):
    repo = borrowing_repo
    serializer_class = BorrowingSerializer



@api_view(['GET'])
def aggregated_report(request):
    total_authors = len(author_repo.get_all())
    total_comics = len(comic_repo.get_all())
    total_readers = len(reader_repo.get_all())
    total_genres = len(genre_repo.get_all())
    total_publishers = len(publisher_repo.get_all())
    total_reviews = len(review_repo.get_all())
    total_borrowings = len(borrowing_repo.get_all())


    active_borrowings_qs = Borrowing.objects.filter(returndate__isnull=True)
    active_borrowings = [{
        'borrowid': b.borrowid,
        'comic': b.comic.title,
        'reader': f"{b.reader.firstname} {b.reader.lastname}",
        'borrowdate': b.borrowdate,
        'duedate': b.duedate
    } for b in active_borrowings_qs]


    report = {
        'totals': {
            'authors': total_authors,
            'comics': total_comics,
            'readers': total_readers,
            'genres': total_genres,
            'publishers': total_publishers,
            'reviews': total_reviews,
            'borrowings': total_borrowings,
        },
        'active_borrowings': active_borrowings,
    }
    return Response(report)
