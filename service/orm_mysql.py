import os
from dotenv import load_dotenv, find_dotenv
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.dialects.mysql import insert, Insert
from collections import defaultdict
from sqlalchemy.inspection import inspect
from dependencies import MySQLConfigChecker
import pandas as pd
load_dotenv(find_dotenv())

class ObjectRelativeMappingMySQL:

    def __init__(self, database):
        self.database = database

    def __enter__(self):
        """
        """
        self.engine = create_engine(
            self.connection_setting(),
            max_overflow=10,
            pool_pre_ping=True,
            pool_recycle=1200,
            echo=False, # DEBUG Mode
            )

        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        self.conn = self.engine.connect()
        return self

    def __exit__(self, *args):
        self.session.commit()
        self.conn.close()

    def connection_setting(self):
        hostname = os.getenv("MYSQL_HOST")
        username = os.getenv("MYSQL_USER")
        password = os.getenv("MYSQL_PASSWORD")
        
        mysql = MySQLConfigChecker(hostname, username, password, self.database)
        return f"mysql+pymysql://{mysql._username}:{mysql._password}@{mysql._hostname}/{mysql._database}"

    def init_db(self, base):
        """ Create rdbms table automatic
        author: Ben Liu
        args:
        conn: sqlalchemy.engine.base.Engine. connector object
        base: sqlalchemy.ext.declarative.api.DeclarativeMeta
        return:
        None.
        """
        base.metadata.create_all(self.conn)

    def drop_db(self, base):
        """ Delete rdbms table automatic
        author: Ben Liu
        args:
        conn: sqlalchemy.engine.base.Engine. connector object
        base: sqlalchemy.ext.declarative.api.DeclarativeMeta
        return:
        None.
        """
        base.metadata.drop_all(self.conn)

    def insert_on_duplicate_key(self, model: declarative_base, data: list, update_field: list):
        """
        on_duplicate_key_update for mysql
        """
        stmt = insert(model).values(data)
        d = {f: getattr(stmt.inserted, f) for f in update_field}
        self.session.execute(stmt.on_duplicate_key_update(**d))

    def query(self, *model):
        """
        inherit: session object
        model: MySQL orm table class object
        return: None
        """
        return self.session.query(*model)

class Query:
    """
    customized return type method class
    """
    def to_dict(rset):
        """
        params:
            rset: orm query object
        return:
            dict
        """
        result = defaultdict(list)
        for obj in rset:
            instance = inspect(obj)
            for key, x in instance.attrs.items():
                result[key].append(x.value)
        return result

    @classmethod
    def to_dataframe(cls, rset):
        """
        params:
            rset: orm query object
        return: dataframe
        """
        return pd.DataFrame(cls.to_dict(rset))

    def to_list(rset):
        """
        params:
            rset: orm query object
        return: list
        """
        result = []
        for obj in rset:
            instance = inspect(obj)
            items = instance.attrs.items()
            result.append([x.value for _,x in items])
        return instance.attrs.keys(), result
