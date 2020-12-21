from django.contrib import admin


from .forms import User


class UserAdmin(admin.ModelAdmin):
    list_filter = ('email', 'first_name',)
