import couchdb.client as c

class Server(c.Server):
    def delete(self, database):
        super(Server, self).delete(database.name)



  