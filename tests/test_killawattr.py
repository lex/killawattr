import pandas as pd
import os
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

    def test_fetching_has_content_type_set_to_application_json(self, requests_mock):
        requests_mock.register_uri(
            self.method, self.url, json=self.json, status_code=200)
        data_json = self.k.fetch_data(self.filename)
        assert requests_mock.last_request.headers['Content-type'] == 'application/json'

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


class TestKillawattrSaving:
    k = Killawattr(API_URL, USERNAME, PASSWORD)
    filename = 'test'
    df = pd.DataFrame(data={'a': [1, 2], 'b': [3, 4]})
    expected_output_csv = f'csv-{filename}.csv'
    expected_output_graph = f'graph-{filename}.html'

    def test_save_csv_generates_a_file(self):
        self.k.save_csv(self.df, self.filename)
        assert os.path.exists(self.expected_output_csv)
        os.remove(self.expected_output_csv)

    def test_save_graph_generates_a_file(self):
        self.k.save_graph(self.df, self.filename)
        assert os.path.exists(self.expected_output_graph)
        os.remove(self.expected_output_graph)
