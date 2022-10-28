import requests
from requests.auth import HTTPBasicAuth
from .wrangling import wrangle_power_data, create_filtered_and_sorted_data_frame
import pandas as pd
pd.options.plotting.backend = "plotly"


class Killawattr:
    def __init__(self, api_url, username, password):
        self.api_url = api_url
        self.username = username
        self.password = password

    def fetch_data(self, filename):
        auth = HTTPBasicAuth(self.username, self.password)
        headers = {'Content-type': 'application/json'}
        response = requests.get(
            f'{self.api_url}/{filename}', auth=auth, headers=headers)

        if response.status_code != 200:
            return None

        return response.json()

    def save_csv(self, df, filename):
        output_file = f'csv-{filename}.csv'
        with open(output_file, 'w') as f:
            f.write(df.to_csv())
            print(f'[+] Wrote the csv to {output_file}')

    def save_graph(self, df, filename):
        df = df.round(1)
        output_file = f'graph-{filename}.html'
        graph = df.plot.line()
        graph.write_html(output_file)
        print(f'[+] Wrote the graph to {output_file}')

    def get_clean_visualize_data(self, filename):
        data = self.fetch_data(filename)
        if not data:
            print(
                '[!] Couldn\'t get data. Try another filename or check your internet connection.')
            return

        wrangled_data = wrangle_power_data(data['data'])
        df = create_filtered_and_sorted_data_frame(wrangled_data)
        self.save_graph(df, filename)
        self.save_csv(df, filename)
