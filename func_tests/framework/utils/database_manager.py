# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
import sqlite3


class DatabaseManager:
    def get_connection(self, database_name='../../../src/datawinners/mangrovedb'):
        return sqlite3.connect(database_name)

    def get_activation_code(self, email, database_name='../../../src/datawinners/mangrovedb'):
        try:
            con = self.get_connection(database_name)
            cur = con.cursor()
            cur.execute(
                "select activation_key from registration_registrationprofile where user_id=(select id from auth_user where email=?);", (email,))
            values = cur.fetchone()
            if values is not None:
                return values[0]
            else:
                return values
        finally:
            cur.close()
            con.close()


def set_sms_telephone_number(self, telephone_number, email, database_name='../../../src/datawinners/mangrovedb'):
    try:
        con = self.get_connection(database_name)
        cur = con.cursor()
        cur.execute("update accountmanagement_organizationsettings set sms_tel_number=? where \
              organization_id=(select id from accountmanagement_organization where \
              org_id=(select org_id from accountmanagement_ngouserprofile where \
              user_id=(select id from auth_user where email=?)));", (telephone_number, email))
        con.commit()
    finally:
        cur.close()
        con.close()
