import tweepy as tweepy

from database import DatabaseHelper
from env import *


def find_link(tweet_data):
    for url in tweet_data.entities['urls']:
        temp = str(url['expanded_url'])
        if (temp.__contains__('t.me') or temp.__contains__('telegram.me')) and temp.__contains__('?'):
            return temp
        else:
            continue
    return None


if __name__ == '__main__':
    db = DatabaseHelper()
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)

    words = ' OR '.join(['t.me/HarfBeManBot', 'telegram.me/HarfBeManBot',
                         't.me/BiChatBot', 'telegram.me/BiChatBot',
                         't.me/BChatBot', 'telegram.me/BChatBot'])
    query = ' '.join([words, '-filter:retweets'])
    date_since = "2019-01-01"

    total = 0
    pages = tweepy.Cursor(api.search, q=query, count=100, result_type="recent", include_entities=True, lang="fa") \
        .pages()
    for page in pages:
        total += len(page)
        print(f'{len(page)} New Tweets - {total} Till now')
        for tweet in page:
            link = find_link(tweet)
            if link is not None:
                db.add_item(tweet, link)
