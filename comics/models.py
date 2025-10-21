from django.db import models
from django.utils import timezone

class Genre(models.Model):
    genreid = models.AutoField(primary_key=True)
    genrename = models.CharField(max_length=80)

    class Meta:
        managed = False
        db_table = 'genre'

    def __str__(self):
        return self.genrename

class Publisher(models.Model):
    publisherid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)
    country = models.CharField(max_length=100)
    foundedyear = models.SmallIntegerField()

    class Meta:
        db_table = 'publisher'
        managed = False

    def __str__(self):
        return self.name

class Author(models.Model):
    authorid = models.AutoField(primary_key=True)
    firstname = models.CharField(max_length=60)
    lastname = models.CharField(max_length=80)
    country = models.CharField(max_length=80)

    class Meta:
        managed = False
        db_table = 'author'

    def __str__(self):
        return f"{self.firstname} {self.lastname}"

class Reader(models.Model):
    readerid = models.AutoField(primary_key=True)
    firstname = models.CharField(max_length=60)
    lastname = models.CharField(max_length=80)
    email = models.CharField(max_length=150, unique=True)
    joindate = models.DateField(default=timezone.now)
    isblocked = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = 'reader'

    def __str__(self):
        return f"{self.firstname} {self.lastname} ({self.email})"

class Comic(models.Model):
    comicid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    volume = models.IntegerField(null=True, blank=True)
    releasedate = models.DateField()
    availablenumber = models.IntegerField()
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, db_column='publisherid')
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True, db_column='genreid')
    authors = models.ManyToManyField(Author, through='ComicAuthor')

    class Meta:
        managed = False
        db_table = 'comic'

    def __str__(self):
        return self.title

class ComicAuthor(models.Model):
    comic = models.ForeignKey(Comic, on_delete=models.CASCADE, db_column='comicid')
    author = models.ForeignKey(Author, on_delete=models.CASCADE, db_column='authorid')

    class Meta:
        unique_together = ('comic', 'author')
        managed = False
        db_table = 'comicauthor'

class Review(models.Model):
    reviewid = models.AutoField(primary_key=True)
    comic = models.ForeignKey(Comic, on_delete=models.CASCADE, db_column='comicid')
    reader = models.ForeignKey(Reader, on_delete=models.CASCADE, db_column='readerid')
    rating = models.SmallIntegerField()
    comment = models.TextField(null=True, blank=True)
    reviewdate = models.DateField(default=timezone.now)

    class Meta:
        managed = False
        db_table = 'review'
    def __str__(self):
        return f"Review for {self.comic.title} by {self.reader.firstname}"

class Borrowing(models.Model):
    borrowingid = models.AutoField(primary_key=True)
    comic = models.ForeignKey(Comic, on_delete=models.CASCADE, db_column='comicid')
    reader = models.ForeignKey(Reader, on_delete=models.CASCADE, db_column='readerid')
    borrowdate = models.DateField(default=timezone.now)
    duedate = models.DateField()
    returndate = models.DateField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'borrowing'

    def __str__(self):
        return f"{self.comic.title} borrowed by {self.reader.firstname}"
