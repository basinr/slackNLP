# slackNLP-Analysis

Access a slack user's DM and channel logs, and conducts a sentiment analysis on all messages sent by the user. Uses python_slackclient, and Python's Natural Language Toolkit (NLTK). 

The user's token is required to access logs, along with the respective user_id (both are passed as command line arguments to the program). matplotlib.pyplot is used to the graph sentiment values of all DM and channel messages combined, as a time series. 
