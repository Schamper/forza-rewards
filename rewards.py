#!/usr/bin/env python
import re
import time
import json
import random
import urllib2
import argparse
import urlparse
import traceback


URL = "https://rewards.forzamotorsport.net/en-us/redeem"
MSG = {
    "text": "",
    "username": "ForzaBot",
    "icon_emoji": ":red_car:"
}


class ForzaBot(object):
    def __init__(self, token, webhook=None, interval=43200):
        self.token = token
        self.webhook = webhook
        self.interval = interval

        self.cookies = 'xlaWebAuth_1={}'.format(self.token)

    def check(self):
        f = req(URL, cookies=self.cookies)

        if f.url != URL:
            if 'auth' in f.url:
                self.notify("Token expired")
            else:
                self.notify("Failed to check Rewards - {:d}: {}".format(f.code, f.msg))
            return

        content = f.read()
        try:
            if 'rewards-btn' in content:
                redeemurl = urlparse.urljoin(URL, re.search("data-redeemurl=\"(.+)\"", content).group(1))
                antiforgerytoken = re.search("__RequestVerificationToken.+?value=\"(.+)?\"", content).group(1)

                f = req(redeemurl, "__RequestVerificationToken={}".format(antiforgerytoken), cookies=self.cookies)
                if f.code == 200:
                    self.notify("Successfully claimed rewards!")
                else:
                    self.notify("Failed to claim rewards - {:d}: {} ({})".format(f.code, f.msg, f.read()))
            else:
                match = re.search("data-previous='\d+' data-current='(\d)+'", content)
                self.notify("{} days left until rewards".format(int(match.group(1))))
        except Exception:
            self.notify("Failed to parse response: \n```python\n{}\n```".format(traceback.format_exc()))

    def notify(self, text):
        print(text)

        if self.webhook:
            msg = dict(MSG)
            msg['text'] = text
            req(self.webhook, "payload={}".format(json.dumps(msg)))

    def run(self, daemon=False):
        drift = 0
        while True:
            self.check()

            if not daemon:
                break

            timeout = self.interval - drift
            drift = random.randint(7200, 14400)

            time.sleep(timeout + drift)


def req(url, data=None, cookies=None):
    o = urllib2.build_opener()
    o.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0')]

    if cookies:
        o.addheaders.append(('Cookie', cookies))

    return o.open(url, data)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Forza Reward Bot")
    parser.add_argument('token', help="Authentication token")
    parser.add_argument('--webhook', type=str, help="Webhook to send notifications to")
    parser.add_argument('--daemon', '-d', action='store_true', default=False, help="Run as daemon")
    parser.add_argument('--interval', '-i', type=int, default=43200, help="Interval for checks when running in daemon mode. A random amount of between 2 and 4 hours is added on top")
    args = parser.parse_args()

    bot = ForzaBot(args.token, args.webhook, args.interval)
    bot.run(args.daemon)
