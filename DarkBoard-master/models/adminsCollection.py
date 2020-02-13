from DarkBoard.models.userCollection import userCollection

'''
Admins collection

{
 ID: int
 Name: str
}
'''
class adminsCollection(userCollection):

    def __init__(self, db):
        super().__init__()
        self.collection = db.db.Admins
        self.curMaxID = self.collection.find_one(sort=[("ID", -1)])["ID"]

