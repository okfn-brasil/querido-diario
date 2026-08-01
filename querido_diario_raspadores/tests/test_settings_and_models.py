import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from gazette import settings
from gazette.database.models import Territory, create_tables, load_territories


def test_spidermon_validation_schema_path_exists():
    schemas = settings.SPIDERMON_VALIDATION_SCHEMAS
    assert len(schemas) == 1
    assert os.path.isfile(schemas[0])


def test_load_territories_populates_table_from_package_resource():
    engine = create_engine("sqlite://")
    create_tables(engine)

    load_territories(engine)

    session = sessionmaker(bind=engine)()
    assert session.query(Territory).count() > 0
