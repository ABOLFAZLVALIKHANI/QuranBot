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
from Bot.credentials import APP_NAME ,admin_chati_id
import uuid 
from django.core.exceptions import ObjectDoesNotExist
from .processors import keboard_admin , keboard_choice

def send_to_all_user(message : str , bot : TelegramBot ):
    # people = 
    for p in PeopleModel.objects.all() :
        bot.sendMessage( chat_id= p.Chatid , text= message  )

    return True


@processor(state_manager, from_states='message_to_all' ,fail=state_types.Keep )
def admin_panel(bot: TelegramBot, update: Update, state: TelegramState):
    chatid = update.get_chat().get_id()  
    text = update.get_message().get_text()
    try:
        bot.sendMessage(chat_id= chatid , text= "پیام شما رفت برای ارسال ممکن است کمی زمان ببرد")
        if send_to_all_user(text , bot ):
            pass
        else:
            pass
        bot.sendMessage(chat_id= chatid , text= "پیغام برای همه ارسال شد" , reply_markup= keboard_admin)
    except Exception as e :
        bot.sendMessage(chat_id= chatid , text= e, reply_markup= keboard_admin)

    state.name = 'ad-'
    state.save()

@processor(state_manager, from_states='ad-' ,fail=state_types.Keep )
def admin_panel(bot: TelegramBot, update: Update, state: TelegramState):
    chatid = update.get_chat().get_id()  

    if chatid in admin_chati_id :
        try:
            text = update.get_message().get_text()
            # chatid = update.get_chat().get_id() 
            people = PeopleModel.objects.get(Chatid = chatid )
            
            # bot.sendMessage(chatid , "ربات در خدمت شماست"
            #                 , reply_markup= keboard_admin )

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
بعدی: /next
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

                state.name = "ad-"

            elif text == "دریافت کلمه رندم" :
                import random
                number = random.choice(people.ReadList())
                v = WordsModel.objects.get(Number = number )
                
                text = f""" { v.Number } - {v.English}
<span class="tg-spoiler"> 
{v.Persian}
</span>
{ v.ExampleEN }
<span class="tg-spoiler"> 
{ v.ExampleFA }
</span>

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
                                    
                            , parse_mode="HTML" )



                state.name = "ad-"

            elif text == "دریافت 10 کلمه بعدی" :
                bot.sendMessage(chatid , "این بخش به زودی فعال خواهد شد" , reply_markup = keboard_admin ) 
                state.name = "ad-"

            elif text == "مشاهده علاقمندی ها" :
                bot.sendMessage(chatid , "این بخش به زودی فعال خواهد شد" , reply_markup = keboard_admin )  
                state.name = "ad-"

            elif text == "تنظیم تعداد کلمه در روز" :
                bot.sendMessage(chatid , 'بسیار خب ،انتخاب کنید'  , reply_markup= keboard_choice )  
                state.name = "choice-daily-read" 
                
            elif text == "دعوت دوست" :
                bot.sendMessage(chatid , "این بخش به زودی فعال خواهد شد" , reply_markup = keboard_admin )
                state.name = "ad-"

            
            elif text == "جستجوی یک سوره" :
                bot.sendMessage(chatid , "این بخش به زودی فعال خواهد شد" , reply_markup = keboard_admin )
                state.name = "ad-"

            elif text == 'پیغام به همه':
                bot.sendMessage(chatid , "پیغام خود را وارد کنید (فعلا فقط متن) ادمین جان" , reply_markup = keboard_admin )
                state.name = "message_to_all"


            
            
        except Exception as e : 
            bot.sendMessage(update.get_chat().get_id(), e ) 


    else:
        state.name='pe'

    state.save()
