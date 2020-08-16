from django.contrib import admin

# Register your models here.
from book.models import Category, Book, Images, Comment


class BookImageInline(admin.TabularInline):
    model = Images
    extra = 5
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'image_tag']
    list_filter = ['status']
    readonly_fields = ('image_tag',)

class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'image_tag', 'status']
    readonly_fields = ('image_tag',)
    list_filter = ['status', 'category']
    inlines = [BookImageInline]
class ImagesAdmin(admin.ModelAdmin):
    list_display = ['title', 'book', 'image_tag']

class CommentAdmin(admin.ModelAdmin):
    list_display = ['subject', 'comment', 'book', 'user', 'status']
    list_filter = ['status']


admin.site.register(Category , CategoryAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Images, ImagesAdmin)
admin.site.register(Comment,CommentAdmin)