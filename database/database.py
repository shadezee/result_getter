import sqlite3

class Database():
    def delete_credentials(self, conn, cursor, uid):
        delete_query = '''DELETE FROM users
                            WHERE id = ?'''
        cursor.execute(delete_query, (uid,))
        conn.commit()
        return True

    def insert_credentials(self, conn, cursor, prn, seat_num, db_id):
        insert_query = '''INSERT INTO users (
                            prn,
                            seat_num,
                            db_id
                        ) VALUES (?, ?, ?)'''
        cursor.execute(insert_query, (prn, seat_num, db_id))
        conn.commit()
        return True

    def select_credentials(self, conn, cursor):
        select_query = '''SELECT
                            id,
                            prn,
                            seat_num,
                            db_id
                        FROM users'''
        cursor.execute(select_query)
        rows = cursor.fetchall()
        return rows

    def create_table(self, conn, cursor):
        create_query = '''CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            prn INTEGER,
                            seat_num INTEGER,
                            db_id INTEGER
                        )'''
        cursor.execute(create_query)
        conn.commit()
        return True

    def database_action(self, opn_type, prn, seat_num, db_id):
        conn = sqlite3.connect('database/database.db')
        cursor = conn.cursor()

        self.create_table(conn, cursor)

        if (opn_type == 'get'):
            data = self.select_credentials(conn, cursor)
            conn.close()
            return data
        if (opn_type == 'add'):
            self.insert_credentials(conn, cursor, prn, seat_num, db_id)
            conn.close()
            return True

# DELETE RECORD
# db = Database()
# conn = sqlite3.connect('database.db')
# cursor = conn.cursor()
# uid = 4
# db.delete_credentials(conn, cursor, uid)
