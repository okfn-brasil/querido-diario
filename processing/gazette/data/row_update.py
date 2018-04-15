from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
from database.models import db_connect, create_tables


class RowUpdate:
    """
    Class used to update database rows.
    
    Doesn't know anything about what is going to be updated, only handles connection
    with the database and querying. The latter, based on conditions given
    by an Executor class, injected when calling the `__call__` method.
    """

    def __init__(self, model_cls):
        self.model_cls = model_cls
        self._session = None

    def session(self):
        if not self._session:
            engine = db_connect()
            create_tables(engine)
            self._session = sessionmaker(bind=engine)()
        return self._session

    def __call__(self, executor_cls):
        executor = executor_cls(self.session())
        rows = self.filtered_rows(executor.condition())
        executor.update(rows)
        self.session().commit()

    def filtered_rows(self, condition):
        condition = text(condition)
        query = self.session().query(self.model_cls).filter(condition)
        return query.all()
