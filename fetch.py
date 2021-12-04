import re
import base64
import requests
import datetime
import asyncio
from screenshot import screenshot
from requests.exceptions import HTTPError

url_github = 'https://oscar-wos.github.io'
url_thm = 'https://tryhackme.com/badge/770900'


def main():
    reply = 'success'

    try:
        search = r'\"([A-z0-9+]*)\"'

        r = requests.get(url_thm)
        match = re.search(search, r.text)

        if match is None:
            exit()

        decode = base64.b64decode(match.group(1))
        decoded = str(decode, 'UTF-8')

        css_search = r'([\w\W]*)'
        css_search += r'<style scoped>([\w\W]*)<\/style>'
        css_search += r'([\w\W]*)<!--'

        css_match = re.search(css_search, decoded)

        with open('index.html', 'w') as f:
            avatar_search = r'url\(([\w\W]*png)\)'
            css_search = r'<span class="thm_rank">[\w\[\]]+<\/span>'

            css_link = '<link rel="stylesheet" href="thm.css">\n'
            css_link += '<link rel="stylesheet" href="animation.css">'

            url_replace = 'url(/img/avatar.png)'

            html_group1 = re.sub(
                avatar_search, url_replace, css_match.group(1)).replace(
                    'https://tryhackme.com/', '/')

            css_replace = '<span class="level-8"></span>'

            html_group2 = re.sub(
                css_search, css_replace, css_match.group(3)).replace(
                    'https://tryhackme.com/', '/')

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

        asyncio.get_event_loop().run_until_complete(screenshot(url_github))


if __name__ == "__main__":
    main()
