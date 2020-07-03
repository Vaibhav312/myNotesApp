from django.contrib import admin
from blog.models import  User,ContactUsInfo,NotesInfo
# Register your models here.


admin.site.register(ContactUsInfo)
admin.site.register(NotesInfo)

