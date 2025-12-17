from django.db.models import Count, Avg, Sum, F, Q
from django.db.models.functions import ExtractYear
from .models import Publisher, Author, Comic, Genre, Reader, Review, Borrowing


class AnalyticsRepository:

    @staticmethod
    def get_top_publishers_by_inventory():
        return Publisher.objects.annotate(
            total_stock=Sum('comic__availablenumber'),
            titles_count=Count('comic')
        ).filter(
            total_stock__gt=50
        ).order_by('-total_stock')

    @staticmethod
    def get_highly_rated_authors():
        return Author.objects.annotate(
            avg_rating=Avg('comic__review__rating'),
            review_count=Count('comic__review')
        ).filter(
            avg_rating__gt=3,
            review_count__gt=3
        ).order_by('-avg_rating')

    @staticmethod
    def get_comics_release_activity():
        return Comic.objects.annotate(
            year=ExtractYear('releasedate')
        ).values('year').annotate(
            total_released=Count('comicid')
        ).order_by('-year')

    @staticmethod
    def get_popular_genres():
        return Genre.objects.annotate(
            borrow_count=Count('comic__borrowing')
        ).filter(
            borrow_count__gt=1000
        ).order_by('-borrow_count')

    @staticmethod
    def get_active_readers():
        return Reader.objects.filter(
            isblocked=False
        ).annotate(
            books_borrowed=Count('borrowing')
        ).filter(
            books_borrowed__gt=2
        ).order_by('-books_borrowed')

    @staticmethod
    def get_most_reviewed_comics():
        return Comic.objects.annotate(
            reviews_total=Count('review'),
            rating_avg=Avg('review__rating')
        ).filter(
            reviews_total__gte=1
        ).order_by('-reviews_total')


    @staticmethod
    def get_raw_comic_data():
        return Comic.objects.select_related('genre', 'publisher').values(
            'title',
            'volume',
            'availablenumber',
            'genre__genrename',
            'publisher__name'
        )

    @staticmethod
    def get_raw_review_data():
        return Review.objects.values('rating', 'comic__title')
