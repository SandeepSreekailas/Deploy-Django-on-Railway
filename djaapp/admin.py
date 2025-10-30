from django.contrib import admin
from .models import Book

# Register your models here.

class ModelAdminBook(admin.ModelAdmin):

    list_display=('name','author','description','price')

    actions = ['mark_free']

    def mark_free(self, request, queryset):
        queryset.update(price=0)
        self.message_user(request, "books marked as free")
    mark_free.short_description = "Mark selected books as free"


admin.site.register(Book, ModelAdminBook)