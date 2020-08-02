Forza Rewards
=============

Automatically claim Forza Rewards. Requires a valid cookie.

Usage
-----
```
usage: rewards.py [-h] [--webhook WEBHOOK] [--daemon] [--interval INTERVAL]
                  cookies

Forza Reward Bot

positional arguments:
  cookie                Cookies

optional arguments:
  -h, --help            show this help message and exit
  --webhook WEBHOOK     Webhook to send notifications to
  --daemon, -d          Run as daemon
  --interval INTERVAL, -i INTERVAL
                        Interval for checks when running in daemon mode. A
                        random amount of between 2 and 4 hours is added on top
```

