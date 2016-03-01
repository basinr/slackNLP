import sys
import time
import python_slackclient
import numpy as nump
import helper_functions
from python_slackclient.slackclient import SlackClient
from textblob import TextBlob


# Command line arguments
token = sys.argv[1]
user = sys.argv[2]

# found at https://api.slack.com/web#authentication
sc = SlackClient(token)

if sc.rtm_connect():

    im_lists =  sc.api_call(
    	"im.list"
    )

    channel_lists = sc.api_call(
        "channels.list"
    )

    # channel_convs = sc.api_call(
    #     "channels.history", channel="C08516EL8")


    helper_functions.driver(im_lists, channel_lists, user, sc)

    # users = user_list = sc.api_call(
    #     "users.list")
    # x = 0
    # while x < len(users["members"]):
    #     if users["members"][x]["real_name"] == 'Gary Basin':
    #         print 'Gary Basin'
    #     x += 1


else:
    print "Connection Failed, invalid token?"

# In case i want to start usings bots...
# print sc.api_call(
# 	"chat.postMessage", channel="#general", text="How are you feeling today, sir?",
#      username='ronbot', icon_emoji=':robot_face:'
# )







