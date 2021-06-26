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
        self.user_id = user_id
        self.name = name
        self._message_count = 0
        self._likes_given = {}
        self._likes_received = {}

    # Getter property method for the user_id field
    @property
    def user_id(self):
        return self._user_id

    # Setter property method for the user_id field
    @user_id.setter
    def user_id(self, id):
        if isinstance(id, int):
            self._user_id = id
        else:
            print('The user id should be an int! Please try again.')

    # Getter property method for the name field
    @property
    def name(self):
        return self._name

    # Setter property method for the name field
    @name.setter
    def name(self, new_name):
        if isinstance(new_name, str):
            self._name = new_name
        else:
            print('The user id should be a str! Please try again.')
    
    # Getter property method for the message_count field
    @property
    def message_count(self):
        return self._message_count

    # Getter property method for the likes_given field
    @property
    def likes_given(self):
        return self._likes_given

    # Getter property method for the likes_received field
    @property
    def likes_received(self):
        return self._likes_received

    def add_message(self):
        """Increment the message_count field by one.
        """
        self._message_count += 1

    def add_like_given(self, recipient_id):
        """Add a 'like' given to the receiving user's entry in the likes
        given dictionary.
        """
        if recipient_id not in self.likes_given:
            self._likes_given[recipient_id] = 1
        else:
            self._likes_given[recipient_id] += 1

    def add_like_received(self, liker_id):
        """Add a 'like' received from the giver in this user's likes given dictionary.
        """
        if liker_id not in self.likes_received:
            self._likes_received[liker_id] = 1
        else:
            self._likes_received[liker_id] += 1

    def total_likes_given(self):
        """Find the total number of likes given while a member of this group chat.
        """
        # Set variable
        likes = 0

        # Get a dict_keys object so we can check the number of entries
        key_list = self.likes_given.keys()

        # If the user has given likes, sum all of them up
        if len(key_list) != 0:
            for user_id in key_list:
                likes += self.likes_given[user_id]

        return likes

    def total_likes_received(self):
        """Find the total number of likes received while a member of this group chat.
        """
        # Set variable
        likes = 0

        # Get a dict_keys object so we can check the number of entries
        key_list = self.likes_received.keys()

        # If the user has received likes, sum all of them up
        if len(key_list) != 0:
            for user_id in key_list:
                likes += self.likes_received[user_id]

        return likes

    # Define built-in object methods

    def __str__(self):
        return f'{self.name}'

    def __repr__(self):
        repr_str = (f"group_member.GroupMember({self.user_id}, '{self.name}',"
                    f" {self.message_count}, {self.total_likes_given()}, {self.total_likes_received()})")
        return repr_str