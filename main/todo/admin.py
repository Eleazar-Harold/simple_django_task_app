from django.contrib import admin
from main.todo.models import Todo

# Register your models here.
@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ['description', 'taskdate', 'started',
                    'complete', 'expire', 'created', 'updated', ]
