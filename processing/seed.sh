wait-for-it postgres:5432
python3 -c 'import database; database.initialize()'
echo "\copy territories FROM /mnt/data/territories.csv CSV HEADER;" | psql $DATABASE_URL
