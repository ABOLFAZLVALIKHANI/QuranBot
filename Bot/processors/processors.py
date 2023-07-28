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
from Account.models import *


keboard_delete = ReplyKeyboardRemove.a(
    remove_keyboard = True
)
keboard_people =ReplyKeyboardMarkup.a(
            one_time_keyboard=True,
            resize_keyboard=True,
            keyboard=[
                [KeyboardButton.a('دریافت آیه جدید'),KeyboardButton.a('دریافت آیه رندم')],
                [KeyboardButton.a('مشاهده علاقمندی ها'),KeyboardButton.a('تنظیم تعداد آیه در روز')],
                [ KeyboardButton.a('جستجوی یک سوره')],
                [KeyboardButton.a('دعوت دوست'), KeyboardButton.a('درباره ربات')],
            ]
        ) 



@processor(state_manager, from_states=None ,fail=state_types.Keep )
def hello_world(bot: TelegramBot, update: Update, state: TelegramState):
    try:
        text = update.get_message().get_text()
        # bot.sendMessage(update.get_chat().get_id(), text)
        chatid = update.get_chat().get_id() 
        
        bot.sendMessage(chatid , "خوش آمدید، من روزانه تعدادی آیه برای شما ارسال میکنم که بخوانید، روزی چند آیه؟ شما به من بگویید"
                        , reply_markup= keboard_people )

        if not PeopleModel.objects.filter(Chatid = chatid ).exists():
            uid = uuid.uuid4()
            if PeopleModel.objects.filter(Uuid = uid ).exists():
                uid = uuid.uuid5(uid , "AbolfazlBots" )
            a= {
                "d_qoran":{
                            "start" : [] ,
                            "end" : [] ,
                            "count" : 0 ,
                        },
            }
            b = {
                "R_qoran":{
                            "number" : 0 ,
                            "numbers" : [] ,
                        },
            }

            PeopleModel.objects.create(Chatid = chatid , ReadDetails = a , DailyRead = 3 , Uuid = uid )
        
        state.name = "pe-"
        
    except:
        pass

    state.save()



@processor(state_manager, from_states=state_types.All,fail=state_types.Keep  , update_types= update_types.MyChatMember )
def change_bot_permision(bot: TelegramBot, update: Update, state: TelegramState):
    chatid_channel = update.get_my_chat_member().get_chat().get_id()
    title_channel = update.get_my_chat_member().get_chat().get_title()
    user_id = update.get_my_chat_member().get_user().get_id()
    status = update.get_my_chat_member().get_new_chat_member().get_status()
    status_old = update.get_my_chat_member().get_old_chat_member().get_status()

    print("saaaaaaaaalaaaaaaaaaam delbar ")
    print( status_old + "->" + status )

    if status_old  in [ "left" , "kicked" ]  and status == "administrator" :
        pass 
    elif status == "administrator" :
        try:
            t="برای مدیریت اشتراک کاربران، نیاز به دسترسی های لازم داریم، لطفا به ربات در کانالتان اجازه اضافه کردن کاربران را بدهید"
            bot.sendMessage(a.chatid ,t,reply_markup=ReplyKeyboardMarkup.a(
                            one_time_keyboard=True,
                            resize_keyboard=True,
                            keyboard= keboard_analyzer
                            ) 
                        ) 
        except:
            pass 
    elif status_old == "member" and status == "kicked" : # کاربر ربات را متوقف میکند
        print("man injam")
    elif status_old == "kicked" and status == "member" : # کاربر ربات را دوباره ران میکند 
        pass # خوش برگشتی، دفعه بعد با ملایمت باهام برخورد کن من ناراحت میشم:)
    

@processor(state_manager, from_states="pe-" ,fail=state_types.Keep )
def panel_people(bot: TelegramBot, update: Update, state: TelegramState):
    try:
        text = update.get_message().get_text()
        chatid = update.get_chat().get_id() 
        people = PeopleModel.objects.get(Chatid = chatid )
        bot.sendMessage(chatid , "خوش آمدید، من روزانه تعدادی آیه برای شما ارسال میکنم که بخوانید، روزی چند آیه؟ شما به من بگویید"
                        , reply_markup= keboard_people )
                        
        if text == "دریافت آیه جدید" :
            v = VersesModel.objects.get(Number = people.ReadNumber() + 1 )
            people.addRead()
            text = f"""بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ 
{v.Arabic}

فارسی:
{v.Persian}
            
            """
            bot.sendMessage(chatid ,text 
                        , reply_markup=InlineKeyboardMarkup.a(
                                    inline_keyboard = [
                                        [InlineKeyboardButton.a('افزودن به علاقمندی' 
                                                        , url=f"https://t.me/sicheckbot?start=fav-{v.Number}" )],
                                        [InlineKeyboardButton.a('اشتراک گذاری' 
                                                        ,switch_inline_query="Shared message" )],
                                    ]
                                )
                                
                        )

        elif text == "دریافت آیه رندم" :
            bot.sendMessage(chatid , "این بخش به زودی فعال خواهد شد")   

        elif text == "مشاهده علاقمندی ها" :
            bot.sendMessage(chatid , "این بخش به زودی فعال خواهد شد")   
    

        elif text == "تنظیم تعداد آیه در روز" :
            bot.sendMessage(chatid , "این بخش به زودی فعال خواهد شد")   
            
        elif text == "دعوت دوست" :
            bot.sendMessage(chatid , "این بخش به زودی فعال خواهد شد") 
        elif text == "درباره ربات" :
            bot.sendMessage(chatid , "این بخش به زودی فعال خواهد شد") 
        elif text == "جستجوی یک سوره" :
            bot.sendMessage(chatid , "این بخش به زودی فعال خواهد شد")     
        
        state.name = "pe-"
        
    except:
        pass

    state.save()



    
@processor(state_manager, from_states=state_types.All )
def add_to_fav(bot: TelegramBot, update: Update, state: TelegramState):
    text = update.get_message().get_text()

    text= str(text[text.find(" ") + 1 :])
    chatid = update.get_chat().get_id() 

    if text.startswith("fav-"):
        try:
            people = PeopleModel.objects.get(Chatid = chatid )
        except:
            return None
        
        number = int(text[5:])
        if number < 6236 :
            people.addFavRead(number)
        else:
            text = "آیه یافت نشد"

        text = "آیه به لیست علاقمندی های شما اضافه شد"

        bot.sendMessage(chatid , text , reply_markup= keboard_people)