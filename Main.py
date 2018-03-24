#!/user/bin/python2.7
import urllib2
import MySQLdb
from raven import Client
import json
import time


class PastebinScraper():
    # Class Variables
    client = None
    cursor = None
    conn = None

    def __init__(self):
        self.client = Client(
            'https://d04b10b9414c46c3b8c220c9c7722a9e:d4282da77bf54f0cb4fe8bc3c6589dc0@sentry.io/305698')
        self.client.captureMessage('Started application pastebin scraper')

    def getPasteText(self, paste_key):
        self.client.captureMessage('Retrieving paste ' + paste_key + 'to obtain its text:')
        try:
            req = urllib2.urlopen('https://pastebin.com/raw/' + paste_key, timeout=3)
            pasteText = req.read()
            length = len(pasteText)
            self.client.captureMessage('Retrieved paste length: ' + str(length))
            file = open('np/'+paste_key, "w")
            file.write(pasteText)
            file.close()
            print(pasteText)
            return pasteText
        except IOError as e:
            print("[!] API Error:", e)
            self.client.captureException()

    def initDB(self):
        self.client.captureMessage('Initializing local MySQL database, standby...')
        try:
            self.conn = MySQLdb.connect(
                host="localhost",
                user="root",
                passwd="nanomader#!$!%(",
                db="pastebin")
            self.conn.set_character_set('utf8')
            self.cursor = self.conn.cursor()
            self.cursor.execute('SET NAMES utf8;')
            self.cursor.execute('SET CHARACTER SET utf8;')
            self.cursor.execute('SET character_set_connection=utf8;')
        except Exception as e:
            print("[!] API Error:", e)
            self.client.captureException()

    def scraper(self):
        data, limit = self.getlimiteddata()
        secs = 100
        self.client.captureMessage('Starting looping through pastes')

        for d in range(limit):
            self.client.context.activate()
            self.client.context.merge({'pasteKey': data[d]["key"]})
            txt = self.getPasteText(data[d]["key"])
            print(txt)
            try:
                self.cursor.execute("""INSERT INTO P 
                (fullurl, pastedate, pastekey, size, expire, title, syntax, user, txt)
                 VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)""", (data[d]["full_url"], data[d]["date"], data[d]["key"], data[d]["size"], data[d]["expire"], data[d]["title"], data[d]["syntax"], data[d]["user"], str(txt)))
                self.conn.commit()
            except Exception as e:
                print("[!] API Error:", e)
                self.client.captureException()
            self.client.context.clear()
        msg = str(limit) + ' pastes took'
        print(msg)
        self.client.captureMessage(msg)


    def getlimiteddata(self):
        limit = 100
        fetchurl = 'https://pastebin.com/api_scraping.php?limit=' + str(limit)
        self.client.captureMessage('FetchUrl size is ' + str(len(fetchurl)))
        req = urllib2.urlopen(fetchurl, timeout=3)
        data = json.loads(req.read())
        print('data length: ' + str(len(data)))
        self.client.captureMessage('data length: ' + str(len(data)))
        return data, limit


if __name__ == "__main__":
    paste = PastebinScraper()
    paste.initDB()
    while True:
        try:
            start = time.time()
            paste.scraper()
            end = time.time()
            secsleft = int(round(end - start))
            paste.client.captureMessage('Sleeping for ' + str(secsleft))
            time.sleep(secsleft - 5)
        except Exception as e:
            paste.client.captureException()
