from django.contrib import admin
from .models import Boss
# Register your models here.
@admin.register(Boss)
class BossAdmin(admin.ModelAdmin):
    list_display = ('first_name','last_name','username','email','code_meli','phone_number','bank')
    search_fields = ( 'first_name','last_name','username','email')
