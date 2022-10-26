from killawattr.killawattr import Killawattr

API_URL = 'https://api.com'


class TestKillawattr:
    k = Killawattr(API_URL)

    def test_given_api_url_is_saved(self):
        assert self.k.api_url == API_URL
