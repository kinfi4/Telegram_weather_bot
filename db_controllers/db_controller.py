import pypyodbc

from db_controllers.database_constatnts import SERVER, DRIVER, DATABASE


class DB_Handler:

    def __init__(self):
        self.cursor = self.connection.cursor()

    @property
    def connection(self):
        return self.make_connection()

    @staticmethod
    def make_connection():
        try:
            connection = pypyodbc.connect(
                'Driver={' + DRIVER + '};'
                                      'Server=' + SERVER + ';'
                                                           'Database=' + DATABASE + ';'
            )
            return connection

        except Exception as ex:
            print('yce pogano')
            print(ex)
            return None

    def get_subscribers(self):
        with self.connection:
            return self.cursor.execute('SELECT * FROM bot_users WHERE status = 1').fetchall()

    def subscriber_exist(self, user_id):
        with self.connection:
            data = self.cursor.execute(f'SELECT * FROM bot_users WHERE user_id = ?', (user_id,)).fetchall()
            return len(data) > 0

    def add_subscriber(self, user_id, city, status=True):
        with self.connection:
            self.cursor.execute(f'INSERT INTO bot_users (user_id, status, city) VALUES (?,?,?)',
                                (user_id, status, city)).commit()

    def get_user_city(self, user_id):
        with self.connection:
            data = self.cursor.execute(f'SELECT city FROM bot_users WHERE user_id = ?', (user_id,)).fetchall()

            if data:
                return data[0][0]
            else:
                return

    def update_user_status(self, user_id, status):
        with self.connection:
            self.cursor.execute(f'UPDATE bot_users SET status = ? WHERE user_id = ?', (status, user_id)).commit()

    def update_user_city(self, user_id, city):
        with self.connection:
            self.cursor.execute(f'update bot_users set city = ? where user_id = ?', (city, user_id)).commit()

    def close(self):
        self.connection.close()


if __name__ == '__main__':
    db = DB_Handler()
    # db.add_subscriber('Hell')
    # db.update_user('132123123', False)
    print(db.get_subscribers())
    print(db.get_user_city('428404849'))

    # 428404849
