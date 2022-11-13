# naudojami moduliai
import sqlite3


# klasė, konstruktorius, metodai
class DuomenuBaze:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute('CREATE TABLE IF NOT EXISTS islaidos (pavadinimas text, kaina float, data date)')
        self.conn.commit()

    def pasiimti_duomenis_db(self, query):
        self.cur.execute(query)
        rows = self.cur.fetchall()
        return rows

    def irasyti_duomenis_db(self, pavadinimas, kaina, data):
        self.cur.execute('INSERT INTO islaidos VALUES (?, ?, ?)', (pavadinimas, kaina, data))
        self.conn.commit()

    def trinti_duomenis_db(self, rwid):
        self.cur.execute('DELETE FROM islaidos WHERE rowid=?', (rwid,))
        self.conn.commit()

    def atnaujinti_duomenis_db(self, pavadinimas, kaina, data, rid):
        self.cur.execute('UPDATE islaidos SET pavadinimas = ?, kaina = ?, data = ? WHERE rowid = ?', (pavadinimas, kaina, data, rid))
        self.conn.commit()

    def __del__(self):
        self.conn.close()
