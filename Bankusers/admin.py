from django.contrib import admin
from .models import Boss
# Register your models here.
@admin.register(Boss)
class BossAdmin(admin.ModelAdmin):
    list_display = ('first_name','last_name','username','email','code_meli','phone_number')
    search_fields = ( 'first_name','last_name','username','email')
    {
        "first_name":"parsa",
        "last_name":"hashemian",
        "username":"parsa",
        "code_meli":"0250021031",
        "email":"parsahashemian@gmail.com",
        "phone_number":"1234312311",
        "password":"parsa1234"

    }