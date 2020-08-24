import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('store.db', check_same_thread=False)
        self.c = self.conn.cursor()
        self.conn.row_factory = sqlite3.Row
        self.create_tables()

    def create_tables(self):
        try:
            self.c.execute('''
            CREATE TABLE `activities` (
                `client_id` INTEGER NOT NULL,
                `time` TIMESTAMP NOT NULL,
                `action` TEXT NOT NULL,
                `apSource` TEXT NOT NULL,
                `apNew` TEXT
            );
            ''')
            self.conn.commit()

        except Exception as e:
            print(e)

        try:
            self.c.execute('''
            CREATE TABLE `clients` (
                `id` INTEGER PRIMARY KEY NOT NULL,
                `mac` TEXT NOT NULL,
                `username` TEXT NOT NULL
            );
            ''')
            self.conn.commit()

        except Exception as e:
            print(e)

    def get_client_id(self, mac):
        self.c.execute("select id from clients where mac=?", (mac,))
        return int(self.c.fetchone()[0])

    def add_activity(self, client_id, datetime, action, apSource, apNew=None):
        values = (client_id, datetime, action, apSource, apNew)
        self.c.execute("INSERT INTO activities VALUES (?,?,?,?,?)", values)
        self.conn.commit()

    def add_client(self, mac, username):
        self.c.execute('''
        INSERT INTO clients (mac, username)
            SELECT * FROM (SELECT ?, ?) AS tmp
            WHERE NOT EXISTS (
                SELECT mac FROM clients WHERE mac = ?
            ) LIMIT 1;
        ''', (mac, username, mac))
        self.conn.commit()

    def get_activities(self, start_timestamp, end_timestamp):
        self.c.execute('''
        SELECT * FROM activities WHERE time BETWEEN
        datetime(?, 'unixepoch') AND datetime(?,'unixepoch')
        ''', (start_timestamp, end_timestamp))
        json_responce = []
        for row in self.c.fetchall():
            json_responce.append({
                "client_id": row[0],
                "time": row[1],
                "action": row[2],
                "apSource": row[3],
                "apNew": row[4]
            })
        return json_responce


