import hashlib as h
import random
from couchdb.mapping import TextField, DateTimeField
from services.repository.DocumentBase import DocumentBase

class EncryptionHelper(object):
    def hash(self, valueToHash,salt=None, algorithm='sha1'):
        salt = salt or self.get_hexdigest('sha1', str(random.random()), str(random.random()))[:5]
        hsh = self.get_hexdigest(algorithm, salt, valueToHash)
        return '%s$%s$%s' % (algorithm, salt, hsh)

    def check_password(self, hash, password):
        array = hash.split('$')
        return hash == self.hash(password, salt=array[1],algorithm=array[0])

    def get_hexdigest(self, algorithm, salt, raw_password):
        sha = h.new(algorithm);
        sha.update(salt + raw_password)
        return sha.hexdigest()

class UserModel(DocumentBase):
    def __init__(self, id=None, encryptionHelper = EncryptionHelper(), **values):
        if values.get('password'):
            values['password'] =  encryptionHelper.hash(values['password'])
        DocumentBase.__init__(self, id=id, type= 'UserModel', **values)

    title = TextField()
    first_name = TextField()
    last_name = TextField()
    email = TextField()
    password = TextField()
    last_login = DateTimeField()
    organization_id = TextField()


    def get_username(self):
        return self.email
    username = property(get_username)


    def get_name(self):
        return self.first_name+" "+self.last_name
    name = property(get_name)


    def is_authenticated(self):
        return True
