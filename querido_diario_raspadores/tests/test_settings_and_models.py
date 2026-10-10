import csv
import zipfile
from importlib.resources import files

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


STATE_TERRITORY_IDS = {"3199999", "3299999", "3399999", "3599999"}


def _read_packaged_territories():
    territories_file = files("gazette").joinpath("resources/territories.csv")
    with territories_file.open(encoding="utf-8") as csvfile:
        return list(csv.DictReader(csvfile))


def test_load_territories_populates_empty_table_from_package_resource():
    engine = create_engine("sqlite://")
    create_tables(engine)

    load_territories(engine)

    session = sessionmaker(bind=engine)()
    assert session.query(Territory).count() == len(_read_packaged_territories())
    espirito_santo = session.get(Territory, "3299999")
    assert espirito_santo.name == "Governo do Estado do Espírito Santo"
    assert espirito_santo.state_code == "ES"
    assert espirito_santo.state == "Espírito Santo"


def test_load_territories_inserts_only_missing_territories():
    rows = _read_packaged_territories()
    engine = create_engine("sqlite://")
    create_tables(engine)
    session = sessionmaker(bind=engine)()
    session.bulk_save_objects(
        [Territory(**row) for row in rows if row["id"] not in STATE_TERRITORY_IDS]
    )
    session.commit()
    assert session.query(Territory).count() == len(rows) - len(STATE_TERRITORY_IDS)

    load_territories(engine)

    assert session.query(Territory).count() == len(rows)
    inserted_ids = {
        territory_id
        for (territory_id,) in session.query(Territory.id).filter(
            Territory.id.in_(STATE_TERRITORY_IDS)
        )
    }
    assert inserted_ids == STATE_TERRITORY_IDS


def test_load_territories_is_idempotent():
    engine = create_engine("sqlite://")
    create_tables(engine)

    load_territories(engine)
    load_territories(engine)

    session = sessionmaker(bind=engine)()
    assert session.query(Territory).count() == len(_read_packaged_territories())


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
