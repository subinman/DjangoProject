from django.contrib import admin
from news.models import News
from tinymce.widgets import TinyMCE
from django.db import models

class NewsAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
    }

admin.site.register(News, NewsAdmin)
