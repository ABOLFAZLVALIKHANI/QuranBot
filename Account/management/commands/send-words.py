from django.conf import settings
from django.core.management.base import BaseCommand , CommandError

from django_tgbot_vip.management import helpers
from Account.models import PeopleModel , WordsModel
from Bot.bot import TelegramBot
from Bot.processors.processors import keboard_people
from django_tgbot_vip.bot_api_user import BotAPIUser
from Bot.credentials import BOT_TOKEN

class Command(BaseCommand):
    help = 'send Verses to user'

    def handle(self, *args, **options):
        try:
            for people in PeopleModel.objects.all() :
                DailyRead = people.DailyRead
                number = people.ReadNumber()
                numberList = people.ReadList()
                text = str()
                while DailyRead > 0 :
                    if number not in numberList :
                        v = WordsModel.objects.get( Number = number )
                    else:
                        number += 1
                        v = WordsModel.objects.get( Number = number )

                    text = text + f"""{ v.Number } - {v.English}
{v.Persian}
------------
{ v.ExampleEN }
{ v.ExampleFA }

"""              
                    people.addRead(number= number )
                    DailyRead -= 1 
                    number += 1
                    
                bot = BotAPIUser(BOT_TOKEN)
                bot.sendMessage( chat_id= people.Chatid , text= text , reply_markup= keboard_people )
                people.save()

        except Exception as e :
            raise CommandError(f'error for check portfo = {e}')
        
