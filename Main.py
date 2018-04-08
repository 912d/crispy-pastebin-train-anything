# -- coding: utf-8 --
import urllib2
import MySQLdb
import json
import time
import Logger
from Properties import Properties


class PastebinScraper():
    # Class Variables
    client = None
    cursor = None
    conn = None

    def getPasteText(self, paste_key):
        try:
            req = urllib2.urlopen('https://pastebin.com/raw/' + paste_key, timeout=3)
            pasteText = req.read()
            file = open(Properties.pastedirectory + paste_key, "w")
            file.write(pasteText)
            file.close()
            return pasteText
        except IOError as e:
            Logger.log("getPasteText", e)
            print("[!] API Error1:", e)


    def initDB(self):
        Logger.log("initDB", "Initializing database..")
        try:
            self.conn = MySQLdb.connect(
                host=Properties.host,
                user=Properties.user,
                passwd=Properties.password,
                db=Properties.database,
                use_unicode=True,
                charset=Properties.charset
            )
            self.conn.set_character_set('utf8')
            self.cursor = self.conn.cursor()
            self.cursor.execute('SET NAMES utf8mb4;')
            self.cursor.execute('SET CHARACTER SET utf8mb4;')
            self.cursor.execute('SET character_set_connection=utf8mb4;')
        except Exception as e:
            Logger.log("initDB", e)
            print("[!] API Error:", e)


    def scraper(self):
        data, limit = self.getlimiteddata()
        Logger.log("scraper", "Starting looping through pastes")

        for d in range(limit):
            print("date: " + data[d]["date"])
            txt = self.getPasteText(data[d]["key"])
            try:
                self.cursor.execute(u"""INSERT INTO P2 (fullurl, pastedate, pastekey, size, expire, title, syntax, user, txt)
                 VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)""", (data[d]["full_url"], data[d]["date"], data[d]["key"], data[d]["size"], data[d]["expire"], data[d]["title"], data[d]["syntax"], data[d]["user"], txt))
                self.conn.commit()
            except Exception as e:
                Logger.log("scraper", e)
                print("[!] API Error3:", e)


    def getlimiteddata(self):
        limit = 100
        fetchurl = 'https://pastebin.com/api_scraping.php?limit=' + str(limit)
        req = urllib2.urlopen(fetchurl, timeout=3)
        data = json.loads(req.read())
        return data, limit


if __name__ == "__main__":
    Logger.log("main", "Starting pastebin scrapper")
    paste = PastebinScraper()
    paste.initDB()

    while True:
        try:
            start = time.time()
            paste.scraper()
            end = time.time()
            secsleft = 60 - (int(round(end - start)))
            Logger.log("main", str(secsleft) + " seconds sleeping")
            time.sleep(secsleft)
        except Exception as e:
            Logger.log("main", e)
            print("[!] API Error4:", e)
