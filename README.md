# Python Crawler for Singapore Exchange

## How to run
- Run manually

    `python3 main.py -o <directory> -s <start_date> -e <end_date>`

- Run as cron job
    1. Enter script crontab -e
    2. Set time and command to run the program
        
        Ex: `0 23 * * Mon-Fri /home/longcv/workspace/dev/python-crawler/run.sh`

## Environment
- Python 3.8.10
- PIP 20.0.2