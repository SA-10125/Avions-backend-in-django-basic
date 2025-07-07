from django.contrib import admin

#register your models here.

from .models import team_member, gallery_name, Blog

admin.site.register(team_member)
admin.site.register(gallery_name)
admin.site.register(Blog)
