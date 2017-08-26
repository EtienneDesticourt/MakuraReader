import sqlite3
import sys
import romkan
import config

class DicFetcher(object):
    WORD_QUERY = 'SELECT * FROM edict WHERE word LIKE "%s"'

    def __init__(self):
        self.con = sqlite3.connect(config.DIC_DATABASE)
        self.con.text_factory = str
        self.cur = self.con.cursor()

    def fetch_word(self, word):
        self.cur.execute(self.WORD_QUERY % word)
        rows = self.cur.fetchall()
        if len(rows) == 0: return ""
        return rows[0]
        