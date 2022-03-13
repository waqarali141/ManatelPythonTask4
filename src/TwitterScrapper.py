from typing import Optional
from urllib.parse import urlparse
import os

from .exceptions import TwitterError
import requests


class FetchTwitter:
    search_by_username_url = "https://api.twitter.com/2/users/by/username/{}?user.fields=public_metrics"

    def __init__(self, bearer_token: Optional[str] = None):
        """
        create a session with twitter bearer token for API calls using requests
        :param bearer_token: Twitter API authorization token
        """
        bearer_token = bearer_token or os.getenv('BEARER_TOKEN')
        if not bearer_token:
            raise TwitterError("No Bearer Token Provided")

        # Set the Authorization token in the Request session to be used for calling Twitters EndPoints
        self._session = requests.session()
        self._session.headers = {
            'Authorization': 'Bearer {}'.format(bearer_token)
        }

    @staticmethod
    def _extract_username_from_url(url: str) -> str:
        """
        parse url to extract twitter username
        :param url: profile url
        :return: username
        """
        parsed_url = urlparse(url)
        return parsed_url.path.split('/')[-1]

    def fetch_followers(self, url: str) -> int:
        """
        fetch follower count of the given profile url
        :param url: Twitter account url
        :return: follower count
        """
        username = self._extract_username_from_url(url)
        response = self._session.get(url=self.search_by_username_url.format(username))

        if response.ok:
            res = response.json()
            follower_count = res.get('data', {}).get('public_metrics', {}).get('followers_count', -1)
            if follower_count == -1:
                raise TwitterError("Couldn't retrieve followers count")
            return follower_count
        else:
            raise TwitterError("Bad twitter request")
