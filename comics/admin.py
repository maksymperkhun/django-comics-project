from django.contrib import admin

from comics.models import Author, Review, Comic, Borrowing, ComicAuthor, Genre, Publisher, Reader

admin.site.register(Author)
admin.site.register(Comic)
admin.site.register(Review)
admin.site.register(Borrowing)
admin.site.register(ComicAuthor)
admin.site.register(Genre)
admin.register(Publisher)
admin.site.register(Reader)