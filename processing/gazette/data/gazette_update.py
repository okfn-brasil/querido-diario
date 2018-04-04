from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
from database.models import Gazette, db_connect, create_gazettes_table


class GazetteUpdate:
    """
    Class used to update Gazette rows in the database.
    
    Doesn't know anything about what is going to be updated, only handles connection
    with the database and querying. The latter, based on conditions given
    by an Executor class, injected when calling the `__call__` method.
    """

    def __init__(self, location):
        self.location = location
        self._session = None

    def session(self):
        if not self._session:
            engine = db_connect()
            create_gazettes_table(engine)
            self._session = sessionmaker(bind=engine)()
        return self._session

    def __call__(self, executor_cls):
        executor = executor_cls(self.location)
        rows = self.filtered_rows(executor.condition())
        executor.update(rows)
        self.session().commit()

    def filtered_rows(self, condition):
        condition = text(condition)
        query = self.session().query(Gazette).filter(condition)
        return query.all()
