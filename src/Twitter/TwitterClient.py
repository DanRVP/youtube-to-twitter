from src.Http.Api import Api
from src.Http.ResponseObject import Response
from src.Twitter.OAuth import OAuth

class TwitterClient:
    api = None
    default_headers = {
        'Connection': 'close',
        'User-Agent': 'YouTube-To-Twitter',
        'Content-Type': 'application/json',
        'Authorization': '',
        'Host': 'api.twitter.com',
    }

    def __init__(self) -> None:
        self.api = Api()

    def _getAccessToken(self):
        oauth = OAuth('POST', self.api.BASE_URL + 'oauth/access_token')

    def createTweet(self, tweet_content: str) -> Response:
        data = {'text': tweet_content}
        oauth = OAuth('POST', self.api.BASE_URL + 'tweets', data)
        headers = self.default_headers
        headers['Authorization'] = oauth.createAuthorizationString()

        return self.api.post('tweets', data, headers)
