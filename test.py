from src.Twitter.TwitterClient import TwitterClient

client = TwitterClient()
res = client.createTweet('Test. Sent via API')
print('done')
