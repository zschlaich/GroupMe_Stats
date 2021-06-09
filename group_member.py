"""Class used to represent a member of a GroupMe groupchat.

GroupMe members have various attributes that we want to pay attention to.
For example, the name of a member, their user_id (so that we know who they)
are even when they change their nicknames, how many messages they've sent,
how many messages they've liked, how many likes received, etc.
"""

class GroupMember():
    """Class representation of a GroupMe group chat member.
    """
    
    # Initialize a GroupMember
    def __init__(self, user_id, name=''):
        self.__user_id = user_id
        self.__name = name
        self.__message_count = 0
        self.__likes_given = {}
        self.__likes_received = {}

    # Get methods for each of the class fields

    def get_user_id(self):
        return self.__user_id

    def get_name(self):
        return self.__name

    def get_message_count(self):
        return self.__message_count

    def get_likes_given(self):
        return self.__likes_given

    def get_likes_received(self):
        return self.__get_likes_received

    def add_message(self):
        self.__message_count += 1

    def add_like_given(self, recipient_id):
        """Add a 'like' given to the receiving user's entry in the likes
        given dictionary.
        """
        if recipient_id not in self.__likes_given:
            self.__likes_given[recipient_id] = 1
        else:
            self.__likes_given[recipient_id] += 1

    def add_like_received(self, liker_id):
        """Add a 'like' received from the giver in this user's likes given dictionary.
        """
        if liker_id not in self.__likes_given:
            self.__likes_given[liker_id] = 1
        else:
            self.__likes_given[liker_id] += 1