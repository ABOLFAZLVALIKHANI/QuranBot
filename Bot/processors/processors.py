from django_tgbot_vip.decorators import processor
from django_tgbot_vip.state_manager import message_types, update_types, state_types
from django_tgbot_vip.types.update import Update
from ..bot import state_manager
from ..models import TelegramState
from ..bot import TelegramBot

from django_tgbot_vip.types.replykeyboardmarkup import ReplyKeyboardMarkup
from django_tgbot_vip.types.keyboardbutton import KeyboardButton 
from django_tgbot_vip.types.replykeyboardremove import ReplyKeyboardRemove
from django_tgbot_vip.types.inlinekeyboardmarkup import InlineKeyboardMarkup
from django_tgbot_vip.types.inlinekeyboardbutton import InlineKeyboardButton
from Account.models import PeopleModel , WordsModel , MessageModel
from django.contrib.auth.models import User
from Bot.credentials import APP_NAME , admin_chati_id
import uuid 
from django.core.exceptions import ObjectDoesNotExist

keboard_delete = ReplyKeyboardRemove.a(
    remove_keyboard = True
)
keboard_people =ReplyKeyboardMarkup.a(
            one_time_keyboard=True,
            resize_keyboard=True,
            keyboard=[
                [KeyboardButton.a("دریافت کلمه جدید"),KeyboardButton.a('دریافت کلمه رندم')],
                [KeyboardButton.a('مشاهده علاقمندی ها'),KeyboardButton.a('تنظیم تعداد کلمه در روز')],
                [ KeyboardButton.a('جستجوی یک سوره')],
                [KeyboardButton.a('دعوت دوست'), KeyboardButton.a('درباره ربات')],
            ]
        ) 

"دریافت 10 کلمه بعدی"

keboard_admin = ReplyKeyboardMarkup.a(
            one_time_keyboard=True,
            resize_keyboard=True,
            keyboard=[
                [KeyboardButton.a("دریافت کلمه جدید"),KeyboardButton.a('دریافت کلمه رندم')],
                [KeyboardButton.a('مشاهده علاقمندی ها'),KeyboardButton.a('تنظیم تعداد کلمه در روز')],
                [KeyboardButton.a('جستجوی یک سوره')],
                [KeyboardButton.a('پیغام به همه')],
            ]
        ) 

keboard_choice =ReplyKeyboardMarkup.a(
            one_time_keyboard=True,
            resize_keyboard=True,
            keyboard=[
                [KeyboardButton.a('1'),KeyboardButton.a('2'),KeyboardButton.a('3')],
                [KeyboardButton.a('4'),KeyboardButton.a('5'),KeyboardButton.a('6')],
                [KeyboardButton.a('7'),KeyboardButton.a('8'),KeyboardButton.a('9')],
                [KeyboardButton.a('10'),KeyboardButton.a('11'),KeyboardButton.a('12')],
            ]
        ) 


@processor(state_manager, from_states=None ,fail=state_types.Keep )
def hello_world(bot: TelegramBot, update: Update, state: TelegramState):
    try:
        text = update.get_message().get_text()
        # bot.sendMessage(update.get_chat().get_id(), text)   
        chatid = update.get_chat().get_id() 

        bot.sendMessage(chatid , "خوش آمدید، من روزانه تعدادی کلمه برای شما ارسال میکنم که بخوانید، روزی چند کلمه؟ شما به من بگویید"
                        , reply_markup= keboard_choice )

        if not PeopleModel.objects.filter(Chatid = chatid ).exists():
            print('53')
            uid = uuid.uuid4()
            if PeopleModel.objects.filter(Uuid = uid ).exists():
                uid = uuid.uuid5(uid , "AbolfazlBots" )
            a= {
                "d_words":{
                            "start" : [] ,
                            "end" : [] ,
                            "count" : 0 ,
                        },
            }
            b = {
                "R_words":{
                            "number" : 0 ,
                            "numbers" : [] ,
                            "favnumbers" : [] ,
                        },
            }
            us = User.objects.create(username = chatid)
            us.set_password(chatid)
            us.save()
            PeopleModel.objects.create(Chatid = chatid , People = us  ,Read = b ,  ReadDetails = a , DailyRead = 3 , Uuid = uid  )
        
        state.name = "choice-daily-read"

            
        
    except Exception as e : 
        bot.sendMessage(update.get_chat().get_id(), e )  

    state.save()



# @processor(state_manager, from_states=state_types.All,fail=state_types.Keep  , update_types= update_types.MyChatMember )
# def change_bot_permision(bot: TelegramBot, update: Update, state: TelegramState):
#     chatid_channel = update.get_my_chat_member().get_chat().get_id()
#     title_channel = update.get_my_chat_member().get_chat().get_title()
#     user_id = update.get_my_chat_member().get_user().get_id()
#     status = update.get_my_chat_member().get_new_chat_member().get_status()
#     status_old = update.get_my_chat_member().get_old_chat_member().get_status()

#     # print("saaaaaaaaalaaaaaaaaaam delbar ")
#     # print( status_old + "->" + status )

#     if status_old  in [ "left" , "kicked" ]  and status == "administrator" :
#         pass 
#     elif status == "administrator" :
#         try:
#             t="برای مدیریت اشتراک کاربران، نیاز به دسترسی های لازم داریم، لطفا به ربات در کانالتان اجازه اضافه کردن کاربران را بدهید"
#             bot.sendMessage(a.chatid ,t,reply_markup=ReplyKeyboardMarkup.a(
#                             one_time_keyboard=True,
#                             resize_keyboard=True,
#                             keyboard= keboard_analyzer
#                             ) 
#                         ) 
#         except:
#             pass 
#     elif status_old == "member" and status == "kicked" : # کاربر ربات را متوقف میکند
#         print("man injam")
#     elif status_old == "kicked" and status == "member" : # کاربر ربات را دوباره ران میکند 
#         pass # خوش برگشتی، دفعه بعد با ملایمت باهام برخورد کن من ناراحت میشم:)
    



@processor(state_manager, from_states="choice-daily-read" ,fail=state_types.Keep )
def panel_people(bot: TelegramBot, update: Update, state: TelegramState):
    try:
        text = int(update.get_message().get_text())
        chatid = update.get_chat().get_id() 
        people = PeopleModel.objects.get(Chatid = chatid )
        people.DailyRead = int(text) 
        people.save()
        bot.sendMessage(chat_id= chatid , text= "تنظیم شد. از این پس من هر روز راس ساعت ۲۱:۰۰ برای تو همین تعداد کلمه جدید و ارسال میکنم" , reply_markup = keboard_people )
        state.name = 'pe-'

    except Exception as e :
        bot.sendMessage(chat_id= update.get_chat().get_id()  , text= f"error > { e }" , reply_markup = keboard_people )

    state.save()
    


@processor(state_manager, from_states="pe-" ,fail=state_types.Keep )
def panel_people(bot: TelegramBot, update: Update, state: TelegramState):
    chatid = update.get_chat().get_id() 

    if chatid not in admin_chati_id:
        try:
            text = update.get_message().get_text()
            chatid = update.get_chat().get_id() 
            people = PeopleModel.objects.get(Chatid = chatid )
            
            # bot.sendMessage(chatid , "ربات در خدمت شماست"
            #                 , reply_markup= keboard_people )

            if text in ["دریافت کلمه جدید" , "/next" , "next"] :
                number = people.ReadNumber() # این تابع میگه الان کدوم ایه هستش
                v = WordsModel.objects.get(Number = number + 1 )
                # print('149')
                people.addRead( number + 1 )
                text = f"""{ v.Number } - {v.English}
{v.Persian}
{ v.ExampleEN }
{ v.ExampleFA }
------------
"""

                
                bot.sendMessage(chatid ,text 
                            , reply_markup=InlineKeyboardMarkup.a(
                                        inline_keyboard = [
                                            [InlineKeyboardButton.a('افزودن به علاقمندی' 
                                                            , url=f"https://t.me/{APP_NAME}?start=fav-{v.Number}" )],
                                            [InlineKeyboardButton.a('اشتراک گذاری' 
                                                            ,switch_inline_query=text)],
                                            
                                        ]
                                    )
                                    
                            )

                state.name = "pe-"

            elif text == "دریافت کلمه رندم" :
                bot.sendMessage(chatid , "این بخش به زودی فعال خواهد شد" , reply_markup = keboard_people ) 
                state.name = "pe-"


            elif text == "مشاهده علاقمندی ها" :
                bot.sendMessage(chatid , "این بخش به زودی فعال خواهد شد" , reply_markup = keboard_people )  
                state.name = "pe-"

            elif text == "تنظیم تعداد کلمه در روز" :
                bot.sendMessage(chatid , 'بسیار خب ،انتخاب کنید'  , reply_markup= keboard_choice )  
                state.name = "choice-daily-read" 
                
            elif text == "دعوت دوست" :
                bot.sendMessage(chatid , "این بخش به زودی فعال خواهد شد" , reply_markup = keboard_people )
                state.name = "pe-"

            elif text == "درباره ربات" :
                bot.sendMessage(chatid , "این بخش به زودی فعال خواهد شد" , reply_markup = keboard_people )
                state.name = "pe-"

            elif text == "جستجوی یک سوره" :
                bot.sendMessage(chatid , "این بخش به زودی فعال خواهد شد" , reply_markup = keboard_people )
                state.name = "pe-"
            
            elif text == "دریافت 10 کلمه بعدی" :
                bot.sendMessage(chatid , "این بخش به زودی فعال خواهد شد" , reply_markup = keboard_admin ) 
                state.name = "ad-"

            
            
        except Exception as e : 
            bot.sendMessage(update.get_chat().get_id(), e )  
            
    else: # admin 
        bot.sendMessage(update.get_chat().get_id(),  'شما ادمین هستید' , reply_markup = keboard_admin )  
        state.name = "ad-"

    state.save()
    people.save()   




    
@processor(state_manager, from_states=state_types.All )
def manage_start_message(bot: TelegramBot, update: Update, state: TelegramState):
    try :
        text = update.get_message().get_text()

        text= str(text[text.find(" ") + 1 :])
        chatid = update.get_chat().get_id() 
        # bot.sendMessage(update.get_chat().get_id(), text)   

        if text.startswith("fav-"):
            try:
                people = PeopleModel.objects.get(Chatid = chatid )
                number = int(text[4:])
                
                if number < 6236 :
                    people.addFavRead(number)
                else:
                    text = "کلمه یافت نشد"

                text = "کلمه به لیست علاقمندی های شما اضافه شد"

                bot.sendMessage(chatid , text , reply_markup= keboard_people)
                
            except ObjectDoesNotExist :
                state.name = None
                state.save()
            
            

        elif text.startswith("back"):
            try:
                people = PeopleModel.objects.get(Chatid = chatid )
                if chatid not in admin_chati_id :
                    bot.sendMessage(chatid , "بازگشت به منو اصلی" , reply_markup= keboard_people)
                else:
                    bot.sendMessage(chatid , "بازگشت به منو ادمین" , reply_markup= keboard_admin)
            except:
                state.name = None
                state.save()
    except:
        pass