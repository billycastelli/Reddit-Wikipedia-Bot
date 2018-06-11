
import praw
import wikipedia as w

reddit = praw.Reddit(client_id = 'YOUR_ID',
                     client_secret = 'YOUR_SECRET',
                     username = 'YOUR_USERNAME',
                     password = 'YOUR_PASSWORD',
                     user_agent = 'web:WikiBot:1.0 (by /u/YOUR_USERNAME)')


subreddit = reddit.subreddit("test")


# This function filters through the past 5 posts on the /r/test subreddit, 
# and searches the comments for a call to "uciWikiBot".
def pastBot():
    posts = subreddit.new(limit = 5)
    for p in posts:
        p.comments.replace_more(limit=None)
        for comment in p.comments.list():
            if "uciWikiBot:" in comment.body:
                keyword = comment.body.split(':')[-1]
                print(keyword)
                comment.reply("**Here is a summary of this article: " +
                              w.summary(keyword, sentences=3))
                print("Comment posted")


# This function filters through live comments in the /r/test subreddit
# searching for wikipedia links. Replies to these comments with a 3 sentence summary. 
# -- Added uciWikiBot functionality to stream
def streamBot():
    reply = ""
    for comment in subreddit.stream.comments():
        if 'wikipedia.org' in comment.body:
            whole_comment = comment.body.split()
            for word in whole_comment:
                if 'wikipedia.org' in word:
                    link = word
                    print("URL: ", link)
                    link = link.split('/')
                    keyword = link[-1].strip(',;:]-')
                    print("KEYWORD: ", keyword)
                    try:
                        reply = "\n" + w.summary(keyword, 3)
                        comment.reply("**Here is a summary of this Wikipedia Article:**\n" + reply)
                    except w.exceptions.DisambiguationError as e:
                        reply = "\n", w.summary(e.options[0])
                        comment.reply("**Here is a summary of this Wikipedia Article:**\n" + reply)
                    except:
                        pass
                    
        if "uciWikiBot:" in comment.body:
            keyword = comment.body.split()[-1]
            reply = w.summary(keyword, 3)
            comment.reply("**Here is a summary of this Wikipedia Article:**\n" + reply)

                    
if __name__ == "__main__":
    pastBot()
    streamBot()

    
   
