import praw, random, re, sqlite3, time

#http://www.youtube.com/watch?v=qjOZtWZ56lc

USERNAME  = "NumberWangBot"
PASSWORD  = "***BOT PASSWORD***"
USERAGENT = "The Reddit NumberWangBot by blendt.com"
SUBREDDIT = "video"
MAXPOSTS = 10
WAIT = 60

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
                        post.reply("%d, That's NumberWang!!" % int(digits[0]))
                        print("%d, That's NumberWang!!" % int(digits[0]))
                    else:
                        post.reply("Sorry, " + digits[0] + " is not NumberWang.")
                        print("Sorry, " + digits[0] + " is not NumberWang.")

                except IndexError:
                    pass
    sql.commit()

def deleteNeg():
    print("COMMENT SCORE CHECK CYCLE STARTED")
    user = r.get_redditor(USERNAME)
    total = 0
    upvoted = 0
    unvoted = 0
    downvoted = 0
    deleted = 0
    for c in user.get_comments(limit=None):
      
        if len(str(c.score)) == 4:
            spaces = ""
        if len(str(c.score)) == 3:
            spaces = " "
        if len(str(c.score)) == 2:
            spaces = "  "
        if len(str(c.score)) == 1:
            spaces = "   "
      
        total = total + 1
        if c.score < 1:
                c.delete()
                deleted = deleted + 1
                downvoted = downvoted + 1
                print("Comment Deleted")
        elif c.score > 10:
                upvoted = upvoted + 1
        elif c.score > 1:
            upvoted = upvoted + 1
        elif c.score > 0:
            unvoted = unvoted + 1
      
    print ("")
    print("COMMENT SCORE CHECK CYCLE COMPLETED")
    urate = round(upvoted / float(total) * 100)
    nrate = round(unvoted / float(total) * 100)
    drate = round(downvoted / float(total) * 100)
    print("Upvoted:      %s\t%s\b\b %%"%(upvoted,urate))
    print("Unvoted       %s\t%s\b\b %%"%(unvoted,nrate))
    print("Downvoted:    %s\t%s\b\b %%"%(downvoted,drate))
    print("Total:        %s"%total)

while True:
    scanSub()
    deleteNeg()
    print('Running again in ' + WAITS + ' seconds \n')
    sql.commit()
    time.sleep(WAIT)
