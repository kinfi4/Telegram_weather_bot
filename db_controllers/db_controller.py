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
            return self.cursor.execute('select * from users where subscribe = 1').fetchall()

    def subscriber_exist(self, user_id):
        with self.connection:
            data = self.cursor.execute(f'select * from users where user_id = ?', (user_id,)).fetchall()
            return len(data) > 0

    def add_subscriber(self, user_id, status=True):
        with self.connection:
            self.cursor.execute('insert into users (user_id, subscribe) values (?,?)', (user_id, status))

    def update_user(self, user_id, status):
        self.cursor.execute('update users set subscribe = ? where user_id = ?', (status, user_id))


if __name__ == '__main__':
    db = DB_Handler()
    # db.add_subscriber('132123123')
    db.update_user('Hello world', False)
    print(db.get_subscribers())
    print(db.subscriber_exist('Hello world'))
