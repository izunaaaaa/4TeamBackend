from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Letterlist, Letter


# Register your models here.
@admin.register(Letterlist)
class LetterListAdmin(admin.ModelAdmin):
    list_display = ("pk", "users_list",)


@admin.register(Letter)
class LetterAdmin(admin.ModelAdmin):
    list_display = ("sender","text",)
