class messagesCollection:

    def __init__(self, db):
        super().__init__()
        self.collection = db.db.Messages
        self.curMaxID = self.collection.find_one(sort=[("ID", -1)])
        if self.curMaxID == None:
            self.curMaxID = 100000000-1
        else:
            self.curMaxID = self.curMaxID["ID"]

    def create(self, senderID, recipientID, assignmentID):
        pass