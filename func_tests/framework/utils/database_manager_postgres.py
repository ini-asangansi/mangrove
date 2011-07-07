# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
import os
import sys
import psycopg2
from framework.utils.couch_http_wrapper import CouchHttpWrapper
from resources.local_settings import DATABASES

DEFAULT_DNS = "dbname='" + DATABASES['default']['NAME'] + "' user='" + DATABASES['default']['USER'] + "'"


class DatabaseManager(object):

    def get_connection(self, database_name=DEFAULT_DNS):
        """
        Function to get the connection to SQLite3 database

        Args:
        'database_name' is the relative path of the database from mangrove/func_tests/framework/utils
        This is optional field and default value is '../../../src/datawinners/mangrovedb'

        Return connection
        """
        con = psycopg2.connect(database_name)
        return con

    def get_activation_code(self, email, database_name=DEFAULT_DNS):
        """
        Function to get activation code for the given email id from SQLite3 database

        Args:
        'email' is the email address of the organization
        'database_name' is the relative path of the database from mangrove/func_tests/framework/utils.
        This is optional field and default value is '../../../src/datawinners/mangrovedb'

        Return activation code
        """
        try:
            con = self.get_connection(database_name)
            cur = con.cursor()
            cur.execute(
                "select activation_key from registration_registrationprofile where user_id=(select id from auth_user where email=%s);", (email,))
            values = cur.fetchone()
            if values is not None:
                return values[0]
            else:
                return values
        finally:
            cur.close()
            con.close()

    def set_sms_telephone_number(self, telephone_number, email, database_name=DEFAULT_DNS):
        """
        Function to set the SMS telephone number for the organization

        Args:
        'telephone_number' is the unique telephone number for the organization on which organization will do submission
        'email' is the email address of the organization
        'database_name' is the relative path of the database from mangrove/func_tests/framework/utils.
        This is optional field and default value is '../../../src/datawinners/mangrovedb'
        """
        try:
            con = self.get_connection(database_name)
            cur = con.cursor()
            cur.execute("update accountmanagement_organizationsetting set sms_tel_number=%s where \
                  organization_id=(select org_id from accountmanagement_ngouserprofile where \
                  user_id=(select id from auth_user where email=%s));" , (telephone_number, email))
            con.commit()
        except Exception as e:
            print e
        finally:
            cur.close()
            con.close()

    def delete_organization_all_details(self, email, database_name=DEFAULT_DNS):
        """
        Function to delete all the organization related details

        Args:
        'email' is the email address of the organization
        'database_name' is the relative path of the database from mangrove/func_tests/framework/utils.
        This is optional field and default value is '../../../src/datawinners/mangrovedb'
        """
        try:
            con = self.get_connection(database_name)
            cur = con.cursor()
            cur.execute("select id from auth_user where email=%s;", (email,))
            user_id = int(cur.fetchone()[0])
            cur.execute("select org_id from accountmanagement_ngouserprofile where user_id=%s;", (user_id,))
            org_id = str(cur.fetchone()[0])
            cur.execute("select document_store from accountmanagement_organizationsetting where organization_id=%s;", (org_id,))
            organization_db_name = str(cur.fetchone()[0])
            cur.execute("delete from accountmanagement_organization where org_id=%s;", (org_id,))
            cur.execute("delete from registration_registrationprofile where user_id=%s;", (user_id,))
            cur.execute("delete from accountmanagement_ngouserprofile where org_id=%s;", (org_id,))
            cur.execute("delete from accountmanagement_organizationsetting where organization_id=%s;", (org_id,))
            cur.execute("delete from auth_user_groups where user_id=%s;", (user_id,))
            cur.execute("delete from auth_user where id=%s;", (user_id,))
            con.commit()
            return organization_db_name
        finally:
            cur.close()
            con.close()

if __name__ == "__main__":
    db = DatabaseManager()
    dbname = db.delete_organization_all_details("ngo993cmv@ngo.com")
    print dbname