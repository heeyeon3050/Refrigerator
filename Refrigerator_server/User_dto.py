class U_dto:
    def __init__(self, U_ID='', U_PW='', U_Name='', EMAIL=''):
        self.U_ID = U_ID
        self.U_PW = U_PW
        self.U_Name = U_Name
        self.EMAIL = EMAIL

    def __str__(self):
        return self.U_ID + self.U_PW + self.U_Name + self.EMAIL
