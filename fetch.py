import re
import base64
import requests
import datetime
from requests.exceptions import HTTPError

reply = 'success'
search = r'\"([A-z0-9+]*)\"'

try:
    r = requests.get('https://tryhackme.com/badge/770900')
    match = re.search(search, r.text)

    # str(base64.b64decode(match.group(1)), 'UTF-8')
    decode = base64.b64decode(match.group(1))
    decoded = str(decode, 'UTF-8')

    css_search = r'([\w\W]*)'
    css_search += r'<style scoped>([\w\W]*)<\/style>'
    css_search += r'([\w\W]*)<!--'

    css_match = re.search(css_search, decoded)

    with open('index.html', 'w') as f:
        css_link = '<link rel="stylesheet" href="thm.css">'
        f.write(f'{css_link}\n{css_match.group(1)}{css_match.group(3)}')

    with open('thm.css', 'w') as f:
        f.write(css_match.group(2))

except HTTPError as http_err:
    reply = f'HTTP error {http_err}'
except Exception as err:
    reply = f'Other error {err}'
else:
    reply = 'unknown'

time = datetime.datetime.now()

with open('/tmp/fetch.txt', 'a') as f:
    f.write(f'{time}:{reply}')
