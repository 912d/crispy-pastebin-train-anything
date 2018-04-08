# -- coding: utf-8 --
import datetime
import urllib2
from Properties import Properties


def log(header, data):
    data = str(datetime.datetime.now()) + " " + data
    data = urllib2.quote(data)
    header = urllib2.quote(header)
    url = Properties.restlogger + '/add?header=' + header + '&data=' + data
    print("url: " + url)
    response = urllib2.urlopen(url, timeout=3)
    if (response.read() == "Log saved"):
        return True
    else:
        return False


if __name__ == "__main__":
    print(log('Logger.py', 'Starting Logger.py...'))