from bokeh.resources import CDN
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action, api_view
from .serializers import *
from comics.repositoriesdir.django_repositories import *
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


# comics/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Comic
from .forms import ComicForm

# 1. Список об'єктів
def comic_list(request):
    comics = Comic.objects.all()
    return render(request, 'comics/comic_list.html', {'comics': comics})

# 2. Деталі об'єкта
def comic_detail(request, pk):
    comic = get_object_or_404(Comic, pk=pk)
    return render(request, 'comics/comic_detail.html', {'comic': comic})

# 3. Створення нового об'єкта
def comic_create(request):
    if request.method == "POST":
        form = ComicForm(request.POST)
        if form.is_valid():
            comic = form.save()
            return redirect('comic_detail', pk=comic.pk)
    else:
        form = ComicForm()
    return render(request, 'comics/comic_form.html', {'form': form, 'action': 'Створити'})

# 4. Редагування об'єкта
def comic_edit(request, pk):
    comic = get_object_or_404(Comic, pk=pk)
    if request.method == "POST":
        form = ComicForm(request.POST, instance=comic) # instance заповнює форму старими даними
        if form.is_valid():
            form.save()
            return redirect('comic_detail', pk=comic.pk)
    else:
        form = ComicForm(instance=comic)
    return render(request, 'comics/comic_form.html', {'form': form, 'action': 'Редагувати'})

# 5. Видалення об'єкта
def comic_delete(request, pk):
    comic = get_object_or_404(Comic, pk=pk)
    if request.method == "POST":
        comic.delete()
        return redirect('comic_list')
    return render(request, 'comics/comic_confirm_delete.html', {'comic': comic})



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


from django.shortcuts import render, redirect
from .NetworkHelper import NetworkHelper

API_URL = "http://127.0.0.1:8001/api/clients/"
API_USER = "admin"
API_PASS = "admin"


def external_api_list(request):
    helper = NetworkHelper(API_URL, API_USER, API_PASS)

    # Отримуємо дані з чужого сайту
    external_data = helper.get_list()

    return render(request, 'comics/api_list.html', {'items': external_data})


def external_api_delete(request, item_id):
    if request.method == "POST":
        helper = NetworkHelper(API_URL, API_USER, API_PASS)
        helper.delete_item(item_id)
    return redirect('external_list')


from rest_framework.views import APIView



class BasePandasView(APIView):
    def export_data(self, queryset, fields):
        data = list(queryset.values(*fields))
        df = pd.DataFrame(data)

        if df.empty:
            return Response({"message": "Даних не знайдено", "data": []})

        return Response(df.to_dict(orient='records'))


class PublisherInventoryView(BasePandasView):
    def get(self, request):
        qs = AnalyticsRepository.get_top_publishers_by_inventory()
        return self.export_data(qs, fields=['name', 'country', 'total_stock', 'titles_count'])


class TopAuthorsView(BasePandasView):
    def get(self, request):
        qs = AnalyticsRepository.get_highly_rated_authors()
        return self.export_data(qs, fields=['firstname', 'lastname', 'avg_rating', 'review_count'])


class ReleaseActivityView(BasePandasView):
    def get(self, request):
        qs = AnalyticsRepository.get_comics_release_activity()
        return self.export_data(qs, fields=['year', 'total_released'])


class PopularGenresView(BasePandasView):
    def get(self, request):
        qs = AnalyticsRepository.get_popular_genres()
        return self.export_data(qs, fields=['genrename', 'borrow_count'])


class ActiveReadersView(BasePandasView):
    def get(self, request):
        qs = AnalyticsRepository.get_active_readers()
        return self.export_data(qs, fields=['firstname', 'lastname', 'email', 'books_borrowed'])


class ComicReviewsView(BasePandasView):
    def get(self, request):
        qs = AnalyticsRepository.get_most_reviewed_comics()
        return self.export_data(qs, fields=['title', 'reviews_total', 'rating_avg'])


from rest_framework.views import APIView
from rest_framework.response import Response


class BasicStatsView(APIView):
    def get(self, request):
        comics_qs = AnalyticsRepository.get_raw_comic_data()
        reviews_qs = AnalyticsRepository.get_raw_review_data()

        df_comics = pd.DataFrame(list(comics_qs))
        df_reviews = pd.DataFrame(list(reviews_qs))

        if df_comics.empty or df_reviews.empty:
            return Response({"message": "Not enough data for statistics"})

        stock_stats = df_comics['availablenumber'].describe().to_dict()

        median_stock = df_comics['availablenumber'].median()

        rating_stats = {
            'min_rating': df_reviews['rating'].min(),
            'max_rating': df_reviews['rating'].max(),
            'mean_rating': round(df_reviews['rating'].mean(), 2),
            'median_rating': df_reviews['rating'].median()
        }

        genre_grouping = df_comics.groupby('genre__genrename')['availablenumber'].mean().reset_index()
        genre_grouping.columns = ['Genre', 'Average_Stock']

        comic_rating_grouping = df_reviews.groupby('comic__title')['rating'].max().reset_index()
        comic_rating_grouping.columns = ['Comic', 'Max_Rating']

        response_data = {
            "general_stats": {
                "stock_statistics": stock_stats,
                "stock_median_explicit": median_stock,
                "rating_statistics": rating_stats
            },
            "grouped_analysis": {
                "avg_stock_by_genre": genre_grouping.to_dict(orient='records'),
                "max_rating_by_comic": comic_rating_grouping.to_dict(orient='records')
            }
        }

        return Response(response_data)


from django.shortcuts import render
from rest_framework.views import APIView
import pandas as pd
import plotly.express as px
import plotly.io as pio


from .repositories import AnalyticsRepository


class DashboardPlotlyView(APIView):
    def get(self, request):
        min_stock = int(request.GET.get('min_stock', 0))

        charts = []

        qs1 = AnalyticsRepository.get_top_publishers_by_inventory()
        df1 = pd.DataFrame(list(qs1.values('name', 'total_stock')))
        if not df1.empty:
            df1 = df1[df1['total_stock'] >= min_stock]
            fig1 = px.bar(df1, x='name', y='total_stock', title=f"Видавництва з > {min_stock} книг", color='name')
            charts.append(pio.to_html(fig1, full_html=False))


        qs2 = AnalyticsRepository.get_highly_rated_authors()
        df2 = pd.DataFrame(list(qs2.values('lastname', 'avg_rating', 'review_count')))
        if not df2.empty:
            fig2 = px.scatter(df2, x='review_count', y='avg_rating', hover_name='lastname', size='review_count',
                              title="Автори: Рейтинг vs Кількість відгуків")
            charts.append(pio.to_html(fig2, full_html=False))


        qs3 = AnalyticsRepository.get_comics_release_activity()
        df3 = pd.DataFrame(list(qs3.values('year', 'total_released')))
        if not df3.empty:
            df3 = df3.sort_values('year')
            fig3 = px.line(df3, x='year', y='total_released', markers=True, title="Динаміка випуску коміксів")
            charts.append(pio.to_html(fig3, full_html=False))


        qs4 = AnalyticsRepository.get_popular_genres()
        df4 = pd.DataFrame(list(qs4.values('genrename', 'borrow_count')))
        if not df4.empty:
            fig4 = px.pie(df4, values='borrow_count', names='genrename', title="Частка жанрів у позичаннях")
            charts.append(pio.to_html(fig4, full_html=False))


        qs5 = AnalyticsRepository.get_active_readers()
        df5 = pd.DataFrame(list(qs5.values('lastname', 'books_borrowed')))

        if not df5.empty:
            df5 = df5.sort_values('books_borrowed', ascending=True)
            df5_top = df5.tail(20)

            fig5 = px.bar(
                df5_top,
                x='books_borrowed',
                y='lastname',
                orientation='h',
                title="Топ-20 Активних читачів",
                text='books_borrowed',
            )
            charts.append(pio.to_html(fig5, full_html=False))


        qs6 = AnalyticsRepository.get_most_reviewed_comics()
        df6 = pd.DataFrame(list(qs6.values('title', 'rating_avg', 'reviews_total')))

        if not df6.empty:
            df6_top = df6.head(20)

            fig6 = px.bar(
                df6_top,
                x='title',
                y='rating_avg',
                title="Рейтинг популярних коміксів",
                labels={'rating_avg': 'Рейтинг', 'title': 'Комікс'}
            )

            charts.append(pio.to_html(fig6, full_html=False))
        return render(request, 'comics/dashboard_plotly.html', {
            'charts': charts,
            'filters': {'min_stock': min_stock}
        })



from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.resources import CDN
from bokeh.transform import factor_cmap, cumsum, linear_cmap

from math import pi


class DashboardBokehView(APIView):
    def get(self, request):
        min_stock = int(request.GET.get('min_stock', 0))
        script_divs = []

        qs1 = AnalyticsRepository.get_top_publishers_by_inventory()
        df1 = pd.DataFrame(list(qs1.values('name', 'total_stock')))
        if not df1.empty:
            df1 = df1[df1['total_stock'] >= min_stock]
            source = ColumnDataSource(df1)
            publishers = df1['name'].tolist()

            p = figure(x_range=publishers, height=400, title="1. Видавництва (Inventory)",
                       toolbar_location=None, tools="", sizing_mode='stretch_width')
            p.vbar(x='name', top='total_stock', width=0.9, source=source,
                   line_color='white')
            script_divs.append(components(p))


        qs2 = AnalyticsRepository.get_highly_rated_authors()
        df2 = pd.DataFrame(list(qs2.values('lastname', 'avg_rating', 'review_count')))
        if not df2.empty:
            df2 = df2.head(20)
            source = ColumnDataSource(df2)
            p = figure(height=400, title="2. Автори (Rating vs Reviews)", sizing_mode='stretch_width')
            p.circle(x='review_count', y='avg_rating', size=15, source=source)
            script_divs.append(components(p))


        qs3 = AnalyticsRepository.get_comics_release_activity()
        df3 = pd.DataFrame(list(qs3.values('year', 'total_released')))
        if not df3.empty:
            df3 = df3.sort_values('year')
            p = figure(height=400, title="3. Динаміка публікацій", sizing_mode='stretch_width')
            p.line(df3['year'], df3['total_released'], line_width=3, color="navy")
            p.circle(df3['year'], df3['total_released'], size=8, line_color="navy")
            script_divs.append(components(p))


        qs4 = AnalyticsRepository.get_popular_genres()
        df4 = pd.DataFrame(list(qs4.values('genrename', 'borrow_count')))

        if not df4.empty:
            df4['angle'] = df4['borrow_count'] / df4['borrow_count'].sum() * 2 * pi

            source = ColumnDataSource(df4)

            p = figure(height=400, title="4. Популярні жанри (Pie Chart)", toolbar_location=None,
                       tools="hover", tooltips="@genrename: @borrow_count", x_range=(-0.5, 1.0),
                       sizing_mode='stretch_width')

            p.wedge(x=0, y=1, radius=0.4,
                    start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
                    line_color="white", legend_field='genrename', source=source)

            p.axis.axis_label = None
            p.axis.visible = False
            p.grid.grid_line_color = None

            script_divs.append(components(p))

        qs5 = AnalyticsRepository.get_active_readers()
        df5 = pd.DataFrame(list(qs5.values('lastname', 'books_borrowed')))

        if not df5.empty:
            df5 = df5.sort_values('books_borrowed', ascending=True).tail(15)  # Топ-15
            readers = df5['lastname'].tolist()
            source = ColumnDataSource(df5)

            p = figure(y_range=readers, height=400, title="5. Топ читачів (Horizontal)",
                       toolbar_location=None, tools="", sizing_mode='stretch_width')

            p.hbar(y='lastname', right='books_borrowed', height=0.8, source=source,
                   line_color="white")

            script_divs.append(components(p))


        qs6 = AnalyticsRepository.get_most_reviewed_comics()
        df6 = pd.DataFrame(list(qs6.values('title', 'rating_avg', 'reviews_total')))

        if not df6.empty:
            df6 = df6.head(20)
            source = ColumnDataSource(df6)
            titles = df6['title'].tolist()

            p = figure(x_range=titles, height=400, title="6. Рейтинг популярних коміксів (Color Map)",
                       toolbar_location=None, tools="", sizing_mode='stretch_width')

            p.vbar(x='title', top='rating_avg', width=0.9, source=source)

            p.xaxis.major_label_orientation = 0.785

            script_divs.append(components(p))

        resources = CDN.render()

        return render(request, 'comics/dashboard_bokeh.html', {
            'charts': script_divs,
            'filters': {'min_stock': min_stock},
            'resources': resources
        })


from .benchmark import DatabaseBenchmark


class BenchmarkView(APIView):


    def get(self, request):
        # При GET запиті просто показуємо порожню сторінку з кнопкою
        return render(request, 'comics/benchmark.html', {'chart': None})

    def post(self, request):
        # Отримуємо налаштування з форми
        try:
            total_requests = int(request.POST.get('total_requests', 200))
        except ValueError:
            total_requests = 200

        # 1. Запускаємо бенчмарк
        # Тестуємо на 1, 2, 4, 8, 16, 32 потоках
        data = DatabaseBenchmark.run_benchmark(
            total_requests=total_requests,
            max_workers_list=[1, 2, 4, 5, 8, 10, 16, 32]
        )

        # 2. Будуємо графік Plotly
        df = pd.DataFrame(data)

        fig = px.line(
            df,
            x='workers',
            y='time',
            markers=True,
            title=f"Залежність часу виконання від кількості потоків ({total_requests} запитів)",
            labels={'workers': 'Кількість потоків', 'time': 'Час виконання (сек)'}
        )

        # Додаємо лінію тренду або просто прикрашаємо
        fig.update_layout(
            xaxis=dict(tickmode='linear'),  # Показувати всі кроки на осі X
            template="plotly_white"
        )

        chart_html = pio.to_html(fig, full_html=False)

        return render(request, 'comics/benchmark.html', {
            'chart': chart_html,
            'last_requests': total_requests
        })