from django.contrib import admin

# Register your models here.
from mptt.admin import DraggableMPTTAdmin

from book.models import Category, Book, Images, Comment


class BookImageInline(admin.TabularInline):
    model = Images
    extra = 5
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'image_tag']
    list_filter = ['status']
    readonly_fields = ('image_tag',)

class CategoryAdmin2(DraggableMPTTAdmin):
    mptt_indent_field = "title"
    list_display = ('tree_actions', 'indented_title',
                    'related_books_count', 'related_books_cumulative_count')
    list_display_links = ('indented_title',)
    prepopulated_fields = {'slug': ('title',)}

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative book count
        qs = Category.objects.add_related_count(
            qs,
            Book,
            'category',
            'books_cumulative_count',
            cumulative=True)

        # Add non cumulative book count
        qs = Category.objects.add_related_count(qs,
                                                Book,
                                                'category',
                                                'books_count',
                                                cumulative=False)
        return qs

    def related_books_count(self, instance):
        return instance.books_count

    related_books_count.short_description = 'Related books (for this specific category)'

    def related_books_cumulative_count(self, instance):
        return instance.books_cumulative_count

    related_books_cumulative_count.short_description = 'Related books (in tree)'
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'image_tag', 'status']
    readonly_fields = ('image_tag',)
    list_filter = ['status', 'category']
    inlines = [BookImageInline]
    prepopulated_fields = {'slug': ('title',)}
class ImagesAdmin(admin.ModelAdmin):
    list_display = ['title', 'book', 'image_tag']

class CommentAdmin(admin.ModelAdmin):
    list_display = ['subject', 'comment', 'book', 'user', 'status']
    list_filter = ['status']


admin.site.register(Category , CategoryAdmin2)
admin.site.register(Book, BookAdmin)
admin.site.register(Images, ImagesAdmin)
admin.site.register(Comment,CommentAdmin)