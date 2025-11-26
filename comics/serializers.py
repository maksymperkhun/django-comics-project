
import datetime

from rest_framework import serializers
from .models import *
from comics.repositories.django_repositories import *

author_repo = DjangoAuthorRepository()
comic_repo = DjangoComicRepository()
reader_repo = DjangoReaderRepository()
genre_repo = DjangoGenreRepository()
review_repo = DjangoReviewRepository()
borrowing_repo = DjangoBorrowingRepository()
comicauthor_repo = DjangoComicAuthorRepository()
publisher_repo = DjangoPublisherRepository()


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

    def create(self, validated_data):
        genre = Genre(**validated_data)
        return genre_repo.add(genre)

    def update(self, instance, validated_data):
        for k, v in validated_data.items():
            setattr(instance, k, v)
        return genre_repo.update(instance)


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = '__all__'

    def create(self, validated_data):
        p = Publisher(**validated_data)
        return publisher_repo.add(p)

    def update(self, instance, validated_data):
        for k, v in validated_data.items():
            setattr(instance, k, v)
        return publisher_repo.update(instance)


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

    def create(self, validated_data):
        a = Author(**validated_data)
        return author_repo.add(a)

    def update(self, instance, validated_data):
        for k, v in validated_data.items():
            setattr(instance, k, v)
        return author_repo.update(instance)


class ReaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reader
        fields = '__all__'

    def create(self, validated_data):
        r = Reader(**validated_data)
        return reader_repo.add(r)

    def update(self, instance, validated_data):
        for k, v in validated_data.items():
            setattr(instance, k, v)
        return reader_repo.update(instance)


class ComicAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComicAuthor
        fields = ['comic', 'author']

    def create(self, validated_data):
        ca = ComicAuthor(**validated_data)
        return comicauthor_repo.add(ca)


class ComicSerializer(serializers.ModelSerializer):
    authors = serializers.PrimaryKeyRelatedField(many=True, queryset=Author.objects.all())


    class Meta:
        model = Comic
        fields = '__all__'

    def create(self, validated_data):
        authors = validated_data.pop('authors', [])
        comic = Comic(**validated_data)
        comic = comic_repo.add(comic)

        for author in authors:
            ca = ComicAuthor(comic=comic, author=author)
            comicauthor_repo.add(ca)
        return comic

    def update(self, instance, validated_data):
        authors = validated_data.pop('authors', None)
        for k, v in validated_data.items():
            setattr(instance, k, v)
        instance = comic_repo.update(instance)

        if authors is not None:
            comicauthor_repo.delete_by_comic(instance)
            for author in authors:
                ca = ComicAuthor(comic=instance, author=author)
                comicauthor_repo.add(ca)
        return instance


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

    def create(self, validated_data):
        r = Review(**validated_data)
        return review_repo.add(r)

    def update(self, instance, validated_data):
        for k, v in validated_data.items():
            setattr(instance, k, v)
        return review_repo.update(instance)


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = '__all__'

    def create(self, validated_data):
        b = Borrowing(**validated_data)
        return borrowing_repo.add(b)

    def update(self, instance, validated_data):
        for k, v in validated_data.items():
            setattr(instance, k, v)
        return borrowing_repo.update(instance)
