from rest_framework import serializers, exceptions
from reviews.models import User
from reviews.models import Category, Genre, Title
import datetime as dt
from reviews.models import Review, Comment
from rest_framework.relations import SlugRelatedField
from django.db.models import Avg
from rest_framework.validators import UniqueTogetherValidator
from django.shortcuts import get_object_or_404


class SignUpSerializer(serializers.ModelSerializer):
    def validate(self, data):
        if data['username'] == 'me':
            raise serializers.ValidationError('Пользователь с таким именем '
                                              'не допустим. Пожалуйста '
                                              'выберите другое имя.')
        return data

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role',
        )


class UserTokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    def validate(self, data):
        username = data['username']
        confirmation_code = data['confirmation_code']
        if not User.objects.filter(username=username).exists():
            raise exceptions.NotFound('Пользователь не найден.')
        elif not User.objects.filter(
            confirmation_code=confirmation_code
        ).exists():
            raise serializers.ValidationError('Неправильный код')
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role',
        )


class CategorySerializer(serializers.ModelSerializer):
    lookup_field = 'slug'

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    lookup_field = 'slug'

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        required=False,
        many=True,
        slug_field='slug'
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        required=False,
        slug_field='slug',
    )
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating',
            'description', 'category', 'genre')

    def get_rating(self, obj):
        rating = obj.reviews.all().aggregate(Avg('score'))['score__avg']
        return rating

    def validate_year(self, value):
        thisyear = dt.date.today().year
        if not (0 <= int(value) <= thisyear):
            raise serializers.ValidationError(
                'Проверьте год, он должен быть в пределах '
                f'0 - {thisyear}')
        return value


class TitleSerializerView(TitleSerializer):
    genre = GenreSerializer(
        required=False,
        many=True,
    )
    category = CategorySerializer(
        required=False,
    )


class CurrentTitleDafault:
    requires_context = True

    def __call__(self, serializer_field):
        c_view = serializer_field.context['view']
        title_id = c_view.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        return title

    def __repr__(self):
        return f'{self.__class__.__name__}()'


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        slug_field='username',
        read_only=True)
    title = serializers.HiddenField(default=CurrentTitleDafault())

    class Meta:
        model = Review
        read_only_fields = ('author',)
        fields = ('id', 'text', 'author', 'score', 'pub_date', 'title')

        validators = (
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('author', 'title')
            ),
        )


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Comment
        read_only_fields = ('author',)
        fields = ('id', 'text', 'author', 'pub_date')
