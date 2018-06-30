Forza Rewards
=============

Automatically claim Forza Rewards. Requires a valid authentication token.

Usage
-----
```
usage: rewards.py [-h] [--webhook WEBHOOK] [--daemon] [--interval INTERVAL]
                  token

Forza Reward Bot

positional arguments:
  token                 Authentication token

optional arguments:
  -h, --help            show this help message and exit
  --webhook WEBHOOK     Webhook to send notifications to
  --daemon, -d          Run as daemon
  --interval INTERVAL, -i INTERVAL
                        Interval for checks when running in daemon mode. A
                        random amount of between 2 and 4 hours is added on top
```

