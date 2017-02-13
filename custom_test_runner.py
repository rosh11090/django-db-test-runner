import MySQLdb
from django.test.simple import DjangoTestSuiteRunner

from django.conf import settings

class NoDbTestRunner1(DjangoTestSuiteRunner):
    def setup_databases(self, **kwargs):
        """ Override the database creation defined in parent class """
        pass

    def teardown_databases(self, old_config, **kwargs):
        """ Override the database teardown defined in parent class """
        pass

class CustomDbTestRunner(DjangoTestSuiteRunner):
    def __init__(self, *args, **kwargs):
        db_setting = settings.DATABASES.get("default", {})

        self.db_name = db_setting.get("NAME", "test") 
        self.test_db_name = "test_{0}".format(self.db_name)
        self.db_kwargs = {
                'db':self.db_name,
                'user':db_setting.get("USER", "root"),
                'passwd':db_setting.get("PASSWORD", "root")
                }

        super(NoDbTestRunner, self).__init__(*args, **kwargs)


    def setup_databases(self, **kwargs):
        """ Override the database creation defined in parent class """
        # dro databases if already exitst
        db = MySQLdb.connect(**self.db_kwargs)
        cu = db.cursor()
        cu.execute("show databases")
        all_db = cu.fetchall()
        if self.test_db_name in map(lambda x: x[0], all_db):
            cu.execute("drop database {0}".format(self.test_db_name))

        cu.execute("show tables")
        res = cu.fetchall()

        cu.execute("create database {0}".format(self.test_db_name))
        for table in res:
            table_name = table[0]
            cu.execute("create table {0}.{1} like {2}.{1}".format(self.test_db_name, table_name, self.db_name))
        cu.close()

    def teardown_databases(self, old_config, **kwargs):
        """ Override the database teardown defined in parent class """
        db = MySQLdb.connect(**self.db_kwargs)
        cu = db.cursor()
        cu.execute("drop database {0}".format(self.test_db_name))
        cu.close()
