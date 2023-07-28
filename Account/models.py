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
    Read = models.JSONField(verbose_name="آیه های خوانده شده", null = True , default=dict )
    Read.help_text = {
                "R_qoran":{
                            "number" : 0 ,
                            "numbers" : [] ,
                            "favnumbers" : [] ,
                        },
    }

    ReadDetails = models.JSONField(verbose_name="جزییات خوانده شده ها", null = True , default=dict )
    ReadDetails.help_text={
        "d_qoran":{
                    "start" : [] ,
                    "end" : [] ,
                    "count" : 0 ,
                },
    }
    
    DailyRead = models.IntegerField( verbose_name="تعداد آیه در روز" , null=True )
    Chatid = models.CharField(max_length=30,verbose_name="چت ایدی", blank=True , null= True )


    persian = 1
    arabic = 2
    english = 3

    StatusActiveChoice =((persian,"فارسی"),
                (arabic,"عربی"),
                (english,"انگلیسی"))

    Lang = models.IntegerField(choices=StatusActiveChoice , verbose_name="زبان", default= 1 , null= False) 
    

    def ReadNumber(self):
        return self.Read["R_qoran"]["number"]

    def ReadList(self):
        return self.Read["R_qoran"]["numbers"]

    def addRead(self ):
        self.Read["R_qoran"]["number"] += 1
        self.Read["R_qoran"]["numbers"].append( self.Read["R_qoran"]["number"] )
        self.save()
    
    def addFavRead(self , number ):
        self.Read["R_qoran"]["favnumbers"].append(number)
        self.save()
        

class VersesModel(models.Model):
    class Meta:
        verbose_name="آیه"
        verbose_name_plural="آیه ها"

    Number = models.IntegerField( verbose_name="شماره آیه" , null=True )
    Persian = models.TextField(max_length=2000, verbose_name="فارسی",null= True)
    English = models.TextField(max_length=2000, verbose_name="انگلیسی",null= True)
    Arabic = models.TextField(max_length=2000, verbose_name="عربی",null= True)
    Soreh = models.TextField(max_length=100, verbose_name="سوره",null= True)
    Jose = models.TextField(max_length=100, verbose_name="جز",null= True)
    Voice = models.ImageField(upload_to = "Voice/", verbose_name="صوت" , null= True , blank = True , validators =[validate_file_extension,validate_file_size] )

    def __str__(self) -> str:
        return self.Number  

class MessageModel(models.Model):
    class Meta:
        verbose_name="پیام"
        verbose_name_plural="پیام ها"

    One = models.TextField(max_length=2000, verbose_name="متن اول",null= True)
    Two = models.TextField(max_length=2000, verbose_name="متن دوم",null= True)
    

