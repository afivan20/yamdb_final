from django.contrib import admin
from reviews.models import GenreTitle, User, Category, Genre, Title
from reviews.models import Review, Comment


class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'username', 'email', 'role')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    search_fields = ('name',)


class GenreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    search_fields = ('name',)


class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'year', 'description', 'category')
    search_fields = ('name',)
    list_filter = ('year',)
    empty_value_display = '-пусто-'


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'author', 'pub_date')
    search_fields = ('text',)
    empty_value_display = '-пусто-'


class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'author', 'pub_date')
    search_fields = ('text',)
    empty_value_display = '-пусто-'


class GenreTitleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title_id', 'genre_id')


admin.site.register(User, UserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(GenreTitle, GenreTitleAdmin)
