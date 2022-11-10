from Product_dao import P_dao
from Recipe_dao import R_dao
from User_dao import U_dao

db_host = "127.0.0.1"
db_port = 3306
database = "rma_db"
username = "RMAUSER"
password = "1234"


class Service:
    def __init__(self):
        self.r_dao = R_dao(db_host, db_port, database, username, password)
        self.p_dao = P_dao(db_host, db_port, database, username, password)
        self.u_dao = U_dao(db_host, db_port, database, username, password)

    def Search_P(self, num):
        return self.p_dao.Search(num)

    def Search_R(self):
        return self.r_dao.Search()

    def Login_Check(self, datas):
        return self.u_dao.Login_Search(datas)

    def Insert_U(self, arr):
        return self.u_dao.Insert(arr)
