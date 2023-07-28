from django.core.exceptions import ValidationError
import os

def validate_file_size(value):
    filesize= value.size
    
    if filesize > 5242880:
        raise ValidationError(" ماکزیمم سایزی که می توانید آپلود کنید 5 مگابایت می باشد")
    else:
        return value


def validate_file_extension(value):
  ext = os.path.splitext(value.name)[1]
  valid_extensions = ['.jpg','.png','.PNG','.JPG','.Png','.Jpg','.pNG','.jPG', '.image' ,'.IMAGE' , '.jpeg' , '.JPEG' ]
  if not ext in valid_extensions:
    raise ValidationError(u'فرمت های مجاز : jpg و png!')
