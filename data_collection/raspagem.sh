# coleta último dia

# coleta intervalo
scrapy crawl rn_pau_dos_ferros_2022 -a start_date=2024-05-01 -a end_date=2024-06-01 -o rn_pau_dos_ferros_2022-intervalo.csv --logfile=rn_pau_dos_ferros_2022-intervalo.log
scrapy crawl sp_paulinia -a start_date=2024-05-01 -a end_date=2024-06-01 -o sp_paulinia-intervalo.csv --logfile=sp_paulinia-intervalo.log

rm querido-diario.db

# coleta completa
scrapy crawl rn_pau_dos_ferros_2022  -o rn_pau_dos_ferros_2022-completa.csv --logfile=rn_pau_dos_ferros_2022-completa.log
scrapy crawl sp_paulinia  -o sp_paulinia-completa.csv --logfile=sp_paulinia-completa.log

rm querido-diario.db