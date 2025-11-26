from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import *

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
    path('api/', include(router.urls)),
    path('report/aggregated/', aggregated_report),
    path('', comic_list, name='comic_list'),
    path('comic/<int:pk>/', comic_detail, name='comic_detail'),
    path('comic/new/', comic_create, name='comic_new'),
    path('comic/<int:pk>/edit/', comic_edit, name='comic_edit'),
    path('comic/<int:pk>/delete/', comic_delete, name='comic_delete'),
]
