import django_filters

from reviews.models import Title


class GenreFilter(django_filters.FilterSet):
    genre = django_filters.CharFilter(
        field_name='genre__slug', method='filter_genre')
    category = django_filters.CharFilter(
        field_name='category__slug', method='filter_category')
    year = django_filters.CharFilter(field_name='year', method='filter_year')
    name = django_filters.CharFilter(field_name='name', method='filter_name')

    class Meta:
        model = Title
        fields = ('genre', 'category', 'name', 'year',)

    def filter_genre(self, queryset, name, genre):
        return Title.objects.filter(genre__slug__contains=genre)

    def filter_category(self, queryset, name, category):
        return Title.objects.filter(category__slug__contains=category)

    def filter_year(self, queryset, name, year):
        return Title.objects.filter(year__contains=year)

    def filter_name(self, queryset, names, name):
        return Title.objects.filter(name__contains=name)
