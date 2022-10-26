from killawattr.killawattr import Killawattr

API_URL = 'https://api.com'
USERNAME = 'username'
PASSWORD = 'password'


class TestKillawattrFetching:
    k = Killawattr(API_URL, USERNAME, PASSWORD)
    method = 'GET'
    filename = 'asd'
    json = {'ok': 'ok'}
    url = f'{API_URL}/{filename}'

    def test_given_api_url_is_saved(self):
        assert self.k.api_url == API_URL

    def test_fetching_uses_given_api_url(self, requests_mock):
        requests_mock.register_uri(
            self.method, self.url, json=self.json, status_code=200)
        data_json = self.k.fetch_data(self.filename)
        assert requests_mock.called

    def test_fetching_uses_http_basic_auth(self, requests_mock):
        requests_mock.register_uri(
            self.method, self.url, json=self.json, status_code=200)
        data_json = self.k.fetch_data(self.filename)
        assert 'Basic' in requests_mock.last_request.headers['Authorization']

    def test_fetching_returns_the_json_if_http_200(self, requests_mock):
        requests_mock.register_uri(
            self.method, self.url, json=self.json, status_code=200)
        data_json = self.k.fetch_data(self.filename)
        assert data_json == self.json

    def test_fetching_returns_none_if_not_http_200(self, requests_mock):
        requests_mock.register_uri(
            self.method, self.url, json=self.json, status_code=404)
        data_json = self.k.fetch_data(self.filename)
        assert data_json == None
