from textblob import TextBlob
import pdb
import numpy as nump

# INPUT: JSON object of all messages in DM channel
# RETURNS: messages ONLY SENT BY USER in list of strings 
def parseUserMessages(params, target, size):
	counter = 0
	my_list = []
	while (counter < size):

		# This makes sure the convo isnt with a BOT (can't access "user", then)
		if not "subtype" in params[counter]:
			if params[counter]["user"] == target:
				my_list.append(params[counter]["text"])
		counter += 1
	return my_list

#INPUT: list of string messages
#RETURNS: finds average polarity using TextBlob
def sentimentAnalyzer(value_list):
	size = len(value_list)
	new_list = []
	if size == 0:
		return

	for x in value_list:
		msg = TextBlob(x)
		new_list.append(msg.sentiment.polarity)

		# not sure what to do with this, yet
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


#INPUT: list of all DM convos, Channels (as JSON objects)
def driver(im_lists, channel_lists, user, sc):
	# ims_size = len(lists['ims'])

	# build dictionaries for ims, all channels
	im_dict = build_dict(user, sc, "im.history", im_lists['ims'])
	ch_dict = build_dict(user, sc, "channels.history", channel_lists['channels'])


	# Apply TextBlob to messages in dictionary
	# and add to new dictionary of average sentiments, polarity

	im_dict.update(ch_dict)

	dictionary = im_dict
	sentiment_dict = dictionary
	print "key (user ID)" + ": " + "sentiment average"
	for key in dictionary: 
	    sentiment_dict[key] = sentimentAnalyzer(dictionary[key])
	    val = sentiment_dict[key]

	    if val:
	        print "{0} : average = {1}, std dev = {2}".format(key, nump.mean(val),
	            nump.std(val))


