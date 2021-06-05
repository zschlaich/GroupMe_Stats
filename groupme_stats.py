"""GroupMe Stats Finder

Script for gathering various portions of the GroupeMe API
"""

import requests, json, time

# Requests are of the form 'base_url/selection_parameters?token=ACCESS_TOKEN

# TODO:
# - Create a way for users to submit their access token through CLI
# - Create a way for users to pick which group they want to analyze through CLI

# The base url used for all calls to the GroupMe API
base_url = 'https://api.groupme.com/v3'
# Be sure to remove your access token before committing and pushing to Github!
access_token = ''
groupme_group_id = ''

def main():
    users_dict = create_users_dict()
    messages_dict = get_user_message_counts(users_dict)

    for user in messages_dict.keys():

        if user in users_dict.keys():
            print(f'User {users_dict[user]} has sent {messages_dict[user]:,} messages!')
        else:
            print(f'GroupMe {user} has sent {messages_dict[user]:,} messages!')

def create_users_dict():
    """Return a dictionary of user_ids and user names.
    
    This information is gathered using a GET request to the Groups/Show portion of the API.
    The request received contains information on the specific group included in the input
    parameter for the function.

    The dictionary returned is in the following format:\n
        {
            'user_id1' : 'First Last',
            'user_id2' : 'First Last',
            ...
        }
    """
    # create dict
    users = {}

    # TODO: change this to just include a passed in parameter that contains the group_id
    parameters = f'groups/{groupme_group_id}'

    # query API for group information, including user info
    r = requests.get(f'{base_url}/{parameters}?token={access_token}')
    request = r.json()

    # for each user dictionary grab information and store in main user dictionary
    for user_dict in request['response']['members']:
        user_id = user_dict['user_id']
        name = user_dict['name']
        users[user_id] = name
    
    # print(json.dumps(users, indent=4))
    return users

def get_user_message_counts(users):
    """Get a dictionary containing the number of messages sent by each group member.

    This information is gathered using a GET request to the Groups/:group_id/Messages portion
    of the API. The request receives 20 messages per query, so each batch is parsed for its
    message data and then another query is sent. To get older messages, the most recent
    message identification number is saved and used in the 'before_id' parameter for the next
    request query sent to the API.

    The dictionary returned is in the following format:\n
        {
            'user_id1' : 'message_count1',
            'user_id2' : 'message_count2',
            ...
        }
    """

    # Create a dictionary to store message counts
    message_counts = {}

    # Create the url_params value to be used in the API GET request
    url_params = f'groups/{groupme_group_id}/messages'

    # Get the first request
    r = requests.get(f'{base_url}/{url_params}?token={access_token}')
    request = r.json()

    # Get the total number of messages in the group
    total_messages = int(request['response']['count'])

    # Create a variable to track remaining messages
    remaining_messages = total_messages

    # Set queries value with the number of queries done. This information is tracked because you
    # can only send so many requests within a certain amount of time, or you will get an error.
    #queries = 1

    while remaining_messages > 0:
    #for _ in range(100):
        # For each message in the request response
        for message in request['response']['messages']:
            sender = message['sender_id']
            message_id = message['id']

            # add sender information to messsage_counts
            if sender not in message_counts:
                message_counts[sender] = 1
            else:
                message_counts[sender] += 1

        # Get the next set of messages if there is more than a batch left
        if remaining_messages >= 20:

            # Update the request params to include the last message id
            params = {
                'before_id' : f'{message_id}'
            }

            # Get next set of messages. In the event of a ConnectionError, wait for a cooldown
            # period and then try again
            try:
                r = requests.get(f'{base_url}/{url_params}?token={access_token}', params)
            except requests.exceptions.ConnectionError:
                time.sleep(60)
                r = requests.get(f'{base_url}/{url_params}?token={access_token}', params)

            request = r.json()

            # Decrement the number of messages left
            remaining_messages -= 20
            # Add number of queries done in this batch
            # queries += 1

            # if queries == 30:
            #     time.sleep(60)
            #     queries = 0

    #print(json.dumps(request, indent=4))
    return message_counts

if __name__ == "__main__":
    main()