class R_dto:
    def __init__(self, F_Name='', Thing1='', Thing2='', Thing3=''):
        self.F_Name = F_Name
        self.Thing1 = Thing1
        self.Thing2 = Thing2
        self.Thing3 = Thing3

    def __str__(self):
        return self.F_Name + self.Thing1 + self.Thing2 + self.Thing3
