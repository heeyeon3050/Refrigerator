import pymysql
from User_dto import U_dto


class U_dao:
    def __init__(self, db_host, db_port, database, username, password):
        self.db_host = db_host
        self.db_port = db_port
        self.database = database
        self.username = username
        self.password = password

    def Connect(self):
        return pymysql.connect(host=self.db_host, user=self.username, passwd=self.password,
                               db=self.database, port=self.db_port, use_unicode=True, charset='utf8')

    def Login_Search(self, arr):
        try:
            conn = self.Connect()
            sql = "SELECT U_NAME FROM USERS WHERE U_ID = %s and U_PW = %s"
            text = (arr[0], arr[1])
            cursor = conn.cursor()
            cursor.execute(sql, text)
            row = cursor.fetchone()
            conn.close()

            if row is not None:
                return U_dto(row[0])

        except Exception and IOError:
            print("DB 접속오류")

    def Insert(self, arr):
        try:
            conn = self.Connect()
            sql = f'SELECT U_NAME FROM USERS WHERE U_ID = (%s)'
            cursor = conn.cursor()
            ad = (arr[0])
            cursor.execute(sql, ad)
            row = cursor.fetchone()
            print(row)

            # 아이디가 존재할경우 return 시켜버림
            if row is not None:
                return "중복"

            sql = f'INSERT INTO USERS VALUES (%s, %s, %s, %s)'
            cursor = conn.cursor()
            ad = (arr[0], arr[1], arr[2], arr[3])
            cursor.execute(sql, ad)
            conn.commit()  # 쓰기 완료
            conn.close()
            return "성공"

        except Exception and IOError:
            print("DB 접속오류")




