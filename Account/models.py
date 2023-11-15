from django.db import models 
import uuid
from django.contrib.auth.models import User
from Account.validators import validate_file_size , validate_file_extension

# Create your models here.

class PeopleModel(models.Model):
    class Meta:
        verbose_name="کاربر"
        verbose_name_plural="کاربران"
    
    Uuid = models.UUIDField(default=uuid.uuid4 , unique= True , editable=False)
    People = models.OneToOneField(User,on_delete=models.CASCADE,verbose_name="کاربری",related_name="people")
    Read = models.JSONField(verbose_name="کلمات خوانده شده", null = True , default=dict )
    Read.help_text = {
    "R_words": {
    "number": 0,
    "numbers": [],
    "favnumbers": []
  }
}

    ReadDetails = models.JSONField(verbose_name="جزییات خوانده شده ها", null = True , default=dict )
    ReadDetails.help_text={
        "d_words":{
                    "start" : [] ,
                    "end" : [] ,
                    "count" : 0 ,
                },
    }
    
    DailyRead = models.IntegerField( verbose_name="تعداد کلمه در روز" , null=True )
    Chatid = models.CharField(max_length=30,verbose_name="چت ایدی", blank=True , null= True )


 
    

    def ReadNumber(self):
        return self.Read["R_words"]["number"]

    def ReadList(self):
        return self.Read["R_words"]["numbers"]

    def addRead(self , number ):
        self.Read["R_words"]["number"] += 1
        self.Read["R_words"]["numbers"].append( number )
        self.save()
    
    def addFavRead(self , number ):
        self.Read["R_words"]["favnumbers"].append(number)
        self.save()
        

class WordsModel(models.Model):
    class Meta:
        verbose_name="کلمه"
        verbose_name_plural="کلمه ها"

    Number = models.IntegerField( verbose_name="شماره کلمه" , null=True )
    Persian = models.TextField(max_length=2000, verbose_name="فارسی",null= True)
    English = models.TextField(max_length=2000, verbose_name="انگلیسی",null= True)
    ExampleEN = models.TextField(max_length=2000, verbose_name="مثال انگلیسی",null= True)
    ExampleFA = models.TextField(max_length=2000, verbose_name="مثال فارسی",null= True)

    Voice = models.ImageField(upload_to = "Voice/", verbose_name="صوت" , null= True , blank = True , validators =[validate_file_extension,validate_file_size] )

    def __str__(self) -> str:
        return str(self.English)

class MessageModel(models.Model):
    class Meta:
        verbose_name="پیام"
        verbose_name_plural="پیام ها"

    One = models.TextField(max_length=2000, verbose_name="متن اول",null= True)
    Two = models.TextField(max_length=2000, verbose_name="متن دوم",null= True)
    

