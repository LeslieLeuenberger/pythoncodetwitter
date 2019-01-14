import twitter, json, sys, csv #importing different modules needed for the execution of this code

# == OAuth Authentication ==
CONSUMER_KEY = ''
CONSUMER_SECRET = ''
OAUTH_TOKEN = ''
OAUTH_TOKEN_SECRET = '' #personal consumer secret

# Creates an access token under the the "Your access token" section
access_token="918797696-6UylNJquJsdEAuPWpdKhopfXuFXc8oarv65XpJ4m"# access token key
access_token_secret="KR2wsBRzQV7EAZyB37O1oTorePtddT8nir0g1Dc9urLQ5" #this is the personal  access token secret

auth = twitter.oauth.OAuth(access_token, access_token_secret, consumer_key, consumer_secret) #this defines the variable auth. it is used later on down below.  accesses the twitter module and grasps the oath variable.
twitter_api = twitter.Twitter(auth=auth) # calling the Twitter function, defining the variable twitter_api

csvfile = open('kevinhart.csv', 'w') #this openss a csv file named kevinhart.csv with the mode writing. w stands for writing and creates a file with only writing permissions. it means an existing file with the same name will be erased.
csvwriter = csv.writer(csvfile,delimiter ='|') #this calls the writer function of the csv module. it will create delimited strings of data, delimited by |

q = "kevinhart" #this defines the variable, so the search term for twitter, used in code down below.

# this cleans up our data so we can write unicode to CSV
def clean(val): #function "clean" with the input "val"
    clean = "" #"clean" is empty to start with. later, "clean" is returned.
    if val:
        val = val.replace('|', ' ') #replaces "|" with a space so it becomes easier to read the content of the file and create pivot tables
        val = val.replace('\n', ' ') #replaces new lines with a space
        val = val.replace('\r', ' ') #this replaces carriage returns with a space
        clean = val.encode('utf-8') #encodes the data in utf-8
    return clean #returns the clean value of "clean"

print 'Filtering the public timeline for keyword="%s"' % (q) #prints out "Filtering the public timeline for keyword=WAD2017". %s is replaced by the value follwing % and q was earlier defined as #WAD2017.
twitter_stream = twitter.TwitterStream(auth=twitter_api.auth) #defining the twitter streaming API
stream = twitter_stream.statuses.filter(track=q) #telling the Twitter streaming API to track the word "WAD2017".
for tweet in stream: #iterates through the tweets in the Twitter streaming API with the word "WAD2017"
    # print json.dumps(tweet)
    try: #the try statement is used to handle exceptions. first, the try clause is executed. If no exception occurs, the except clause is skipped and execution of the try statement is finished.
        if tweet['truncated']: #if the tweet is truncated,
            tweet_text = tweet['extended_tweet']['full_text'] #it will be replaced by the extended tweet text
        else: #if the tweet is not truncated,
            tweet_text = tweet['text'] #the tweet text object
        csvwriter.writerow([tweet['created_at'], #the csvwriter function is used to write rows in a csv file of the tweet creation date,
                            clean(tweet['user']['screen_name']), #the user's screen name,
                            clean(tweet_text), #the tweet itself,
                            tweet['user']['created_at'], #the user creation date,
                            tweet['user']['followers_count'], #the follower count,
                            tweet['user']['friends_count'], #the count of people the user follows,
                            tweet['user']['statuses_count'], #the amount of statuses the user has written,
                            clean(tweet['source']), #the utility used to post the Tweet
                            clean(tweet['user']['location']), #the profile location of the user
                            tweet['user']['geo_enabled'], #the boolean value of if the user has enabled geolocation or not
                            tweet['user']['lang'], #the user's language
                            clean(tweet['user']['time_zone']) #the user's time zone
                            ])
        print tweet_text #this prints the tweet to the terminal
    except Exception, err: #If an exception occurs during execution of the try clause, the rest of the clause is skipped. Then if its type matches the exception named after the except keyword, the except clause is executed, and then execution continues after the try statement. The exception class "Exception" contains all built-in, non-system-exiting exceptions. The "err" following Exception is a User-defined Exception and calls the specific exception.
        print err #the specific exception is printed
        pass #"pass" is used when a statement is required syntactically but you do not want any command or code to execute.

print "done" #when finished iterating, code prints "done" to terminal
