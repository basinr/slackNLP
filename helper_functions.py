from textblob import TextBlob
import pdb
import numpy as nump
import matplotlib.pyplot as plt
# INPUT: JSON object of all messages in DM channel
# RETURNS: messages ONLY SENT BY USER in list of strings 
def parseUserMessages(params, target, size):
	counter = 0
	my_list = []
	while (counter < size):

		# This makes sure the convo isnt with a BOT (can't access "user", then)
		if not "subtype" in params[counter]:
			if params[counter]["user"] == target:
				temp = []
				temp.append(params[counter]["text"])
				temp.append(params[counter]["ts"])
				my_list.append(temp)
		counter += 1
	return my_list

#INPUT: list of string messages
#RETURNS: finds average polarity using TextBlob
def sentimentAnalyzer(value_list, key):
	size = len(value_list)
	new_list = []
	if size == 0:
		return

	for x in value_list:
		tup = []
		msg = TextBlob(x[0])
		tup.append(msg.sentiment.polarity)
		tup.append(x[1])
		tup.append(key)

		new_list.append(tup)

		# not sure what to do with this, yet:
		# msg.sentiment.subjectivity

	return new_list

def build_dict(user, sc, api_call, lists):
	dictionary = {}
	counter = 0
	size = len(lists)
	while counter < size:
		item = lists[counter]['id']
		if item not in dictionary:
			dictionary.setdefault(item, [])
		else :
			print "DUPLICATES SHOULD NOT EXIST."
		counter += 1

	# add user messages from each DM to dictionary as list of messages
	for key in dictionary: 
	    whole_convo = sc.api_call(api_call, channel=key)
	    size = len(whole_convo["messages"])

	    value = parseUserMessages(whole_convo["messages"], user, size)
	    dictionary[key] = value

	return dictionary

def get_ts(item):
	return item[1]


def print_time_series(dict_list):
	dict_list = sorted(dict_list, key=get_ts)
	# import pdb
	# pdb.set_trace()
	nump_list = []
	for x in dict_list:
		if x:
			nump_list.append(x[0])
			# print "{0} : average = {1}, std dev = {2}".format(x[2], nump.mean(x[0]),
	  #           nump.std(x[0])) 
	
	plt.plot(nump_list)
	plt.ylabel('sentiment')
	plt.xlabel('time')
	plt.show()

	# for y in nump_list:
	# 	print y

#INPUT: list of all DM convos, Channels (as JSON objects)
def driver(im_lists, channel_lists, user, sc):
	# --- for testing purposes shorten lists to only 10 items each, here --- #
	# temp = {}
	# x = 0
	# for x in range(10):
	# 	temp[x] = im_lists[x]
	
	# im_lists = temp

	# for y in range(10):
	# 	temp[y] = channel_lists[y]

	# channel_lists = temp

	#----Test Purposes End ----#

	# build dictionaries of messages for ims, all channels
	im_dict = build_dict(user, sc, "im.history", im_lists)
	ch_dict = build_dict(user, sc, "channels.history", channel_lists)

	# Apply TextBlob to messages in dictionary
	# and add to new dictionary of average sentiments, polarity
	im_dict.update(ch_dict)
	dictionary = im_dict
	sentiment_dict = dictionary
	print "key (user ID)" + ": " + "sentiment average"

	ts_list = []
	for key in dictionary: 
		if dictionary[key]:
			sentiment_dict[key] = sentimentAnalyzer(dictionary[key], key)
			for y in sentiment_dict[key]:
				ts_list.append(y)

	print_time_series(ts_list)

	    # if val:
	    #     print "{0} : average = {1}, std dev = {2}".format(key, nump.mean(val),
	    #         nump.std(val))


