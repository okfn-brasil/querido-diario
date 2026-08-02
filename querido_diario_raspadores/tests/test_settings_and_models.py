import zipfile

from spidermon.contrib.validation.jsonschema.tools import get_schema_from
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from gazette import settings
from gazette.database import models
from gazette.database.models import Territory, create_tables, load_territories


def test_spidermon_validation_schema_can_be_loaded():
    schemas = settings.SPIDERMON_VALIDATION_SCHEMAS
    assert len(schemas) == 1
    assert isinstance(get_schema_from(schemas[0]), dict)


def test_load_territories_populates_table_from_package_resource():
    engine = create_engine("sqlite://")
    create_tables(engine)

    load_territories(engine)

    session = sessionmaker(bind=engine)()
    assert session.query(Territory).count() > 0


def test_load_territories_from_zipped_package_resource(tmp_path, monkeypatch):
    archive_path = tmp_path / "gazette.egg"
    csv_contents = "id,name,state,state_code\n2700000,Alagoas,Alagoas,AL\n"

    with zipfile.ZipFile(archive_path, "w") as archive:
        archive.writestr("gazette/resources/territories.csv", csv_contents)

    with zipfile.ZipFile(archive_path) as archive:
        package_root = zipfile.Path(archive, "gazette/")
        monkeypatch.setattr(models, "files", lambda package: package_root)
        engine = create_engine("sqlite://")
        create_tables(engine)

        load_territories(engine)

        session = sessionmaker(bind=engine)()
        assert session.query(Territory).count() == 1
