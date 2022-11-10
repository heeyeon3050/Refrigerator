class P_dto:
    def __init__(self, P_Name='', St=''):
        self.P_Name = P_Name
        self.St = St

    def __str__(self):
        return self.P_Name + self.St
