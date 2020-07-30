from django.contrib import admin
from .models import Course1
# Register your models here.
#this class is created to view the date 
class UserAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)

admin.site.register(Course1,UserAdmin)