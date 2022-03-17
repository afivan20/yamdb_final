from rest_framework import status, viewsets, filters, generics, mixins
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from api.permissions import (
    IsAdminModeratorAuthorOrReadOnly,
    IsAdminUserOrReadOnlyGenCat,
    IsAdmin
)
from reviews.models import User, Category, Genre, Title, Comment, Review
from api.serializers import (
    SignUpSerializer, UserTokenSerializer, UserSerializer,
    CategorySerializer, GenreSerializer,
    TitleSerializer, TitleSerializerView,
    ReviewSerializer, CommentSerializer
)
from api.filters import GenreFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from uuid import uuid1
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail


class HTTPMethod:
    GET = 'get'
    PATCH = 'patch'
    DELETE = 'delete'
    POST = 'post'


class SignUpView(APIView):
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data['email']
        username = serializer.data['username']
        code = str(uuid1())
        User.objects.create(
            username=username,
            email=email,
            confirmation_code=code
        )
        send_mail(
            'Confirmation code',
            f'Используйте этот код для входа в учетную запись - {code}',
            'admin@yamdb.com',
            [email],
            fail_silently=False,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class TokenView(APIView):
    def post(self, request):
        serializer = UserTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.data['username']
        user = get_object_or_404(User, username=username)
        refresh = RefreshToken.for_user(user)
        return Response(
            {'access': str(refresh.access_token)},
            status=status.HTTP_200_OK,
        )


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsAdmin)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('username',)
    lookup_field = 'username'
    pagination_class = PageNumberPagination

    @action(
        detail=False,
        methods=(HTTPMethod.GET, HTTPMethod.PATCH,),
        permission_classes=(IsAuthenticated,)
    )
    def me(self, request):
        serializer = UserSerializer(request.user,
                                    data=request.data,
                                    partial=True)

        if request.user.is_admin or request.user.is_moderator:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer.is_valid(raise_exception=True)
        serializer.save(role='user')
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryViewSet(mixins.CreateModelMixin,
                      mixins.ListModelMixin, viewsets.GenericViewSet):
    http_method_names = (HTTPMethod.GET, HTTPMethod.POST,)
    permission_classes = (IsAdminUserOrReadOnlyGenCat,)
    queryset = Category.objects.all()
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('name',)
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination


class GenreViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin, viewsets.GenericViewSet):
    http_method_names = [HTTPMethod.GET, HTTPMethod.POST]
    permission_classes = (IsAdminUserOrReadOnlyGenCat,)
    queryset = Genre.objects.all()
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('name',)
    serializer_class = GenreSerializer
    pagination_class = PageNumberPagination


class TitleViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminUserOrReadOnlyGenCat,)
    queryset = Title.objects.all()
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = GenreFilter
    ordering_fields = ('name', 'year')
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if (self.request.method == 'POST'
                or self.request.method == 'PATCH'
                or self.request.method == 'PUT'):
            return TitleSerializer
        return TitleSerializerView


class CategoriesDelete(generics.DestroyAPIView):
    lookup_field = 'slug'
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = (IsAdmin,)


class GenreDelete(generics.DestroyAPIView):
    lookup_field = 'slug'
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()
    permission_classes = (IsAdmin,)


class ReviewViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        queryset = Review.objects.all()
        title_id = self.kwargs.get('title_id')
        queryset = queryset.filter(title_id=title_id)
        return queryset
    serializer_class = ReviewSerializer
    permission_classes = (IsAdminModeratorAuthorOrReadOnly,)
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)

    def perform_update(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        queryset = Comment.objects.all()
        review_id = self.kwargs.get('review_id')
        queryset = queryset.filter(review_id=review_id)
        return queryset
    serializer_class = CommentSerializer
    permission_classes = (IsAdminModeratorAuthorOrReadOnly,)
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        serializer.save(author=self.request.user, review=review)

    def perform_update(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        serializer.save(author=self.request.user, review=review)
