import pymysql
from Product_dto import P_dto


class P_dao:
    def __init__(self, db_host, db_port, database, username, password):
        self.db_host = db_host
        self.db_port = db_port
        self.database = database
        self.username = username
        self.password = password

    def Connect(self):
        return pymysql.connect(host=self.db_host, user=self.username, passwd=self.password,
                               db=self.database, port=self.db_port, use_unicode=True, charset='utf8')

    def Search(self, num):
        try:
            conn = self.Connect()
            sql = f'SELECT P_NAME, ST_ FROM PRODUCT WHERE BARCODE = \'' + num + '\''
            cursor = conn.cursor()
            cursor.execute(sql)
            row = cursor.fetchone()
            conn.close()

            if row is not None:
                return P_dto(row[0], row[1])

        except Exception and IOError:
            print("DB 접속오류")
