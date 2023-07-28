from django.contrib import admin
from Account.models import *
# Register your models here.
admin.site.register(PeopleModel)
# admin.site.register(VersesModel)
admin.site.register(MessageModel)

@admin.register(VersesModel)
class Verses(admin.ModelAdmin):
    list_display = ( "Number" ,"Persian" , "English" , "Arabic" , "Soreh" , "Jose" )
    search_fields = ('Number' , 'Arabic','Persian')
    list_filter = ( 
        'Jose',)
    list_per_page = 50
    