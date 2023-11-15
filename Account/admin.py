from django.contrib import admin
from Account.models import *
# Register your models here.
admin.site.register(PeopleModel)
admin.site.register(WordsModel)
admin.site.register(MessageModel)

# @admin.register(WordsModel)
# class Verses(admin.ModelAdmin):
#     list_display = ( "Number" ,"Persian" , "English" )
#     search_fields = ('Number','Persian')
#     list_per_page = 50
    