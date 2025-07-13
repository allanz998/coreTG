 
from unfold.admin import ModelAdmin as UnfoldModelAdmin
from .models import File
from django.contrib import admin

@admin.register(File)
class FileAdmin(UnfoldModelAdmin):
    list_display = ('name', 'path', 'description', 'sent', 'date')
    search_fields = ('name', 'path', 'description')
    list_filter = ('sent', 'date')
    ordering = ('-date',)
    date_hierarchy = 'date' 

