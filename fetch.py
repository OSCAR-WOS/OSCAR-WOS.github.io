import re
import base64
import requests
import datetime
from requests.exceptions import HTTPError

reply = 'success'

try:
    search = r'\"([A-z0-9+]*)\"'

    r = requests.get('https://tryhackme.com/badge/770900')
    match = re.search(search, r.text)

    if match is None:
        exit()

    # str(base64.b64decode(match.group(1)), 'UTF-8')
    decode = base64.b64decode(match.group(1))
    decoded = str(decode, 'UTF-8')

    with open('output.txt', 'w') as f:
        f.write(decoded)

    css_search = r'([\w\W]*)'  # 1
    css_search += r'<style scoped>([\w\W]*)<\/style>'  # 2
    css_search += r'([\w\W]*)<!--'  # 3

    css_match = re.search(css_search, decoded)

    with open('index.html', 'w') as f:
        avatar_search = r'url\(([\w\W]*png)\)'
        css_link = '<link rel="stylesheet" href="thm.css">'

        html_group1 = re.sub(
            avatar_search, 'url(/avatar.png)', css_match.group(1)).replace(
                'https://tryhackme.com/img/', '/')

        html_group2 = css_match.group(3).replace(
            'https://tryhackme.com/img/badges/', '/')

        f.write(f'{css_link}\n{html_group1}{html_group2}')

    with open('thm.css', 'w') as f:
        f.write(css_match.group(2))

except HTTPError as http_err:
    reply = f'HTTP error {http_err}'
except Exception as err:
    reply = f'Other error {err}'
else:
    reply = 'unknown'

with open('/tmp/fetch.txt', 'a') as f:
    time = datetime.datetime.now()
    f.write(f'{time}:{reply}\n')
