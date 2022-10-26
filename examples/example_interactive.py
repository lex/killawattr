from killawattr.killawattr import Killawattr

api_url = 'https://api.com'
username = 'username'
password = 'password'
k = Killawattr(api_url, username, password)

done = False

while not done:
    print('Press enter to quit.')
    s = input('Enter the filename(s) you want to visualize separated by spaces: ')
    if not s:
        done = True
    else:
        for filename in s.split(' '):
            k.get_clean_visualize_data(filename)
