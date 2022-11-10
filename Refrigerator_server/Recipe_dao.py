import pymysql
from Recipe_dto import R_dto


class R_dao:
    def __init__(self, db_host, db_port, database, username, password):
        self.db_host = db_host
        self.db_port = db_port
        self.database = database
        self.username = username
        self.password = password

    def Connect(self):
        return pymysql.connect(host=self.db_host, user=self.username, passwd=self.password,
                               db=self.database, port=self.db_port, use_unicode=True, charset='utf8')

    def Search(self):
        try:
            conn = self.Connect()
            sql = f'SELECT * FROM FOOD'
            cursor = conn.cursor()
            cursor.execute(sql)

            datas = []
            for row in cursor:
                datas.append(R_dto(row[0], row[1], row[2], row[3]))

            conn.close()
            return datas

        except Exception and IOError:
            print("DB 접속오류")
