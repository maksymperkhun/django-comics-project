from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ComicViewSet, GenreViewSet, AuthorViewSet, PublisherViewSet,
    ReviewViewSet, BorrowingViewSet, ComicAuthorViewSet, ReaderViewSet,
    aggregated_report
)

router = DefaultRouter()
router.register(r'comics', ComicViewSet, basename='comics')
router.register(r'genres', GenreViewSet, basename='genres')
router.register(r'authors', AuthorViewSet, basename='authors')
router.register(r'readers', ReaderViewSet, basename='readers')
router.register(r'publishers', PublisherViewSet, basename='publishers')
router.register(r'comicauthor', ComicAuthorViewSet, basename='comicauthor')
router.register(r'reviews', ReviewViewSet, basename='reviews')
router.register(r'borrowings', BorrowingViewSet, basename='borrowings')

urlpatterns = [
    path('', include(router.urls)),
    path('report/aggregated/', aggregated_report),
]
