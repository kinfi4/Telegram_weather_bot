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
            return self.cursor.execute('SELECT * FROM users WHERE subscribe = 1').fetchall()

    def subscriber_exist(self, user_id):
        with self.connection:
            data = self.cursor.execute(f'SELECT * FROM users WHERE user_id = ?', (user_id,)).fetchall()
            return len(data) > 0

    def add_subscriber(self, user_id, status=True):
        with self.connection:
            self.cursor.execute(f'INSERT INTO users (user_id, subscribe) VALUES (?,?)', (user_id, status)).commit()

    def update_user(self, user_id, status):
        with self.connection:
            self.cursor.execute(f'UPDATE users SET subscribe = ? WHERE user_id = ?', (status, user_id)).commit()

    def close(self):
        self.connection.close()


if __name__ == '__main__':
    db = DB_Handler()
    # db.add_subscriber('Hell')
    # db.update_user('132123123', False)
    print(db.get_subscribers())
    print(db.subscriber_exist('428404849'))
