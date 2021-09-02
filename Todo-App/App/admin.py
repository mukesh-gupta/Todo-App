from django.contrib import admin

from .models import Todo

class TodoAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)
    list_display = ['id', 'user','title']

admin.site.register(Todo, TodoAdmin)
