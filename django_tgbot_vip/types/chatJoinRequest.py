from . import BasicType

from . import chat , user , chatmember , chatInviteLink

class ChatJoinRequest(BasicType):
    fields = {
        'user_chat_id' : int ,
        'date' : int ,
        'bio' : str ,
    }

    def __init__(self, obj=None):
        super(ChatJoinRequest, self).__init__(obj)

    def get_user(self):
        return getattr(self, 'from', None)

    def get_user_chat_id(self):
        return getattr(self, 'user_chat_id', None)
        
    def get_chat(self):
        return getattr(self, 'chat', None)

    def get_invite_link(self)  :
        return getattr(self, 'invite_link', None)



ChatJoinRequest.fields.update({
    'chat': chat.Chat , 
    'from' : user.User ,
    'invite_link' : chatInviteLink.ChatInviteLink ,
})