from killawattr.killawattr import Killawattr

api_url = 'https://api.com'
username = 'username'
password = 'password'
filename = 'nicefile'
k = Killawattr(api_url, username, password)
k.get_clean_visualize_data(filename)
