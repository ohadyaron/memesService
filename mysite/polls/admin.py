from django.contrib import admin

from .models import Question, Image, Mem

admin.site.register(Question)
admin.site.register(Image)
admin.site.register(Mem)
