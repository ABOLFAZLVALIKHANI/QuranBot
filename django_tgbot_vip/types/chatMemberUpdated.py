from . import BasicType


class ChatMemberUpdated(BasicType):
    fields = {
        'date' : int
    }

    def __init__(self, obj=None):
        super(ChatMemberUpdated, self).__init__(obj)

    def get_user(self):
        return getattr(self, 'from', None)

    def get_chat(self):
        return getattr(self, 'chat', None)
    
    def get_old_chat_member(self):
        return getattr(self, 'old_chat_member', None)

    def get_new_chat_member(self):
        return getattr(self, 'new_chat_member', None)
        

from . import chat , user , chatmember , chatInviteLink

ChatMemberUpdated.fields.update({
    'chat': chat.Chat , 
    'from' : user.User ,
    'old_chat_member' : chatmember.ChatMember ,
    'new_chat_member' : chatmember.ChatMember ,
    'invite_link' : chatInviteLink.ChatInviteLink ,
})