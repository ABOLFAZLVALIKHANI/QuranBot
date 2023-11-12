from django.contrib import admin
from .models import *

# Register your models here.

# @admin.register(SabtenamModel)
# class sabtenam(admin.ModelAdmin):
#     list_display = ("mobile",
#                     "chatid",
#                     "type",
#                     "refral_code")
#     search_fields = ("mobile",
#                     "chatid")
    


# admin.site.register(DarafSignalModel)
admin.site.register(TelegramState)
