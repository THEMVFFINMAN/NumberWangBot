import praw, random, re, sqlite3, time

#http://www.youtube.com/watch?v=qjOZtWZ56lc

USERNAME  = "TheNumberWangBot"
PASSWORD  = "Dat Password"
USERAGENT = "The Reddit NumberWangBot by /u/blendt"
SUBREDDIT = "all"
MAXPOSTS = 100000
WAIT = 240

WAITS = str(WAIT)

sql = sqlite3.connect('sql.db')
print('Loaded SQL Database')
cur = sql.cursor()

cur.execute('CREATE TABLE IF NOT EXISTS oldposts(ID TEXT)')
print('Loaded Completed table')

sql.commit()

r = praw.Reddit(USERAGENT)
r.login(USERNAME, PASSWORD)

def scanSub():
    print('Searching '+ SUBREDDIT + '.')
    subreddit = r.get_subreddit(SUBREDDIT)
    posts = subreddit.get_comments(limit=MAXPOSTS)
    for post in posts:
        pid = post.id
        pauthor = post.author.name

        if pauthor != "NumberWangBot":
            cur.execute('SELECT * FROM oldposts WHERE ID="%s"' % pid)
            if not cur.fetchone():
                try:
                    cur.execute('INSERT INTO oldposts VALUES("%s")' % pid)
                    digits = re.findall(r'\s\d+\s', post.body.lower())

                    if digits:
                        print('Replying to ' + pid + ' by ' + pauthor)

                    if (not random.getrandbits(1)):                     
                        post.reply("%d, That's NumberWang!!  \
                                     [^^Brought ^^to ^^you ^^by ^^the ^^NumberWang ^^Show!!](http://www.youtube.com/watch?v=qjOZtWZ56lc)" % int(digits[0]))
                        print("%d, That's NumberWang!!" % int(digits[0]))
                    else:
                        post.reply("Sorry, " + digits[0] + " is not NumberWang.  \
                                    [^^Brought ^^to ^^you ^^by ^^the ^^NumberWang ^^Show!!](http://www.youtube.com/watch?v=qjOZtWZ56lc)")
                        print("Sorry, " + digits[0] + " is not NumberWang.")

                except IndexError:
                    pass
    sql.commit()

def unreadMessages():
    unread = 0
    for mail in r.get_unread():
            unread = unread + 1
            
    print("Unread Messages:\t" + str(unread) + "\n")

def deleteNeg():
    
    print("\nCOMMENT SCORE CHECK CYCLE STARTED")
    user = r.get_redditor(USERNAME)

    for c in user.get_comments(limit=None):
      
        if c.score < 1:
                c.delete()
                print("Comment Deleted")

      
    print("COMMENT SCORE CHECK CYCLE COMPLETED")
    print("\nComment Karma:\t\t%s"%user.comment_karma)

while True:
    
    try:
        scanSub()
        deleteNeg()
        unreadMessages()
        time.sleep(WAIT)
    except :
        print('ERROR - Running again in 120 seconds \n')
        deleteNeg()
        time.sleep(WAIT)
