#! /bin/bash
cd data_collection
rm -rf data/
rm *.db
rm arquivos_raspadores/*.csv
rm arquivos_raspadores/*.log

echo "Testando raspador para al_associacao_municipios..."
scrapy crawl al_associacao_municipios -a start=2025-05-15 --logfile=arquivos_raspadores/al_associacao_municipios.log -o arquivos_raspadores/al_associacao_municipios.csv
rm -rf data/
rm *.db
echo "Testando raspador para al_igaci..."
scrapy crawl al_igaci -a start=2025-05-15 --logfile=arquivos_raspadores/al_igaci.log -o arquivos_raspadores/al_igaci.csv
rm -rf data/
rm *.db
echo "Testando raspador para al_maceio..."
scrapy crawl al_maceio -a start=2025-05-15 --logfile=arquivos_raspadores/al_maceio.log -o arquivos_raspadores/al_maceio.csv
rm -rf data/
rm *.db
echo "Testando raspador para al_maragogi..."
scrapy crawl al_maragogi -a start=2025-05-15 --logfile=arquivos_raspadores/al_maragogi.log -o arquivos_raspadores/al_maragogi.csv
rm -rf data/
rm *.db
echo "Testando raspador para am_manaus..."
scrapy crawl am_manaus -a start=2025-05-15 --logfile=arquivos_raspadores/am_manaus.log -o arquivos_raspadores/am_manaus.csv
rm -rf data/
rm *.db
echo "Testando raspador para ap_macapa..."
scrapy crawl ap_macapa -a start=2025-05-15 --logfile=arquivos_raspadores/ap_macapa.log -o arquivos_raspadores/ap_macapa.csv
rm -rf data/
rm *.db
echo "Testando raspador para ap_santana..."
scrapy crawl ap_santana -a start=2025-05-15 --logfile=arquivos_raspadores/ap_santana.log -o arquivos_raspadores/ap_santana.csv
rm -rf data/
rm *.db
echo "Testando raspador para ap_tartarugalzinho..."
scrapy crawl ap_tartarugalzinho -a start=2025-05-15 --logfile=arquivos_raspadores/ap_tartarugalzinho.log -o arquivos_raspadores/ap_tartarugalzinho.csv
rm -rf data/
rm *.db
echo "Testando raspador para ba_abare..."
scrapy crawl ba_abare -a start=2025-05-15 --logfile=arquivos_raspadores/ba_abare.log -o arquivos_raspadores/ba_abare.csv
rm -rf data/
rm *.db
echo "Testando raspador para ba_acajutiba..."
scrapy crawl ba_acajutiba -a start=2025-05-15 --logfile=arquivos_raspadores/ba_acajutiba.log -o arquivos_raspadores/ba_acajutiba.csv
rm -rf data/
rm *.db
echo "Testando raspador para ba_adustina..."
scrapy crawl ba_adustina -a start=2025-05-15 --logfile=arquivos_raspadores/ba_adustina.log -o arquivos_raspadores/ba_adustina.csv
rm -rf data/
rm *.db
echo "Testando raspador para ba_alagoinhas..."
scrapy crawl ba_alagoinhas -a start=2025-05-15 --logfile=arquivos_raspadores/ba_alagoinhas.log -o arquivos_raspadores/ba_alagoinhas.csv
rm -rf data/
rm *.db
echo "Testando raspador para ba_alcobaca..."
scrapy crawl ba_alcobaca -a start=2025-05-15 --logfile=arquivos_raspadores/ba_alcobaca.log -o arquivos_raspadores/ba_alcobaca.csv
rm -rf data/
rm *.db
echo "Testando raspador para ba_almadina..."
scrapy crawl ba_almadina -a start=2025-05-15 --logfile=arquivos_raspadores/ba_almadina.log -o arquivos_raspadores/ba_almadina.csv
rm -rf data/
rm *.db
echo "Testando raspador para ba_anage..."
scrapy crawl ba_anage -a start=2025-05-15 --logfile=arquivos_raspadores/ba_anage.log -o arquivos_raspadores/ba_anage.csv
rm -rf data/
rm *.db
echo "Testando raspador para ba_andorinha..."
scrapy crawl ba_andorinha -a start=2025-05-15 --logfile=arquivos_raspadores/ba_andorinha.log -o arquivos_raspadores/ba_andorinha.csv
rm -rf data/
rm *.db
echo "Testando raspador para ba_angical..."
scrapy crawl ba_angical -a start=2025-05-15 --logfile=arquivos_raspadores/ba_angical.log -o arquivos_raspadores/ba_angical.csv
rm -rf data/
rm *.db
echo "Testando raspador para ba_antas..."
scrapy crawl ba_antas -a start=2025-05-15 --logfile=arquivos_raspadores/ba_antas.log -o arquivos_raspadores/ba_antas.csv
rm -rf data/
rm *.db
echo "Testando raspador para ba_apuarema..."
scrapy crawl ba_apuarema -a start=2025-05-15 --logfile=arquivos_raspadores/ba_apuarema.log -o arquivos_raspadores/ba_apuarema.csv
rm -rf data/
rm *.db
echo "Testando raspador para ba_aracas..."
scrapy crawl ba_aracas -a start=2025-05-15 --logfile=arquivos_raspadores/ba_aracas.log -o arquivos_raspadores/ba_aracas.csv
rm -rf data/
rm *.db
echo "Testando raspador para ba_aramari..."
scrapy crawl ba_aramari -a start=2025-05-15 --logfile=arquivos_raspadores/ba_aramari.log -o arquivos_raspadores/ba_aramari.csv
rm -rf data/
rm *.db
echo "Testando raspador para ba_arataca..."
scrapy crawl ba_arataca -a start=2025-05-15 --logfile=arquivos_raspadores/ba_arataca.log -o arquivos_raspadores/ba_arataca.csv
rm -rf data/
rm *.db
echo "Testando raspador para ba_banzae..."
scrapy crawl ba_banzae -a start=2025-05-15 --logfile=arquivos_raspadores/ba_banzae.log -o arquivos_raspadores/ba_banzae.csv
rm -rf data/
rm *.db
echo "Testando raspador para ba_barreiras..."
scrapy crawl ba_barreiras -a start=2025-05-15 --logfile=arquivos_raspadores/ba_barreiras.log -o arquivos_raspadores/ba_barreiras.csv
rm -rf data/
rm *.db
echo "Testando raspador para ba_barrocas_2017..."
scrapy crawl ba_barrocas_2017 -a start=2025-05-15 --logfile=arquivos_raspadores/ba_barrocas_2017.log -o arquivos_raspadores/ba_barrocas_2017.csv
rm -rf data/
rm *.db
echo "Testando raspador para ba_brotas_de_macaubas..."
scrapy crawl ba_brotas_de_macaubas -a start=2025-05-15 --logfile=arquivos_raspadores/ba_brotas_de_macaubas.log -o arquivos_raspadores/ba_brotas_de_macaubas.csv
rm -rf data/
rm *.db
echo "Testando raspador para ba_cachoeira_2017..."
scrapy crawl ba_cachoeira_2017 -a start=2025-05-15 --logfile=arquivos_raspadores/ba_cachoeira_2017.log -o arquivos_raspadores/ba_cachoeira_2017.csv
rm -rf data/
rm *.db
echo "Testando raspador para ba_cacule_2014..."
scrapy crawl ba_cacule_2014 -a start=2025-05-15 --logfile=arquivos_raspadores/ba_cacule_2014.log -o arquivos_raspadores/ba_cacule_2014.csv
rm -rf data/
rm *.db
echo "Testando raspador para ba_caetite..."
scrapy crawl ba_caetite -a start=2025-05-15 --logfile=arquivos_raspadores/ba_caetite.log -o arquivos_raspadores/ba_caetite.csv
rm -rf data/
rm *.db
echo "Testando raspador para ba_camamu_2017..."
scrapy crawl ba_camamu_2017 -a start=2025-05-15 --logfile=arquivos_raspadores/ba_camamu_2017.log -o arquivos_raspadores/ba_camamu_2017.csv
rm -rf data/
rm *.db
echo "Testando raspador para ba_campo_alegre_de_lourdes..."
scrapy crawl ba_campo_alegre_de_lourdes -a start=2025-05-15 --logfile=arquivos_raspadores/ba_campo_alegre_de_lourdes.log -o arquivos_raspadores/ba_campo_alegre_de_lourdes.csv
rm -rf data/
rm *.db
echo "Testando raspador para ba_campo_formoso..."
scrapy crawl ba_campo_formoso -a start=2025-05-15 --logfile=arquivos_raspadores/ba_campo_formoso.log -o arquivos_raspadores/ba_campo_formoso.csv
rm -rf data/
rm *.db
echo "Testando raspador para ba_canudos..."
scrapy crawl ba_canudos -a start=2025-05-15 --logfile=arquivos_raspadores/ba_canudos.log -o arquivos_raspadores/ba_canudos.csv
rm -rf data/
rm *.db
echo "Testando raspador para ba_catolandia_2015..."
scrapy crawl ba_catolandia_2015 -a start=2025-05-15 --logfile=arquivos_raspadores/ba_catolandia_2015.log -o arquivos_raspadores/ba_catolandia_2015.csv
rm -rf data/
rm *.db
echo "Testando raspador para ba_catu_2014..."
scrapy crawl ba_catu_2014 -a start=2025-05-15 --logfile=arquivos_raspadores/ba_catu_2014.log -o arquivos_raspadores/ba_catu_2014.csv
rm -rf data/
rm *.db
echo "Testando raspador para ba_cicero_dantas..."
scrapy crawl ba_cicero_dantas -a start=2025-05-15 --logfile=arquivos_raspadores/ba_cicero_dantas.log -o arquivos_raspadores/ba_cicero_dantas.csv
rm -rf data/
rm *.db
echo "Testando raspador para ba_cipo..."
scrapy crawl ba_cipo -a start=2025-05-15 --logfile=arquivos_raspadores/ba_cipo.log -o arquivos_raspadores/ba_cipo.csv
rm -rf data/
rm *.db
echo "Testando raspador para ba_correntina_2007..."
scrapy crawl ba_correntina_2007 -a start=2025-05-15 --logfile=arquivos_raspadores/ba_correntina_2007.log -o arquivos_raspadores/ba_correntina_2007.csv
rm -rf data/
rm *.db
echo "Testando raspador para ba_correntina_2025..."
scrapy crawl ba_correntina_2025 -a start=2025-05-15 --logfile=arquivos_raspadores/ba_correntina_2025.log -o arquivos_raspadores/ba_correntina_2025.csv
rm -rf data/
rm *.db
echo "Testando raspador para ba_cotegipe..."
scrapy crawl ba_cotegipe -a start=2025-05-15 --logfile=arquivos_raspadores/ba_cotegipe.log -o arquivos_raspadores/ba_cotegipe.csv
rm -rf data/
rm *.db
echo "Testando raspador para ba_cristopolis..."
scrapy crawl ba_cristopolis -a start=2025-05-15 --logfile=arquivos_raspadores/ba_cristopolis.log -o arquivos_raspadores/ba_cristopolis.csv
rm -rf data/
rm *.db
echo "Testando raspador para ba_cruz_das_almas..."
scrapy crawl ba_cruz_das_almas -a start=2025-05-15 --logfile=arquivos_raspadores/ba_cruz_das_almas.log -o arquivos_raspadores/ba_cruz_das_almas.csv
rm -rf data/
rm *.db
echo "Testando raspador para ba_esplanada..."
scrapy crawl ba_esplanada -a start=2025-05-15 --logfile=arquivos_raspadores/ba_esplanada.log -o arquivos_raspadores/ba_esplanada.csv
rm -rf data/
rm *.db
echo "Testando raspador para ba_feira_de_santana..."
scrapy crawl ba_feira_de_santana -a start=2025-05-15 --logfile=arquivos_raspadores/ba_feira_de_santana.log -o arquivos_raspadores/ba_feira_de_santana.csv
rm -rf data/
rm *.db
echo "Testando raspador para ba_formosa_do_rio_preto..."
scrapy crawl ba_formosa_do_rio_preto -a start=2025-05-15 --logfile=arquivos_raspadores/ba_formosa_do_rio_preto.log -o arquivos_raspadores/ba_formosa_do_rio_preto.csv
rm -rf data/
rm *.db
echo "Testando raspador para ba_inhambupe..."
scrapy crawl ba_inhambupe -a start=2025-05-15 --logfile=arquivos_raspadores/ba_inhambupe.log -o arquivos_raspadores/ba_inhambupe.csv
rm -rf data/
rm *.db
echo "Testando raspador para ba_ipiau..."
scrapy crawl ba_ipiau -a start=2025-05-15 --logfile=arquivos_raspadores/ba_ipiau.log -o arquivos_raspadores/ba_ipiau.csv
rm -rf data/
rm *.db
echo "Testando raspador para ba_irara..."
scrapy crawl ba_irara -a start=2025-05-15 --logfile=arquivos_raspadores/ba_irara.log -o arquivos_raspadores/ba_irara.csv
rm -rf data/
rm *.db
echo "Testando raspador para ba_itaberaba..."
scrapy crawl ba_itaberaba -a start=2025-05-15 --logfile=arquivos_raspadores/ba_itaberaba.log -o arquivos_raspadores/ba_itaberaba.csv
rm -rf data/
rm *.db
echo "Testando raspador para ba_itamaraju..."
scrapy crawl ba_itamaraju -a start=2025-05-15 --logfile=arquivos_raspadores/ba_itamaraju.log -o arquivos_raspadores/ba_itamaraju.csv
rm -rf data/
rm *.db
echo "Testando raspador para ba_itapetinga..."
scrapy crawl ba_itapetinga -a start=2025-05-15 --logfile=arquivos_raspadores/ba_itapetinga.log -o arquivos_raspadores/ba_itapetinga.csv
rm -rf data/
rm *.db
echo "Testando raspador para ba_itapicuru..."
scrapy crawl ba_itapicuru -a start=2025-05-15 --logfile=arquivos_raspadores/ba_itapicuru.log -o arquivos_raspadores/ba_itapicuru.csv
rm -rf data/
rm *.db
echo "Testando raspador para ba_itatim..."
scrapy crawl ba_itatim -a start=2025-05-15 --logfile=arquivos_raspadores/ba_itatim.log -o arquivos_raspadores/ba_itatim.csv
rm -rf data/
rm *.db
echo "Testando raspador para ba_ituacu..."
scrapy crawl ba_ituacu -a start=2025-05-15 --logfile=arquivos_raspadores/ba_ituacu.log -o arquivos_raspadores/ba_ituacu.csv
rm -rf data/
rm *.db
echo "Testando raspador para ba_jaborandi..."
scrapy crawl ba_jaborandi -a start=2025-05-15 --logfile=arquivos_raspadores/ba_jaborandi.log -o arquivos_raspadores/ba_jaborandi.csv
rm -rf data/
rm *.db
echo "Testando raspador para ba_jaguaquara..."
scrapy crawl ba_jaguaquara -a start=2025-05-15 --logfile=arquivos_raspadores/ba_jaguaquara.log -o arquivos_raspadores/ba_jaguaquara.csv
rm -rf data/
rm *.db
echo "Testando raspador para ba_jeremoabo..."
scrapy crawl ba_jeremoabo -a start=2025-05-15 --logfile=arquivos_raspadores/ba_jeremoabo.log -o arquivos_raspadores/ba_jeremoabo.csv
rm -rf data/
rm *.db
echo "Testando raspador para ba_juazeiro..."
scrapy crawl ba_juazeiro -a start=2025-05-15 --logfile=arquivos_raspadores/ba_juazeiro.log -o arquivos_raspadores/ba_juazeiro.csv
rm -rf data/
rm *.db
echo "Testando raspador para ba_laje..."
scrapy crawl ba_laje -a start=2025-05-15 --logfile=arquivos_raspadores/ba_laje.log -o arquivos_raspadores/ba_laje.csv
rm -rf data/
rm *.db
echo "Testando raspador para ba_lajedao..."
scrapy crawl ba_lajedao -a start=2025-05-15 --logfile=arquivos_raspadores/ba_lajedao.log -o arquivos_raspadores/ba_lajedao.csv
rm -rf data/
rm *.db
echo "Testando raspador para ba_lauro_de_freitas..."
scrapy crawl ba_lauro_de_freitas -a start=2025-05-15 --logfile=arquivos_raspadores/ba_lauro_de_freitas.log -o arquivos_raspadores/ba_lauro_de_freitas.csv
rm -rf data/
rm *.db
echo "Testando raspador para ba_luis_eduardo_magalhaes..."
scrapy crawl ba_luis_eduardo_magalhaes -a start=2025-05-15 --logfile=arquivos_raspadores/ba_luis_eduardo_magalhaes.log -o arquivos_raspadores/ba_luis_eduardo_magalhaes.csv
rm -rf data/
rm *.db
echo "Testando raspador para ba_macajuba..."
scrapy crawl ba_macajuba -a start=2025-05-15 --logfile=arquivos_raspadores/ba_macajuba.log -o arquivos_raspadores/ba_macajuba.csv
rm -rf data/
rm *.db
echo "Testando raspador para ba_maragogipe..."
scrapy crawl ba_maragogipe -a start=2025-05-15 --logfile=arquivos_raspadores/ba_maragogipe.log -o arquivos_raspadores/ba_maragogipe.csv
rm -rf data/
rm *.db
echo "Testando raspador para ba_mascote..."
scrapy crawl ba_mascote -a start=2025-05-15 --logfile=arquivos_raspadores/ba_mascote.log -o arquivos_raspadores/ba_mascote.csv
rm -rf data/
rm *.db
echo "Testando raspador para ba_monte_santo..."
scrapy crawl ba_monte_santo -a start=2025-05-15 --logfile=arquivos_raspadores/ba_monte_santo.log -o arquivos_raspadores/ba_monte_santo.csv
rm -rf data/
rm *.db
echo "Testando raspador para ba_morro_do_chapeu..."
scrapy crawl ba_morro_do_chapeu -a start=2025-05-15 --logfile=arquivos_raspadores/ba_morro_do_chapeu.log -o arquivos_raspadores/ba_morro_do_chapeu.csv
rm -rf data/
rm *.db
echo "Testando raspador para ba_mucuri..."
scrapy crawl ba_mucuri -a start=2025-05-15 --logfile=arquivos_raspadores/ba_mucuri.log -o arquivos_raspadores/ba_mucuri.csv
rm -rf data/
rm *.db
echo "Testando raspador para ba_prado..."
scrapy crawl ba_prado -a start=2025-05-15 --logfile=arquivos_raspadores/ba_prado.log -o arquivos_raspadores/ba_prado.csv
rm -rf data/
rm *.db
echo "Testando raspador para ba_riachao_das_neves..."
scrapy crawl ba_riachao_das_neves -a start=2025-05-15 --logfile=arquivos_raspadores/ba_riachao_das_neves.log -o arquivos_raspadores/ba_riachao_das_neves.csv
rm -rf data/
rm *.db
echo "Testando raspador para ba_salvador..."
scrapy crawl ba_salvador -a start=2025-05-15 --logfile=arquivos_raspadores/ba_salvador.log -o arquivos_raspadores/ba_salvador.csv
rm -rf data/
rm *.db
echo "Testando raspador para ba_santa_cruz_cabralia..."
scrapy crawl ba_santa_cruz_cabralia -a start=2025-05-15 --logfile=arquivos_raspadores/ba_santa_cruz_cabralia.log -o arquivos_raspadores/ba_santa_cruz_cabralia.csv
rm -rf data/
rm *.db
echo "Testando raspador para ba_santa_luzia_2021..."
scrapy crawl ba_santa_luzia_2021 -a start=2025-05-15 --logfile=arquivos_raspadores/ba_santa_luzia_2021.log -o arquivos_raspadores/ba_santa_luzia_2021.csv
rm -rf data/
rm *.db
echo "Testando raspador para ba_santa_luzia_2024..."
scrapy crawl ba_santa_luzia_2024 -a start=2025-05-15 --logfile=arquivos_raspadores/ba_santa_luzia_2024.log -o arquivos_raspadores/ba_santa_luzia_2024.csv
rm -rf data/
rm *.db
echo "Testando raspador para ba_santa_rita_de_cassia..."
scrapy crawl ba_santa_rita_de_cassia -a start=2025-05-15 --logfile=arquivos_raspadores/ba_santa_rita_de_cassia.log -o arquivos_raspadores/ba_santa_rita_de_cassia.csv
rm -rf data/
rm *.db
echo "Testando raspador para ba_santo_estevao..."
scrapy crawl ba_santo_estevao -a start=2025-05-15 --logfile=arquivos_raspadores/ba_santo_estevao.log -o arquivos_raspadores/ba_santo_estevao.csv
rm -rf data/
rm *.db
echo "Testando raspador para ba_satiro_dias..."
scrapy crawl ba_satiro_dias -a start=2025-05-15 --logfile=arquivos_raspadores/ba_satiro_dias.log -o arquivos_raspadores/ba_satiro_dias.csv
rm -rf data/
rm *.db
echo "Testando raspador para ba_senhor_do_bonfim..."
scrapy crawl ba_senhor_do_bonfim -a start=2025-05-15 --logfile=arquivos_raspadores/ba_senhor_do_bonfim.log -o arquivos_raspadores/ba_senhor_do_bonfim.csv
rm -rf data/
rm *.db
echo "Testando raspador para ba_sento_se..."
scrapy crawl ba_sento_se -a start=2025-05-15 --logfile=arquivos_raspadores/ba_sento_se.log -o arquivos_raspadores/ba_sento_se.csv
rm -rf data/
rm *.db
echo "Testando raspador para ba_tapiramuta..."
scrapy crawl ba_tapiramuta -a start=2025-05-15 --logfile=arquivos_raspadores/ba_tapiramuta.log -o arquivos_raspadores/ba_tapiramuta.csv
rm -rf data/
rm *.db
echo "Testando raspador para ba_teolandia..."
scrapy crawl ba_teolandia -a start=2025-05-15 --logfile=arquivos_raspadores/ba_teolandia.log -o arquivos_raspadores/ba_teolandia.csv
rm -rf data/
rm *.db
echo "Testando raspador para ba_tucano..."
scrapy crawl ba_tucano -a start=2025-05-15 --logfile=arquivos_raspadores/ba_tucano.log -o arquivos_raspadores/ba_tucano.csv
rm -rf data/
rm *.db
echo "Testando raspador para ce_aurora..."
scrapy crawl ce_aurora -a start=2025-05-15 --logfile=arquivos_raspadores/ce_aurora.log -o arquivos_raspadores/ce_aurora.csv
rm -rf data/
rm *.db
echo "Testando raspador para ce_caninde..."
scrapy crawl ce_caninde -a start=2025-05-15 --logfile=arquivos_raspadores/ce_caninde.log -o arquivos_raspadores/ce_caninde.csv
rm -rf data/
rm *.db
echo "Testando raspador para ce_caririacu..."
scrapy crawl ce_caririacu -a start=2025-05-15 --logfile=arquivos_raspadores/ce_caririacu.log -o arquivos_raspadores/ce_caririacu.csv
rm -rf data/
rm *.db
echo "Testando raspador para ce_caucaia..."
scrapy crawl ce_caucaia -a start=2025-05-15 --logfile=arquivos_raspadores/ce_caucaia.log -o arquivos_raspadores/ce_caucaia.csv
rm -rf data/
rm *.db
echo "Testando raspador para ce_cedro..."
scrapy crawl ce_cedro -a start=2025-05-15 --logfile=arquivos_raspadores/ce_cedro.log -o arquivos_raspadores/ce_cedro.csv
rm -rf data/
rm *.db
echo "Testando raspador para ce_crateus..."
scrapy crawl ce_crateus -a start=2025-05-15 --logfile=arquivos_raspadores/ce_crateus.log -o arquivos_raspadores/ce_crateus.csv
rm -rf data/
rm *.db
echo "Testando raspador para ce_general_sampaio..."
scrapy crawl ce_general_sampaio -a start=2025-05-15 --logfile=arquivos_raspadores/ce_general_sampaio.log -o arquivos_raspadores/ce_general_sampaio.csv
rm -rf data/
rm *.db
echo "Testando raspador para ce_hidrolandia..."
scrapy crawl ce_hidrolandia -a start=2025-05-15 --logfile=arquivos_raspadores/ce_hidrolandia.log -o arquivos_raspadores/ce_hidrolandia.csv
rm -rf data/
rm *.db
echo "Testando raspador para ce_horizonte..."
scrapy crawl ce_horizonte -a start=2025-05-15 --logfile=arquivos_raspadores/ce_horizonte.log -o arquivos_raspadores/ce_horizonte.csv
rm -rf data/
rm *.db
echo "Testando raspador para ce_itaitinga..."
scrapy crawl ce_itaitinga -a start=2025-05-15 --logfile=arquivos_raspadores/ce_itaitinga.log -o arquivos_raspadores/ce_itaitinga.csv
rm -rf data/
rm *.db
echo "Testando raspador para ce_jaguaribe..."
scrapy crawl ce_jaguaribe -a start=2025-05-15 --logfile=arquivos_raspadores/ce_jaguaribe.log -o arquivos_raspadores/ce_jaguaribe.csv
rm -rf data/
rm *.db
echo "Testando raspador para ce_juazeiro_do_norte..."
scrapy crawl ce_juazeiro_do_norte -a start=2025-05-15 --logfile=arquivos_raspadores/ce_juazeiro_do_norte.log -o arquivos_raspadores/ce_juazeiro_do_norte.csv
rm -rf data/
rm *.db
echo "Testando raspador para ce_sobral..."
scrapy crawl ce_sobral -a start=2025-05-15 --logfile=arquivos_raspadores/ce_sobral.log -o arquivos_raspadores/ce_sobral.csv
rm -rf data/
rm *.db
echo "Testando raspador para df_brasilia..."
scrapy crawl df_brasilia -a start=2025-05-15 --logfile=arquivos_raspadores/df_brasilia.log -o arquivos_raspadores/df_brasilia.csv
rm -rf data/
rm *.db
echo "Testando raspador para es_serra..."
scrapy crawl es_serra -a start=2025-05-15 --logfile=arquivos_raspadores/es_serra.log -o arquivos_raspadores/es_serra.csv
rm -rf data/
rm *.db
echo "Testando raspador para es_vila_velha..."
scrapy crawl es_vila_velha -a start=2025-05-15 --logfile=arquivos_raspadores/es_vila_velha.log -o arquivos_raspadores/es_vila_velha.csv
rm -rf data/
rm *.db
echo "Testando raspador para es_vitoria..."
scrapy crawl es_vitoria -a start=2025-05-15 --logfile=arquivos_raspadores/es_vitoria.log -o arquivos_raspadores/es_vitoria.csv
rm -rf data/
rm *.db
echo "Testando raspador para go_aparecida_de_goiania..."
scrapy crawl go_aparecida_de_goiania -a start=2025-05-15 --logfile=arquivos_raspadores/go_aparecida_de_goiania.log -o arquivos_raspadores/go_aparecida_de_goiania.csv
rm -rf data/
rm *.db
echo "Testando raspador para go_goiania..."
scrapy crawl go_goiania -a start=2025-05-15 --logfile=arquivos_raspadores/go_goiania.log -o arquivos_raspadores/go_goiania.csv
rm -rf data/
rm *.db
echo "Testando raspador para ma_afonso_cunha..."
scrapy crawl ma_afonso_cunha -a start=2025-05-15 --logfile=arquivos_raspadores/ma_afonso_cunha.log -o arquivos_raspadores/ma_afonso_cunha.csv
rm -rf data/
rm *.db
echo "Testando raspador para ma_aldeias_altas..."
scrapy crawl ma_aldeias_altas -a start=2025-05-15 --logfile=arquivos_raspadores/ma_aldeias_altas.log -o arquivos_raspadores/ma_aldeias_altas.csv
rm -rf data/
rm *.db
echo "Testando raspador para ma_anajatuba..."
scrapy crawl ma_anajatuba -a start=2025-05-15 --logfile=arquivos_raspadores/ma_anajatuba.log -o arquivos_raspadores/ma_anajatuba.csv
rm -rf data/
rm *.db
echo "Testando raspador para ma_axixa..."
scrapy crawl ma_axixa -a start=2025-05-15 --logfile=arquivos_raspadores/ma_axixa.log -o arquivos_raspadores/ma_axixa.csv
rm -rf data/
rm *.db
echo "Testando raspador para ma_bacabal..."
scrapy crawl ma_bacabal -a start=2025-05-15 --logfile=arquivos_raspadores/ma_bacabal.log -o arquivos_raspadores/ma_bacabal.csv
rm -rf data/
rm *.db
echo "Testando raspador para ma_bacuri..."
scrapy crawl ma_bacuri -a start=2025-05-15 --logfile=arquivos_raspadores/ma_bacuri.log -o arquivos_raspadores/ma_bacuri.csv
rm -rf data/
rm *.db
echo "Testando raspador para ma_boa_vista_do_gurupi..."
scrapy crawl ma_boa_vista_do_gurupi -a start=2025-05-15 --logfile=arquivos_raspadores/ma_boa_vista_do_gurupi.log -o arquivos_raspadores/ma_boa_vista_do_gurupi.csv
rm -rf data/
rm *.db
echo "Testando raspador para ma_bom_jardim..."
scrapy crawl ma_bom_jardim -a start=2025-05-15 --logfile=arquivos_raspadores/ma_bom_jardim.log -o arquivos_raspadores/ma_bom_jardim.csv
rm -rf data/
rm *.db
echo "Testando raspador para ma_bom_lugar..."
scrapy crawl ma_bom_lugar -a start=2025-05-15 --logfile=arquivos_raspadores/ma_bom_lugar.log -o arquivos_raspadores/ma_bom_lugar.csv
rm -rf data/
rm *.db
echo "Testando raspador para ma_buriticupu..."
scrapy crawl ma_buriticupu -a start=2025-05-15 --logfile=arquivos_raspadores/ma_buriticupu.log -o arquivos_raspadores/ma_buriticupu.csv
rm -rf data/
rm *.db
echo "Testando raspador para ma_caxias_2017..."
scrapy crawl ma_caxias_2017 -a start=2025-05-15 --logfile=arquivos_raspadores/ma_caxias_2017.log -o arquivos_raspadores/ma_caxias_2017.csv
rm -rf data/
rm *.db
echo "Testando raspador para ma_caxias_2021..."
scrapy crawl ma_caxias_2021 -a start=2025-05-15 --logfile=arquivos_raspadores/ma_caxias_2021.log -o arquivos_raspadores/ma_caxias_2021.csv
rm -rf data/
rm *.db
echo "Testando raspador para ma_centro_do_guilherme..."
scrapy crawl ma_centro_do_guilherme -a start=2025-05-15 --logfile=arquivos_raspadores/ma_centro_do_guilherme.log -o arquivos_raspadores/ma_centro_do_guilherme.csv
rm -rf data/
rm *.db
echo "Testando raspador para ma_codo..."
scrapy crawl ma_codo -a start=2025-05-15 --logfile=arquivos_raspadores/ma_codo.log -o arquivos_raspadores/ma_codo.csv
rm -rf data/
rm *.db
echo "Testando raspador para ma_coroata..."
scrapy crawl ma_coroata -a start=2025-05-15 --logfile=arquivos_raspadores/ma_coroata.log -o arquivos_raspadores/ma_coroata.csv
rm -rf data/
rm *.db
echo "Testando raspador para ma_duque_bacelar..."
scrapy crawl ma_duque_bacelar -a start=2025-05-15 --logfile=arquivos_raspadores/ma_duque_bacelar.log -o arquivos_raspadores/ma_duque_bacelar.csv
rm -rf data/
rm *.db
echo "Testando raspador para ma_itapecuru_mirim..."
scrapy crawl ma_itapecuru_mirim -a start=2025-05-15 --logfile=arquivos_raspadores/ma_itapecuru_mirim.log -o arquivos_raspadores/ma_itapecuru_mirim.csv
rm -rf data/
rm *.db
echo "Testando raspador para ma_maracacume..."
scrapy crawl ma_maracacume -a start=2025-05-15 --logfile=arquivos_raspadores/ma_maracacume.log -o arquivos_raspadores/ma_maracacume.csv
rm -rf data/
rm *.db
echo "Testando raspador para ma_maranhaozinho..."
scrapy crawl ma_maranhaozinho -a start=2025-05-15 --logfile=arquivos_raspadores/ma_maranhaozinho.log -o arquivos_raspadores/ma_maranhaozinho.csv
rm -rf data/
rm *.db
echo "Testando raspador para ma_nina_rodrigues..."
scrapy crawl ma_nina_rodrigues -a start=2025-05-15 --logfile=arquivos_raspadores/ma_nina_rodrigues.log -o arquivos_raspadores/ma_nina_rodrigues.csv
rm -rf data/
rm *.db
echo "Testando raspador para ma_nova_iorque..."
scrapy crawl ma_nova_iorque -a start=2025-05-15 --logfile=arquivos_raspadores/ma_nova_iorque.log -o arquivos_raspadores/ma_nova_iorque.csv
rm -rf data/
rm *.db
echo "Testando raspador para ma_peritoro..."
scrapy crawl ma_peritoro -a start=2025-05-15 --logfile=arquivos_raspadores/ma_peritoro.log -o arquivos_raspadores/ma_peritoro.csv
rm -rf data/
rm *.db
echo "Testando raspador para ma_santo_antonio_dos_lopes..."
scrapy crawl ma_santo_antonio_dos_lopes -a start=2025-05-15 --logfile=arquivos_raspadores/ma_santo_antonio_dos_lopes.log -o arquivos_raspadores/ma_santo_antonio_dos_lopes.csv
rm -rf data/
rm *.db
echo "Testando raspador para ma_sao_jose_dos_basilios..."
scrapy crawl ma_sao_jose_dos_basilios -a start=2025-05-15 --logfile=arquivos_raspadores/ma_sao_jose_dos_basilios.log -o arquivos_raspadores/ma_sao_jose_dos_basilios.csv
rm -rf data/
rm *.db
echo "Testando raspador para ma_sao_luis..."
scrapy crawl ma_sao_luis -a start=2025-05-15 --logfile=arquivos_raspadores/ma_sao_luis.log -o arquivos_raspadores/ma_sao_luis.csv
rm -rf data/
rm *.db
echo "Testando raspador para ma_sao_vicente_ferrer..."
scrapy crawl ma_sao_vicente_ferrer -a start=2025-05-15 --logfile=arquivos_raspadores/ma_sao_vicente_ferrer.log -o arquivos_raspadores/ma_sao_vicente_ferrer.csv
rm -rf data/
rm *.db
echo "Testando raspador para ma_turilandia..."
scrapy crawl ma_turilandia -a start=2025-05-15 --logfile=arquivos_raspadores/ma_turilandia.log -o arquivos_raspadores/ma_turilandia.csv
rm -rf data/
rm *.db
echo "Testando raspador para ma_viana..."
scrapy crawl ma_viana -a start=2025-05-15 --logfile=arquivos_raspadores/ma_viana.log -o arquivos_raspadores/ma_viana.csv
rm -rf data/
rm *.db
echo "Testando raspador para ma_ze_doca..."
scrapy crawl ma_ze_doca -a start=2025-05-15 --logfile=arquivos_raspadores/ma_ze_doca.log -o arquivos_raspadores/ma_ze_doca.csv
rm -rf data/
rm *.db
echo "Testando raspador para mg_belo_horizonte..."
scrapy crawl mg_belo_horizonte -a start=2025-05-15 --logfile=arquivos_raspadores/mg_belo_horizonte.log -o arquivos_raspadores/mg_belo_horizonte.csv
rm -rf data/
rm *.db
echo "Testando raspador para mg_betim..."
scrapy crawl mg_betim -a start=2025-05-15 --logfile=arquivos_raspadores/mg_betim.log -o arquivos_raspadores/mg_betim.csv
rm -rf data/
rm *.db
echo "Testando raspador para mg_campo_belo..."
scrapy crawl mg_campo_belo -a start=2025-05-15 --logfile=arquivos_raspadores/mg_campo_belo.log -o arquivos_raspadores/mg_campo_belo.csv
rm -rf data/
rm *.db
echo "Testando raspador para mg_candeias..."
scrapy crawl mg_candeias -a start=2025-05-15 --logfile=arquivos_raspadores/mg_candeias.log -o arquivos_raspadores/mg_candeias.csv
rm -rf data/
rm *.db
echo "Testando raspador para mg_carmo_da_cachoeira..."
scrapy crawl mg_carmo_da_cachoeira -a start=2025-05-15 --logfile=arquivos_raspadores/mg_carmo_da_cachoeira.log -o arquivos_raspadores/mg_carmo_da_cachoeira.csv
rm -rf data/
rm *.db
echo "Testando raspador para mg_carmo_do_rio_claro..."
scrapy crawl mg_carmo_do_rio_claro -a start=2025-05-15 --logfile=arquivos_raspadores/mg_carmo_do_rio_claro.log -o arquivos_raspadores/mg_carmo_do_rio_claro.csv
rm -rf data/
rm *.db
echo "Testando raspador para mg_contagem..."
scrapy crawl mg_contagem -a start=2025-05-15 --logfile=arquivos_raspadores/mg_contagem.log -o arquivos_raspadores/mg_contagem.csv
rm -rf data/
rm *.db
echo "Testando raspador para mg_crucilandia..."
scrapy crawl mg_crucilandia -a start=2025-05-15 --logfile=arquivos_raspadores/mg_crucilandia.log -o arquivos_raspadores/mg_crucilandia.csv
rm -rf data/
rm *.db
echo "Testando raspador para mg_itajuba..."
scrapy crawl mg_itajuba -a start=2025-05-15 --logfile=arquivos_raspadores/mg_itajuba.log -o arquivos_raspadores/mg_itajuba.csv
rm -rf data/
rm *.db
echo "Testando raspador para mg_itauna..."
scrapy crawl mg_itauna -a start=2025-05-15 --logfile=arquivos_raspadores/mg_itauna.log -o arquivos_raspadores/mg_itauna.csv
rm -rf data/
rm *.db
echo "Testando raspador para mg_januaria..."
scrapy crawl mg_januaria -a start=2025-05-15 --logfile=arquivos_raspadores/mg_januaria.log -o arquivos_raspadores/mg_januaria.csv
rm -rf data/
rm *.db
echo "Testando raspador para mg_juatuba..."
scrapy crawl mg_juatuba -a start=2025-05-15 --logfile=arquivos_raspadores/mg_juatuba.log -o arquivos_raspadores/mg_juatuba.csv
rm -rf data/
rm *.db
echo "Testando raspador para mg_nova_serrana..."
scrapy crawl mg_nova_serrana -a start=2025-05-15 --logfile=arquivos_raspadores/mg_nova_serrana.log -o arquivos_raspadores/mg_nova_serrana.csv
rm -rf data/
rm *.db
echo "Testando raspador para mg_onca_de_pitangui..."
scrapy crawl mg_onca_de_pitangui -a start=2025-05-15 --logfile=arquivos_raspadores/mg_onca_de_pitangui.log -o arquivos_raspadores/mg_onca_de_pitangui.csv
rm -rf data/
rm *.db
echo "Testando raspador para mg_piranguinho..."
scrapy crawl mg_piranguinho -a start=2025-05-15 --logfile=arquivos_raspadores/mg_piranguinho.log -o arquivos_raspadores/mg_piranguinho.csv
rm -rf data/
rm *.db
echo "Testando raspador para mg_salinas..."
scrapy crawl mg_salinas -a start=2025-05-15 --logfile=arquivos_raspadores/mg_salinas.log -o arquivos_raspadores/mg_salinas.csv
rm -rf data/
rm *.db
echo "Testando raspador para mg_taiobeiras..."
scrapy crawl mg_taiobeiras -a start=2025-05-15 --logfile=arquivos_raspadores/mg_taiobeiras.log -o arquivos_raspadores/mg_taiobeiras.csv
rm -rf data/
rm *.db
echo "Testando raspador para mg_uberaba_2003..."
scrapy crawl mg_uberaba_2003 -a start=2025-05-15 --logfile=arquivos_raspadores/mg_uberaba_2003.log -o arquivos_raspadores/mg_uberaba_2003.csv
rm -rf data/
rm *.db
echo "Testando raspador para mg_uberaba_2021..."
scrapy crawl mg_uberaba_2021 -a start=2025-05-15 --logfile=arquivos_raspadores/mg_uberaba_2021.log -o arquivos_raspadores/mg_uberaba_2021.csv
rm -rf data/
rm *.db
echo "Testando raspador para mg_uberlandia..."
scrapy crawl mg_uberlandia -a start=2025-05-15 --logfile=arquivos_raspadores/mg_uberlandia.log -o arquivos_raspadores/mg_uberlandia.csv
rm -rf data/
rm *.db
echo "Testando raspador para mg_varzea_da_palma..."
scrapy crawl mg_varzea_da_palma -a start=2025-05-15 --logfile=arquivos_raspadores/mg_varzea_da_palma.log -o arquivos_raspadores/mg_varzea_da_palma.csv
rm -rf data/
rm *.db
echo "Testando raspador para ms_bela_vista..."
scrapy crawl ms_bela_vista -a start=2025-05-15 --logfile=arquivos_raspadores/ms_bela_vista.log -o arquivos_raspadores/ms_bela_vista.csv
rm -rf data/
rm *.db
echo "Testando raspador para ms_campo_grande..."
scrapy crawl ms_campo_grande -a start=2025-05-15 --logfile=arquivos_raspadores/ms_campo_grande.log -o arquivos_raspadores/ms_campo_grande.csv
rm -rf data/
rm *.db
echo "Testando raspador para ms_corumba..."
scrapy crawl ms_corumba -a start=2025-05-15 --logfile=arquivos_raspadores/ms_corumba.log -o arquivos_raspadores/ms_corumba.csv
rm -rf data/
rm *.db
echo "Testando raspador para ms_costa_rica..."
scrapy crawl ms_costa_rica -a start=2025-05-15 --logfile=arquivos_raspadores/ms_costa_rica.log -o arquivos_raspadores/ms_costa_rica.csv
rm -rf data/
rm *.db
echo "Testando raspador para ms_deodapolis..."
scrapy crawl ms_deodapolis -a start=2025-05-15 --logfile=arquivos_raspadores/ms_deodapolis.log -o arquivos_raspadores/ms_deodapolis.csv
rm -rf data/
rm *.db
echo "Testando raspador para ms_gloria_de_dourados..."
scrapy crawl ms_gloria_de_dourados -a start=2025-05-15 --logfile=arquivos_raspadores/ms_gloria_de_dourados.log -o arquivos_raspadores/ms_gloria_de_dourados.csv
rm -rf data/
rm *.db
echo "Testando raspador para ms_inocencia..."
scrapy crawl ms_inocencia -a start=2025-05-15 --logfile=arquivos_raspadores/ms_inocencia.log -o arquivos_raspadores/ms_inocencia.csv
rm -rf data/
rm *.db
echo "Testando raspador para ms_maracaju..."
scrapy crawl ms_maracaju -a start=2025-05-15 --logfile=arquivos_raspadores/ms_maracaju.log -o arquivos_raspadores/ms_maracaju.csv
rm -rf data/
rm *.db
echo "Testando raspador para ms_paranhos..."
scrapy crawl ms_paranhos -a start=2025-05-15 --logfile=arquivos_raspadores/ms_paranhos.log -o arquivos_raspadores/ms_paranhos.csv
rm -rf data/
rm *.db
echo "Testando raspador para ms_rio_brilhante..."
scrapy crawl ms_rio_brilhante -a start=2025-05-15 --logfile=arquivos_raspadores/ms_rio_brilhante.log -o arquivos_raspadores/ms_rio_brilhante.csv
rm -rf data/
rm *.db
echo "Testando raspador para mt_cotriguacu..."
scrapy crawl mt_cotriguacu -a start=2025-05-15 --logfile=arquivos_raspadores/mt_cotriguacu.log -o arquivos_raspadores/mt_cotriguacu.csv
rm -rf data/
rm *.db
echo "Testando raspador para mt_cuiaba..."
scrapy crawl mt_cuiaba -a start=2025-05-15 --logfile=arquivos_raspadores/mt_cuiaba.log -o arquivos_raspadores/mt_cuiaba.csv
rm -rf data/
rm *.db
echo "Testando raspador para mt_rondonopolis..."
scrapy crawl mt_rondonopolis -a start=2025-05-15 --logfile=arquivos_raspadores/mt_rondonopolis.log -o arquivos_raspadores/mt_rondonopolis.csv
rm -rf data/
rm *.db
echo "Testando raspador para pa_belem..."
scrapy crawl pa_belem -a start=2025-05-15 --logfile=arquivos_raspadores/pa_belem.log -o arquivos_raspadores/pa_belem.csv
rm -rf data/
rm *.db
echo "Testando raspador para pa_garrafao_do_norte..."
scrapy crawl pa_garrafao_do_norte -a start=2025-05-15 --logfile=arquivos_raspadores/pa_garrafao_do_norte.log -o arquivos_raspadores/pa_garrafao_do_norte.csv
rm -rf data/
rm *.db
echo "Testando raspador para pa_santana_do_araguaia..."
scrapy crawl pa_santana_do_araguaia -a start=2025-05-15 --logfile=arquivos_raspadores/pa_santana_do_araguaia.log -o arquivos_raspadores/pa_santana_do_araguaia.csv
rm -rf data/
rm *.db
echo "Testando raspador para pb_jacarau..."
scrapy crawl pb_jacarau -a start=2025-05-15 --logfile=arquivos_raspadores/pb_jacarau.log -o arquivos_raspadores/pb_jacarau.csv
rm -rf data/
rm *.db
echo "Testando raspador para pb_jerico..."
scrapy crawl pb_jerico -a start=2025-05-15 --logfile=arquivos_raspadores/pb_jerico.log -o arquivos_raspadores/pb_jerico.csv
rm -rf data/
rm *.db
echo "Testando raspador para pb_joao_pessoa..."
scrapy crawl pb_joao_pessoa -a start=2025-05-15 --logfile=arquivos_raspadores/pb_joao_pessoa.log -o arquivos_raspadores/pb_joao_pessoa.csv
rm -rf data/
rm *.db
echo "Testando raspador para pb_marizopolis..."
scrapy crawl pb_marizopolis -a start=2025-05-15 --logfile=arquivos_raspadores/pb_marizopolis.log -o arquivos_raspadores/pb_marizopolis.csv
rm -rf data/
rm *.db
echo "Testando raspador para pb_piloezinhos..."
scrapy crawl pb_piloezinhos -a start=2025-05-15 --logfile=arquivos_raspadores/pb_piloezinhos.log -o arquivos_raspadores/pb_piloezinhos.csv
rm -rf data/
rm *.db
echo "Testando raspador para pb_riachao..."
scrapy crawl pb_riachao -a start=2025-05-15 --logfile=arquivos_raspadores/pb_riachao.log -o arquivos_raspadores/pb_riachao.csv
rm -rf data/
rm *.db
echo "Testando raspador para pb_sao_jose_dos_ramos..."
scrapy crawl pb_sao_jose_dos_ramos -a start=2025-05-15 --logfile=arquivos_raspadores/pb_sao_jose_dos_ramos.log -o arquivos_raspadores/pb_sao_jose_dos_ramos.csv
rm -rf data/
rm *.db
echo "Testando raspador para pb_serraria..."
scrapy crawl pb_serraria -a start=2025-05-15 --logfile=arquivos_raspadores/pb_serraria.log -o arquivos_raspadores/pb_serraria.csv
rm -rf data/
rm *.db
echo "Testando raspador para pb_sertaozinho..."
scrapy crawl pb_sertaozinho -a start=2025-05-15 --logfile=arquivos_raspadores/pb_sertaozinho.log -o arquivos_raspadores/pb_sertaozinho.csv
rm -rf data/
rm *.db
echo "Testando raspador para pb_tacima..."
scrapy crawl pb_tacima -a start=2025-05-15 --logfile=arquivos_raspadores/pb_tacima.log -o arquivos_raspadores/pb_tacima.csv
rm -rf data/
rm *.db
echo "Testando raspador para pe_cabrobo..."
scrapy crawl pe_cabrobo -a start=2025-05-15 --logfile=arquivos_raspadores/pe_cabrobo.log -o arquivos_raspadores/pe_cabrobo.csv
rm -rf data/
rm *.db
echo "Testando raspador para pe_jaboatao_dos_guararapes..."
scrapy crawl pe_jaboatao_dos_guararapes -a start=2025-05-15 --logfile=arquivos_raspadores/pe_jaboatao_dos_guararapes.log -o arquivos_raspadores/pe_jaboatao_dos_guararapes.csv
rm -rf data/
rm *.db
echo "Testando raspador para pe_moreilandia..."
scrapy crawl pe_moreilandia -a start=2025-05-15 --logfile=arquivos_raspadores/pe_moreilandia.log -o arquivos_raspadores/pe_moreilandia.csv
rm -rf data/
rm *.db
echo "Testando raspador para pe_petrolina..."
scrapy crawl pe_petrolina -a start=2025-05-15 --logfile=arquivos_raspadores/pe_petrolina.log -o arquivos_raspadores/pe_petrolina.csv
rm -rf data/
rm *.db
echo "Testando raspador para pe_recife_2015..."
scrapy crawl pe_recife_2015 -a start=2025-05-15 --logfile=arquivos_raspadores/pe_recife_2015.log -o arquivos_raspadores/pe_recife_2015.csv
rm -rf data/
rm *.db
echo "Testando raspador para pe_recife_2020..."
scrapy crawl pe_recife_2020 -a start=2025-05-15 --logfile=arquivos_raspadores/pe_recife_2020.log -o arquivos_raspadores/pe_recife_2020.csv
rm -rf data/
rm *.db
echo "Testando raspador para pi_teresina..."
scrapy crawl pi_teresina -a start=2025-05-15 --logfile=arquivos_raspadores/pi_teresina.log -o arquivos_raspadores/pi_teresina.csv
rm -rf data/
rm *.db
echo "Testando raspador para pr_antonio_olinto..."
scrapy crawl pr_antonio_olinto -a start=2025-05-15 --logfile=arquivos_raspadores/pr_antonio_olinto.log -o arquivos_raspadores/pr_antonio_olinto.csv
rm -rf data/
rm *.db
echo "Testando raspador para pr_apucarana..."
scrapy crawl pr_apucarana -a start=2025-05-15 --logfile=arquivos_raspadores/pr_apucarana.log -o arquivos_raspadores/pr_apucarana.csv
rm -rf data/
rm *.db
echo "Testando raspador para pr_arapongas..."
scrapy crawl pr_arapongas -a start=2025-05-15 --logfile=arquivos_raspadores/pr_arapongas.log -o arquivos_raspadores/pr_arapongas.csv
rm -rf data/
rm *.db
echo "Testando raspador para pr_cafelandia..."
scrapy crawl pr_cafelandia -a start=2025-05-15 --logfile=arquivos_raspadores/pr_cafelandia.log -o arquivos_raspadores/pr_cafelandia.csv
rm -rf data/
rm *.db
echo "Testando raspador para pr_cafezal_do_sul..."
scrapy crawl pr_cafezal_do_sul -a start=2025-05-15 --logfile=arquivos_raspadores/pr_cafezal_do_sul.log -o arquivos_raspadores/pr_cafezal_do_sul.csv
rm -rf data/
rm *.db
echo "Testando raspador para pr_campo_largo..."
scrapy crawl pr_campo_largo -a start=2025-05-15 --logfile=arquivos_raspadores/pr_campo_largo.log -o arquivos_raspadores/pr_campo_largo.csv
rm -rf data/
rm *.db
echo "Testando raspador para pr_campo_mourao..."
scrapy crawl pr_campo_mourao -a start=2025-05-15 --logfile=arquivos_raspadores/pr_campo_mourao.log -o arquivos_raspadores/pr_campo_mourao.csv
rm -rf data/
rm *.db
echo "Testando raspador para pr_carambei..."
scrapy crawl pr_carambei -a start=2025-05-15 --logfile=arquivos_raspadores/pr_carambei.log -o arquivos_raspadores/pr_carambei.csv
rm -rf data/
rm *.db
echo "Testando raspador para pr_castro..."
scrapy crawl pr_castro -a start=2025-05-15 --logfile=arquivos_raspadores/pr_castro.log -o arquivos_raspadores/pr_castro.csv
rm -rf data/
rm *.db
echo "Testando raspador para pr_corbelia..."
scrapy crawl pr_corbelia -a start=2025-05-15 --logfile=arquivos_raspadores/pr_corbelia.log -o arquivos_raspadores/pr_corbelia.csv
rm -rf data/
rm *.db
echo "Testando raspador para pr_curitiba..."
scrapy crawl pr_curitiba -a start=2025-05-15 --logfile=arquivos_raspadores/pr_curitiba.log -o arquivos_raspadores/pr_curitiba.csv
rm -rf data/
rm *.db
echo "Testando raspador para pr_guaraniacu..."
scrapy crawl pr_guaraniacu -a start=2025-05-15 --logfile=arquivos_raspadores/pr_guaraniacu.log -o arquivos_raspadores/pr_guaraniacu.csv
rm -rf data/
rm *.db
echo "Testando raspador para pr_ipiranga..."
scrapy crawl pr_ipiranga -a start=2025-05-15 --logfile=arquivos_raspadores/pr_ipiranga.log -o arquivos_raspadores/pr_ipiranga.csv
rm -rf data/
rm *.db
echo "Testando raspador para pr_jaboti..."
scrapy crawl pr_jaboti -a start=2025-05-15 --logfile=arquivos_raspadores/pr_jaboti.log -o arquivos_raspadores/pr_jaboti.csv
rm -rf data/
rm *.db
echo "Testando raspador para pr_juranda..."
scrapy crawl pr_juranda -a start=2025-05-15 --logfile=arquivos_raspadores/pr_juranda.log -o arquivos_raspadores/pr_juranda.csv
rm -rf data/
rm *.db
echo "Testando raspador para pr_londrina..."
scrapy crawl pr_londrina -a start=2025-05-15 --logfile=arquivos_raspadores/pr_londrina.log -o arquivos_raspadores/pr_londrina.csv
rm -rf data/
rm *.db
echo "Testando raspador para pr_mambore..."
scrapy crawl pr_mambore -a start=2025-05-15 --logfile=arquivos_raspadores/pr_mambore.log -o arquivos_raspadores/pr_mambore.csv
rm -rf data/
rm *.db
echo "Testando raspador para pr_marilandia_do_sul..."
scrapy crawl pr_marilandia_do_sul -a start=2025-05-15 --logfile=arquivos_raspadores/pr_marilandia_do_sul.log -o arquivos_raspadores/pr_marilandia_do_sul.csv
rm -rf data/
rm *.db
echo "Testando raspador para pr_maringa..."
scrapy crawl pr_maringa -a start=2025-05-15 --logfile=arquivos_raspadores/pr_maringa.log -o arquivos_raspadores/pr_maringa.csv
rm -rf data/
rm *.db
echo "Testando raspador para pr_ouro_verde_do_oeste..."
scrapy crawl pr_ouro_verde_do_oeste -a start=2025-05-15 --logfile=arquivos_raspadores/pr_ouro_verde_do_oeste.log -o arquivos_raspadores/pr_ouro_verde_do_oeste.csv
rm -rf data/
rm *.db
echo "Testando raspador para pr_pinhais..."
scrapy crawl pr_pinhais -a start=2025-05-15 --logfile=arquivos_raspadores/pr_pinhais.log -o arquivos_raspadores/pr_pinhais.csv
rm -rf data/
rm *.db
echo "Testando raspador para pr_primeiro_de_maio..."
scrapy crawl pr_primeiro_de_maio -a start=2025-05-15 --logfile=arquivos_raspadores/pr_primeiro_de_maio.log -o arquivos_raspadores/pr_primeiro_de_maio.csv
rm -rf data/
rm *.db
echo "Testando raspador para pr_santo_antonio_do_paraiso..."
scrapy crawl pr_santo_antonio_do_paraiso -a start=2025-05-15 --logfile=arquivos_raspadores/pr_santo_antonio_do_paraiso.log -o arquivos_raspadores/pr_santo_antonio_do_paraiso.csv
rm -rf data/
rm *.db
echo "Testando raspador para pr_sao_joao_do_triunfo..."
scrapy crawl pr_sao_joao_do_triunfo -a start=2025-05-15 --logfile=arquivos_raspadores/pr_sao_joao_do_triunfo.log -o arquivos_raspadores/pr_sao_joao_do_triunfo.csv
rm -rf data/
rm *.db
echo "Testando raspador para pr_sao_mateus_do_sul..."
scrapy crawl pr_sao_mateus_do_sul -a start=2025-05-15 --logfile=arquivos_raspadores/pr_sao_mateus_do_sul.log -o arquivos_raspadores/pr_sao_mateus_do_sul.csv
rm -rf data/
rm *.db
echo "Testando raspador para pr_tamboara..."
scrapy crawl pr_tamboara -a start=2025-05-15 --logfile=arquivos_raspadores/pr_tamboara.log -o arquivos_raspadores/pr_tamboara.csv
rm -rf data/
rm *.db
echo "Testando raspador para rj_angra_dos_reis..."
scrapy crawl rj_angra_dos_reis -a start=2025-05-15 --logfile=arquivos_raspadores/rj_angra_dos_reis.log -o arquivos_raspadores/rj_angra_dos_reis.csv
rm -rf data/
rm *.db
echo "Testando raspador para rj_areal..."
scrapy crawl rj_areal -a start=2025-05-15 --logfile=arquivos_raspadores/rj_areal.log -o arquivos_raspadores/rj_areal.csv
rm -rf data/
rm *.db
echo "Testando raspador para rj_armacao_dos_buzios..."
scrapy crawl rj_armacao_dos_buzios -a start=2025-05-15 --logfile=arquivos_raspadores/rj_armacao_dos_buzios.log -o arquivos_raspadores/rj_armacao_dos_buzios.csv
rm -rf data/
rm *.db
echo "Testando raspador para rj_arraial_do_cabo..."
scrapy crawl rj_arraial_do_cabo -a start=2025-05-15 --logfile=arquivos_raspadores/rj_arraial_do_cabo.log -o arquivos_raspadores/rj_arraial_do_cabo.csv
rm -rf data/
rm *.db
echo "Testando raspador para rj_barra_mansa..."
scrapy crawl rj_barra_mansa -a start=2025-05-15 --logfile=arquivos_raspadores/rj_barra_mansa.log -o arquivos_raspadores/rj_barra_mansa.csv
rm -rf data/
rm *.db
echo "Testando raspador para rj_belford_roxo..."
scrapy crawl rj_belford_roxo -a start=2025-05-15 --logfile=arquivos_raspadores/rj_belford_roxo.log -o arquivos_raspadores/rj_belford_roxo.csv
rm -rf data/
rm *.db
echo "Testando raspador para rj_cabo_frio..."
scrapy crawl rj_cabo_frio -a start=2025-05-15 --logfile=arquivos_raspadores/rj_cabo_frio.log -o arquivos_raspadores/rj_cabo_frio.csv
rm -rf data/
rm *.db
echo "Testando raspador para rj_campos_dos_goytacazes..."
scrapy crawl rj_campos_dos_goytacazes -a start=2025-05-15 --logfile=arquivos_raspadores/rj_campos_dos_goytacazes.log -o arquivos_raspadores/rj_campos_dos_goytacazes.csv
rm -rf data/
rm *.db
echo "Testando raspador para rj_casimiro_de_abreu..."
scrapy crawl rj_casimiro_de_abreu -a start=2025-05-15 --logfile=arquivos_raspadores/rj_casimiro_de_abreu.log -o arquivos_raspadores/rj_casimiro_de_abreu.csv
rm -rf data/
rm *.db
echo "Testando raspador para rj_comendador_levy_gasparian..."
scrapy crawl rj_comendador_levy_gasparian -a start=2025-05-15 --logfile=arquivos_raspadores/rj_comendador_levy_gasparian.log -o arquivos_raspadores/rj_comendador_levy_gasparian.csv
rm -rf data/
rm *.db
echo "Testando raspador para rj_cordeiro..."
scrapy crawl rj_cordeiro -a start=2025-05-15 --logfile=arquivos_raspadores/rj_cordeiro.log -o arquivos_raspadores/rj_cordeiro.csv
rm -rf data/
rm *.db
echo "Testando raspador para rj_duque_de_caxias..."
scrapy crawl rj_duque_de_caxias -a start=2025-05-15 --logfile=arquivos_raspadores/rj_duque_de_caxias.log -o arquivos_raspadores/rj_duque_de_caxias.csv
rm -rf data/
rm *.db
echo "Testando raspador para rj_iguaba_grande..."
scrapy crawl rj_iguaba_grande -a start=2025-05-15 --logfile=arquivos_raspadores/rj_iguaba_grande.log -o arquivos_raspadores/rj_iguaba_grande.csv
rm -rf data/
rm *.db
echo "Testando raspador para rj_itaguai..."
scrapy crawl rj_itaguai -a start=2025-05-15 --logfile=arquivos_raspadores/rj_itaguai.log -o arquivos_raspadores/rj_itaguai.csv
rm -rf data/
rm *.db
echo "Testando raspador para rj_macae..."
scrapy crawl rj_macae -a start=2025-05-15 --logfile=arquivos_raspadores/rj_macae.log -o arquivos_raspadores/rj_macae.csv
rm -rf data/
rm *.db
echo "Testando raspador para rj_marica..."
scrapy crawl rj_marica -a start=2025-05-15 --logfile=arquivos_raspadores/rj_marica.log -o arquivos_raspadores/rj_marica.csv
rm -rf data/
rm *.db
echo "Testando raspador para rj_mesquita..."
scrapy crawl rj_mesquita -a start=2025-05-15 --logfile=arquivos_raspadores/rj_mesquita.log -o arquivos_raspadores/rj_mesquita.csv
rm -rf data/
rm *.db
echo "Testando raspador para rj_miguel_pereira..."
scrapy crawl rj_miguel_pereira -a start=2025-05-15 --logfile=arquivos_raspadores/rj_miguel_pereira.log -o arquivos_raspadores/rj_miguel_pereira.csv
rm -rf data/
rm *.db
echo "Testando raspador para rj_niteroi..."
scrapy crawl rj_niteroi -a start=2025-05-15 --logfile=arquivos_raspadores/rj_niteroi.log -o arquivos_raspadores/rj_niteroi.csv
rm -rf data/
rm *.db
echo "Testando raspador para rj_nova_friburgo..."
scrapy crawl rj_nova_friburgo -a start=2025-05-15 --logfile=arquivos_raspadores/rj_nova_friburgo.log -o arquivos_raspadores/rj_nova_friburgo.csv
rm -rf data/
rm *.db
echo "Testando raspador para rj_nova_iguacu..."
scrapy crawl rj_nova_iguacu -a start=2025-05-15 --logfile=arquivos_raspadores/rj_nova_iguacu.log -o arquivos_raspadores/rj_nova_iguacu.csv
rm -rf data/
rm *.db
echo "Testando raspador para rj_quatis..."
scrapy crawl rj_quatis -a start=2025-05-15 --logfile=arquivos_raspadores/rj_quatis.log -o arquivos_raspadores/rj_quatis.csv
rm -rf data/
rm *.db
echo "Testando raspador para rj_queimados..."
scrapy crawl rj_queimados -a start=2025-05-15 --logfile=arquivos_raspadores/rj_queimados.log -o arquivos_raspadores/rj_queimados.csv
rm -rf data/
rm *.db
echo "Testando raspador para rj_quissama..."
scrapy crawl rj_quissama -a start=2025-05-15 --logfile=arquivos_raspadores/rj_quissama.log -o arquivos_raspadores/rj_quissama.csv
rm -rf data/
rm *.db
echo "Testando raspador para rj_rio_de_janeiro..."
scrapy crawl rj_rio_de_janeiro -a start=2025-05-15 --logfile=arquivos_raspadores/rj_rio_de_janeiro.log -o arquivos_raspadores/rj_rio_de_janeiro.csv
rm -rf data/
rm *.db
echo "Testando raspador para rj_sao_joao_da_barra..."
scrapy crawl rj_sao_joao_da_barra -a start=2025-05-15 --logfile=arquivos_raspadores/rj_sao_joao_da_barra.log -o arquivos_raspadores/rj_sao_joao_da_barra.csv
rm -rf data/
rm *.db
echo "Testando raspador para rj_sao_joao_de_meriti..."
scrapy crawl rj_sao_joao_de_meriti -a start=2025-05-15 --logfile=arquivos_raspadores/rj_sao_joao_de_meriti.log -o arquivos_raspadores/rj_sao_joao_de_meriti.csv
rm -rf data/
rm *.db
echo "Testando raspador para rj_sao_jose_do_vale_do_rio_preto..."
scrapy crawl rj_sao_jose_do_vale_do_rio_preto -a start=2025-05-15 --logfile=arquivos_raspadores/rj_sao_jose_do_vale_do_rio_preto.log -o arquivos_raspadores/rj_sao_jose_do_vale_do_rio_preto.csv
rm -rf data/
rm *.db
echo "Testando raspador para rj_sao_pedro_da_aldeia..."
scrapy crawl rj_sao_pedro_da_aldeia -a start=2025-05-15 --logfile=arquivos_raspadores/rj_sao_pedro_da_aldeia.log -o arquivos_raspadores/rj_sao_pedro_da_aldeia.csv
rm -rf data/
rm *.db
echo "Testando raspador para rj_sapucaia..."
scrapy crawl rj_sapucaia -a start=2025-05-15 --logfile=arquivos_raspadores/rj_sapucaia.log -o arquivos_raspadores/rj_sapucaia.csv
rm -rf data/
rm *.db
echo "Testando raspador para rj_saquarema..."
scrapy crawl rj_saquarema -a start=2025-05-15 --logfile=arquivos_raspadores/rj_saquarema.log -o arquivos_raspadores/rj_saquarema.csv
rm -rf data/
rm *.db
echo "Testando raspador para rj_sumidouro..."
scrapy crawl rj_sumidouro -a start=2025-05-15 --logfile=arquivos_raspadores/rj_sumidouro.log -o arquivos_raspadores/rj_sumidouro.csv
rm -rf data/
rm *.db
echo "Testando raspador para rj_varre_sai..."
scrapy crawl rj_varre_sai -a start=2025-05-15 --logfile=arquivos_raspadores/rj_varre_sai.log -o arquivos_raspadores/rj_varre_sai.csv
rm -rf data/
rm *.db
echo "Testando raspador para rn_mossoro_2008..."
scrapy crawl rn_mossoro_2008 -a start=2025-05-15 --logfile=arquivos_raspadores/rn_mossoro_2008.log -o arquivos_raspadores/rn_mossoro_2008.csv
rm -rf data/
rm *.db
echo "Testando raspador para rn_mossoro_2023..."
scrapy crawl rn_mossoro_2023 -a start=2025-05-15 --logfile=arquivos_raspadores/rn_mossoro_2023.log -o arquivos_raspadores/rn_mossoro_2023.csv
rm -rf data/
rm *.db
echo "Testando raspador para rn_natal..."
scrapy crawl rn_natal -a start=2025-05-15 --logfile=arquivos_raspadores/rn_natal.log -o arquivos_raspadores/rn_natal.csv
rm -rf data/
rm *.db
echo "Testando raspador para rn_pau_dos_ferros_2017..."
scrapy crawl rn_pau_dos_ferros_2017 -a start=2025-05-15 --logfile=arquivos_raspadores/rn_pau_dos_ferros_2017.log -o arquivos_raspadores/rn_pau_dos_ferros_2017.csv
rm -rf data/
rm *.db
echo "Testando raspador para rn_pau_dos_ferros_2022..."
scrapy crawl rn_pau_dos_ferros_2022 -a start=2025-05-15 --logfile=arquivos_raspadores/rn_pau_dos_ferros_2022.log -o arquivos_raspadores/rn_pau_dos_ferros_2022.csv
rm -rf data/
rm *.db
echo "Testando raspador para rn_santa_cruz..."
scrapy crawl rn_santa_cruz -a start=2025-05-15 --logfile=arquivos_raspadores/rn_santa_cruz.log -o arquivos_raspadores/rn_santa_cruz.csv
rm -rf data/
rm *.db
echo "Testando raspador para rn_sao_francisco_do_oeste..."
scrapy crawl rn_sao_francisco_do_oeste -a start=2025-05-15 --logfile=arquivos_raspadores/rn_sao_francisco_do_oeste.log -o arquivos_raspadores/rn_sao_francisco_do_oeste.csv
rm -rf data/
rm *.db
echo "Testando raspador para rn_taboleiro_grande..."
scrapy crawl rn_taboleiro_grande -a start=2025-05-15 --logfile=arquivos_raspadores/rn_taboleiro_grande.log -o arquivos_raspadores/rn_taboleiro_grande.csv
rm -rf data/
rm *.db
echo "Testando raspador para ro_jaru..."
scrapy crawl ro_jaru -a start=2025-05-15 --logfile=arquivos_raspadores/ro_jaru.log -o arquivos_raspadores/ro_jaru.csv
rm -rf data/
rm *.db
echo "Testando raspador para rr_boa_vista..."
scrapy crawl rr_boa_vista -a start=2025-05-15 --logfile=arquivos_raspadores/rr_boa_vista.log -o arquivos_raspadores/rr_boa_vista.csv
rm -rf data/
rm *.db
echo "Testando raspador para rs_bento_goncalves..."
scrapy crawl rs_bento_goncalves -a start=2025-05-15 --logfile=arquivos_raspadores/rs_bento_goncalves.log -o arquivos_raspadores/rs_bento_goncalves.csv
rm -rf data/
rm *.db
echo "Testando raspador para rs_cachoeira_do_sul..."
scrapy crawl rs_cachoeira_do_sul -a start=2025-05-15 --logfile=arquivos_raspadores/rs_cachoeira_do_sul.log -o arquivos_raspadores/rs_cachoeira_do_sul.csv
rm -rf data/
rm *.db
echo "Testando raspador para rs_camaqua..."
scrapy crawl rs_camaqua -a start=2025-05-15 --logfile=arquivos_raspadores/rs_camaqua.log -o arquivos_raspadores/rs_camaqua.csv
rm -rf data/
rm *.db
echo "Testando raspador para rs_candelaria..."
scrapy crawl rs_candelaria -a start=2025-05-15 --logfile=arquivos_raspadores/rs_candelaria.log -o arquivos_raspadores/rs_candelaria.csv
rm -rf data/
rm *.db
echo "Testando raspador para rs_caxias_do_sul..."
scrapy crawl rs_caxias_do_sul -a start=2025-05-15 --logfile=arquivos_raspadores/rs_caxias_do_sul.log -o arquivos_raspadores/rs_caxias_do_sul.csv
rm -rf data/
rm *.db
echo "Testando raspador para rs_cerrito..."
scrapy crawl rs_cerrito -a start=2025-05-15 --logfile=arquivos_raspadores/rs_cerrito.log -o arquivos_raspadores/rs_cerrito.csv
rm -rf data/
rm *.db
echo "Testando raspador para rs_dois_irmaos..."
scrapy crawl rs_dois_irmaos -a start=2025-05-15 --logfile=arquivos_raspadores/rs_dois_irmaos.log -o arquivos_raspadores/rs_dois_irmaos.csv
rm -rf data/
rm *.db
echo "Testando raspador para rs_estrela..."
scrapy crawl rs_estrela -a start=2025-05-15 --logfile=arquivos_raspadores/rs_estrela.log -o arquivos_raspadores/rs_estrela.csv
rm -rf data/
rm *.db
echo "Testando raspador para rs_gravatai..."
scrapy crawl rs_gravatai -a start=2025-05-15 --logfile=arquivos_raspadores/rs_gravatai.log -o arquivos_raspadores/rs_gravatai.csv
rm -rf data/
rm *.db
echo "Testando raspador para rs_horizontina..."
scrapy crawl rs_horizontina -a start=2025-05-15 --logfile=arquivos_raspadores/rs_horizontina.log -o arquivos_raspadores/rs_horizontina.csv
rm -rf data/
rm *.db
echo "Testando raspador para rs_marau..."
scrapy crawl rs_marau -a start=2025-05-15 --logfile=arquivos_raspadores/rs_marau.log -o arquivos_raspadores/rs_marau.csv
rm -rf data/
rm *.db
echo "Testando raspador para rs_panambi..."
scrapy crawl rs_panambi -a start=2025-05-15 --logfile=arquivos_raspadores/rs_panambi.log -o arquivos_raspadores/rs_panambi.csv
rm -rf data/
rm *.db
echo "Testando raspador para rs_porto_alegre..."
scrapy crawl rs_porto_alegre -a start=2025-05-15 --logfile=arquivos_raspadores/rs_porto_alegre.log -o arquivos_raspadores/rs_porto_alegre.csv
rm -rf data/
rm *.db
echo "Testando raspador para rs_quatro_irmaos..."
scrapy crawl rs_quatro_irmaos -a start=2025-05-15 --logfile=arquivos_raspadores/rs_quatro_irmaos.log -o arquivos_raspadores/rs_quatro_irmaos.csv
rm -rf data/
rm *.db
echo "Testando raspador para rs_santa_clara_do_sul..."
scrapy crawl rs_santa_clara_do_sul -a start=2025-05-15 --logfile=arquivos_raspadores/rs_santa_clara_do_sul.log -o arquivos_raspadores/rs_santa_clara_do_sul.csv
rm -rf data/
rm *.db
echo "Testando raspador para rs_santa_rosa..."
scrapy crawl rs_santa_rosa -a start=2025-05-15 --logfile=arquivos_raspadores/rs_santa_rosa.log -o arquivos_raspadores/rs_santa_rosa.csv
rm -rf data/
rm *.db
echo "Testando raspador para rs_sao_francisco_de_paula..."
scrapy crawl rs_sao_francisco_de_paula -a start=2025-05-15 --logfile=arquivos_raspadores/rs_sao_francisco_de_paula.log -o arquivos_raspadores/rs_sao_francisco_de_paula.csv
rm -rf data/
rm *.db
echo "Testando raspador para rs_sao_joao_do_polesine..."
scrapy crawl rs_sao_joao_do_polesine -a start=2025-05-15 --logfile=arquivos_raspadores/rs_sao_joao_do_polesine.log -o arquivos_raspadores/rs_sao_joao_do_polesine.csv
rm -rf data/
rm *.db
echo "Testando raspador para rs_sobradinho..."
scrapy crawl rs_sobradinho -a start=2025-05-15 --logfile=arquivos_raspadores/rs_sobradinho.log -o arquivos_raspadores/rs_sobradinho.csv
rm -rf data/
rm *.db
echo "Testando raspador para rs_tres_arroios..."
scrapy crawl rs_tres_arroios -a start=2025-05-15 --logfile=arquivos_raspadores/rs_tres_arroios.log -o arquivos_raspadores/rs_tres_arroios.csv
rm -rf data/
rm *.db
echo "Testando raspador para rs_vera_cruz..."
scrapy crawl rs_vera_cruz -a start=2025-05-15 --logfile=arquivos_raspadores/rs_vera_cruz.log -o arquivos_raspadores/rs_vera_cruz.csv
rm -rf data/
rm *.db
echo "Testando raspador para sc_florianopolis_2009..."
scrapy crawl sc_florianopolis_2009 -a start=2025-05-15 --logfile=arquivos_raspadores/sc_florianopolis_2009.log -o arquivos_raspadores/sc_florianopolis_2009.csv
rm -rf data/
rm *.db
echo "Testando raspador para sc_florianopolis_2024..."
scrapy crawl sc_florianopolis_2024 -a start=2025-05-15 --logfile=arquivos_raspadores/sc_florianopolis_2024.log -o arquivos_raspadores/sc_florianopolis_2024.csv
rm -rf data/
rm *.db
echo "Testando raspador para sc_joinville..."
scrapy crawl sc_joinville -a start=2025-05-15 --logfile=arquivos_raspadores/sc_joinville.log -o arquivos_raspadores/sc_joinville.csv
rm -rf data/
rm *.db
echo "Testando raspador para se_aquidaba..."
scrapy crawl se_aquidaba -a start=2025-05-15 --logfile=arquivos_raspadores/se_aquidaba.log -o arquivos_raspadores/se_aquidaba.csv
rm -rf data/
rm *.db
echo "Testando raspador para se_aracaju..."
scrapy crawl se_aracaju -a start=2025-05-15 --logfile=arquivos_raspadores/se_aracaju.log -o arquivos_raspadores/se_aracaju.csv
rm -rf data/
rm *.db
echo "Testando raspador para se_areia_branca..."
scrapy crawl se_areia_branca -a start=2025-05-15 --logfile=arquivos_raspadores/se_areia_branca.log -o arquivos_raspadores/se_areia_branca.csv
rm -rf data/
rm *.db
echo "Testando raspador para se_barra_dos_coqueiros..."
scrapy crawl se_barra_dos_coqueiros -a start=2025-05-15 --logfile=arquivos_raspadores/se_barra_dos_coqueiros.log -o arquivos_raspadores/se_barra_dos_coqueiros.csv
rm -rf data/
rm *.db
echo "Testando raspador para se_campo_do_brito..."
scrapy crawl se_campo_do_brito -a start=2025-05-15 --logfile=arquivos_raspadores/se_campo_do_brito.log -o arquivos_raspadores/se_campo_do_brito.csv
rm -rf data/
rm *.db
echo "Testando raspador para se_canhoba..."
scrapy crawl se_canhoba -a start=2025-05-15 --logfile=arquivos_raspadores/se_canhoba.log -o arquivos_raspadores/se_canhoba.csv
rm -rf data/
rm *.db
echo "Testando raspador para se_caninde_de_sao_francisco..."
scrapy crawl se_caninde_de_sao_francisco -a start=2025-05-15 --logfile=arquivos_raspadores/se_caninde_de_sao_francisco.log -o arquivos_raspadores/se_caninde_de_sao_francisco.csv
rm -rf data/
rm *.db
echo "Testando raspador para se_capela..."
scrapy crawl se_capela -a start=2025-05-15 --logfile=arquivos_raspadores/se_capela.log -o arquivos_raspadores/se_capela.csv
rm -rf data/
rm *.db
echo "Testando raspador para se_divina_pastora..."
scrapy crawl se_divina_pastora -a start=2025-05-15 --logfile=arquivos_raspadores/se_divina_pastora.log -o arquivos_raspadores/se_divina_pastora.csv
rm -rf data/
rm *.db
echo "Testando raspador para se_estancia..."
scrapy crawl se_estancia -a start=2025-05-15 --logfile=arquivos_raspadores/se_estancia.log -o arquivos_raspadores/se_estancia.csv
rm -rf data/
rm *.db
echo "Testando raspador para se_frei_paulo..."
scrapy crawl se_frei_paulo -a start=2025-05-15 --logfile=arquivos_raspadores/se_frei_paulo.log -o arquivos_raspadores/se_frei_paulo.csv
rm -rf data/
rm *.db
echo "Testando raspador para se_ilha_das_flores..."
scrapy crawl se_ilha_das_flores -a start=2025-05-15 --logfile=arquivos_raspadores/se_ilha_das_flores.log -o arquivos_raspadores/se_ilha_das_flores.csv
rm -rf data/
rm *.db
echo "Testando raspador para se_itabaiana..."
scrapy crawl se_itabaiana -a start=2025-05-15 --logfile=arquivos_raspadores/se_itabaiana.log -o arquivos_raspadores/se_itabaiana.csv
rm -rf data/
rm *.db
echo "Testando raspador para se_itabaianinha..."
scrapy crawl se_itabaianinha -a start=2025-05-15 --logfile=arquivos_raspadores/se_itabaianinha.log -o arquivos_raspadores/se_itabaianinha.csv
rm -rf data/
rm *.db
echo "Testando raspador para se_japaratuba..."
scrapy crawl se_japaratuba -a start=2025-05-15 --logfile=arquivos_raspadores/se_japaratuba.log -o arquivos_raspadores/se_japaratuba.csv
rm -rf data/
rm *.db
echo "Testando raspador para se_moita_bonita..."
scrapy crawl se_moita_bonita -a start=2025-05-15 --logfile=arquivos_raspadores/se_moita_bonita.log -o arquivos_raspadores/se_moita_bonita.csv
rm -rf data/
rm *.db
echo "Testando raspador para se_muribeca..."
scrapy crawl se_muribeca -a start=2025-05-15 --logfile=arquivos_raspadores/se_muribeca.log -o arquivos_raspadores/se_muribeca.csv
rm -rf data/
rm *.db
echo "Testando raspador para se_nossa_senhora_das_dores..."
scrapy crawl se_nossa_senhora_das_dores -a start=2025-05-15 --logfile=arquivos_raspadores/se_nossa_senhora_das_dores.log -o arquivos_raspadores/se_nossa_senhora_das_dores.csv
rm -rf data/
rm *.db
echo "Testando raspador para se_nossa_senhora_de_lourdes..."
scrapy crawl se_nossa_senhora_de_lourdes -a start=2025-05-15 --logfile=arquivos_raspadores/se_nossa_senhora_de_lourdes.log -o arquivos_raspadores/se_nossa_senhora_de_lourdes.csv
rm -rf data/
rm *.db
echo "Testando raspador para se_nossa_senhora_do_socorro..."
scrapy crawl se_nossa_senhora_do_socorro -a start=2025-05-15 --logfile=arquivos_raspadores/se_nossa_senhora_do_socorro.log -o arquivos_raspadores/se_nossa_senhora_do_socorro.csv
rm -rf data/
rm *.db
echo "Testando raspador para se_pedra_mole..."
scrapy crawl se_pedra_mole -a start=2025-05-15 --logfile=arquivos_raspadores/se_pedra_mole.log -o arquivos_raspadores/se_pedra_mole.csv
rm -rf data/
rm *.db
echo "Testando raspador para se_pirambu..."
scrapy crawl se_pirambu -a start=2025-05-15 --logfile=arquivos_raspadores/se_pirambu.log -o arquivos_raspadores/se_pirambu.csv
rm -rf data/
rm *.db
echo "Testando raspador para se_poco_verde..."
scrapy crawl se_poco_verde -a start=2025-05-15 --logfile=arquivos_raspadores/se_poco_verde.log -o arquivos_raspadores/se_poco_verde.csv
rm -rf data/
rm *.db
echo "Testando raspador para se_riachao_do_dantas..."
scrapy crawl se_riachao_do_dantas -a start=2025-05-15 --logfile=arquivos_raspadores/se_riachao_do_dantas.log -o arquivos_raspadores/se_riachao_do_dantas.csv
rm -rf data/
rm *.db
echo "Testando raspador para se_rosario_do_catete..."
scrapy crawl se_rosario_do_catete -a start=2025-05-15 --logfile=arquivos_raspadores/se_rosario_do_catete.log -o arquivos_raspadores/se_rosario_do_catete.csv
rm -rf data/
rm *.db
echo "Testando raspador para se_sao_domingos..."
scrapy crawl se_sao_domingos -a start=2025-05-15 --logfile=arquivos_raspadores/se_sao_domingos.log -o arquivos_raspadores/se_sao_domingos.csv
rm -rf data/
rm *.db
echo "Testando raspador para se_simao_dias..."
scrapy crawl se_simao_dias -a start=2025-05-15 --logfile=arquivos_raspadores/se_simao_dias.log -o arquivos_raspadores/se_simao_dias.csv
rm -rf data/
rm *.db
echo "Testando raspador para se_siriri..."
scrapy crawl se_siriri -a start=2025-05-15 --logfile=arquivos_raspadores/se_siriri.log -o arquivos_raspadores/se_siriri.csv
rm -rf data/
rm *.db
echo "Testando raspador para se_telha..."
scrapy crawl se_telha -a start=2025-05-15 --logfile=arquivos_raspadores/se_telha.log -o arquivos_raspadores/se_telha.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_adolfo..."
scrapy crawl sp_adolfo -a start=2025-05-15 --logfile=arquivos_raspadores/sp_adolfo.log -o arquivos_raspadores/sp_adolfo.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_aguai..."
scrapy crawl sp_aguai -a start=2025-05-15 --logfile=arquivos_raspadores/sp_aguai.log -o arquivos_raspadores/sp_aguai.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_aguas_da_prata..."
scrapy crawl sp_aguas_da_prata -a start=2025-05-15 --logfile=arquivos_raspadores/sp_aguas_da_prata.log -o arquivos_raspadores/sp_aguas_da_prata.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_aguas_de_sao_pedro..."
scrapy crawl sp_aguas_de_sao_pedro -a start=2025-05-15 --logfile=arquivos_raspadores/sp_aguas_de_sao_pedro.log -o arquivos_raspadores/sp_aguas_de_sao_pedro.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_alto_alegre..."
scrapy crawl sp_alto_alegre -a start=2025-05-15 --logfile=arquivos_raspadores/sp_alto_alegre.log -o arquivos_raspadores/sp_alto_alegre.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_alvares_florence..."
scrapy crawl sp_alvares_florence -a start=2025-05-15 --logfile=arquivos_raspadores/sp_alvares_florence.log -o arquivos_raspadores/sp_alvares_florence.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_andradina..."
scrapy crawl sp_andradina -a start=2025-05-15 --logfile=arquivos_raspadores/sp_andradina.log -o arquivos_raspadores/sp_andradina.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_aparecida..."
scrapy crawl sp_aparecida -a start=2025-05-15 --logfile=arquivos_raspadores/sp_aparecida.log -o arquivos_raspadores/sp_aparecida.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_aracariguama..."
scrapy crawl sp_aracariguama -a start=2025-05-15 --logfile=arquivos_raspadores/sp_aracariguama.log -o arquivos_raspadores/sp_aracariguama.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_aracatuba..."
scrapy crawl sp_aracatuba -a start=2025-05-15 --logfile=arquivos_raspadores/sp_aracatuba.log -o arquivos_raspadores/sp_aracatuba.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_arapei..."
scrapy crawl sp_arapei -a start=2025-05-15 --logfile=arquivos_raspadores/sp_arapei.log -o arquivos_raspadores/sp_arapei.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_avanhandava..."
scrapy crawl sp_avanhandava -a start=2025-05-15 --logfile=arquivos_raspadores/sp_avanhandava.log -o arquivos_raspadores/sp_avanhandava.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_avare..."
scrapy crawl sp_avare -a start=2025-05-15 --logfile=arquivos_raspadores/sp_avare.log -o arquivos_raspadores/sp_avare.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_barao_de_antonina..."
scrapy crawl sp_barao_de_antonina -a start=2025-05-15 --logfile=arquivos_raspadores/sp_barao_de_antonina.log -o arquivos_raspadores/sp_barao_de_antonina.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_barbosa..."
scrapy crawl sp_barbosa -a start=2025-05-15 --logfile=arquivos_raspadores/sp_barbosa.log -o arquivos_raspadores/sp_barbosa.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_birigui..."
scrapy crawl sp_birigui -a start=2025-05-15 --logfile=arquivos_raspadores/sp_birigui.log -o arquivos_raspadores/sp_birigui.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_botucatu..."
scrapy crawl sp_botucatu -a start=2025-05-15 --logfile=arquivos_raspadores/sp_botucatu.log -o arquivos_raspadores/sp_botucatu.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_braganca_paulista..."
scrapy crawl sp_braganca_paulista -a start=2025-05-15 --logfile=arquivos_raspadores/sp_braganca_paulista.log -o arquivos_raspadores/sp_braganca_paulista.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_brejo_alegre..."
scrapy crawl sp_brejo_alegre -a start=2025-05-15 --logfile=arquivos_raspadores/sp_brejo_alegre.log -o arquivos_raspadores/sp_brejo_alegre.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_cacapava..."
scrapy crawl sp_cacapava -a start=2025-05-15 --logfile=arquivos_raspadores/sp_cacapava.log -o arquivos_raspadores/sp_cacapava.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_campinas..."
scrapy crawl sp_campinas -a start=2025-05-15 --logfile=arquivos_raspadores/sp_campinas.log -o arquivos_raspadores/sp_campinas.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_campo_limpo_paulista..."
scrapy crawl sp_campo_limpo_paulista -a start=2025-05-15 --logfile=arquivos_raspadores/sp_campo_limpo_paulista.log -o arquivos_raspadores/sp_campo_limpo_paulista.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_catanduva..."
scrapy crawl sp_catanduva -a start=2025-05-15 --logfile=arquivos_raspadores/sp_catanduva.log -o arquivos_raspadores/sp_catanduva.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_charqueada..."
scrapy crawl sp_charqueada -a start=2025-05-15 --logfile=arquivos_raspadores/sp_charqueada.log -o arquivos_raspadores/sp_charqueada.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_coronel_macedo..."
scrapy crawl sp_coronel_macedo -a start=2025-05-15 --logfile=arquivos_raspadores/sp_coronel_macedo.log -o arquivos_raspadores/sp_coronel_macedo.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_cunha..."
scrapy crawl sp_cunha -a start=2025-05-15 --logfile=arquivos_raspadores/sp_cunha.log -o arquivos_raspadores/sp_cunha.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_dirce_reis..."
scrapy crawl sp_dirce_reis -a start=2025-05-15 --logfile=arquivos_raspadores/sp_dirce_reis.log -o arquivos_raspadores/sp_dirce_reis.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_dracena..."
scrapy crawl sp_dracena -a start=2025-05-15 --logfile=arquivos_raspadores/sp_dracena.log -o arquivos_raspadores/sp_dracena.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_eldorado..."
scrapy crawl sp_eldorado -a start=2025-05-15 --logfile=arquivos_raspadores/sp_eldorado.log -o arquivos_raspadores/sp_eldorado.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_floreal..."
scrapy crawl sp_floreal -a start=2025-05-15 --logfile=arquivos_raspadores/sp_floreal.log -o arquivos_raspadores/sp_floreal.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_general_salgado..."
scrapy crawl sp_general_salgado -a start=2025-05-15 --logfile=arquivos_raspadores/sp_general_salgado.log -o arquivos_raspadores/sp_general_salgado.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_glicerio..."
scrapy crawl sp_glicerio -a start=2025-05-15 --logfile=arquivos_raspadores/sp_glicerio.log -o arquivos_raspadores/sp_glicerio.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_guaracai..."
scrapy crawl sp_guaracai -a start=2025-05-15 --logfile=arquivos_raspadores/sp_guaracai.log -o arquivos_raspadores/sp_guaracai.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_guarulhos..."
scrapy crawl sp_guarulhos -a start=2025-05-15 --logfile=arquivos_raspadores/sp_guarulhos.log -o arquivos_raspadores/sp_guarulhos.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_ibitinga..."
scrapy crawl sp_ibitinga -a start=2025-05-15 --logfile=arquivos_raspadores/sp_ibitinga.log -o arquivos_raspadores/sp_ibitinga.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_iepe..."
scrapy crawl sp_iepe -a start=2025-05-15 --logfile=arquivos_raspadores/sp_iepe.log -o arquivos_raspadores/sp_iepe.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_igaracu_do_tiete..."
scrapy crawl sp_igaracu_do_tiete -a start=2025-05-15 --logfile=arquivos_raspadores/sp_igaracu_do_tiete.log -o arquivos_raspadores/sp_igaracu_do_tiete.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_iracemapolis..."
scrapy crawl sp_iracemapolis -a start=2025-05-15 --logfile=arquivos_raspadores/sp_iracemapolis.log -o arquivos_raspadores/sp_iracemapolis.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_irapuru..."
scrapy crawl sp_irapuru -a start=2025-05-15 --logfile=arquivos_raspadores/sp_irapuru.log -o arquivos_raspadores/sp_irapuru.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_itapeva..."
scrapy crawl sp_itapeva -a start=2025-05-15 --logfile=arquivos_raspadores/sp_itapeva.log -o arquivos_raspadores/sp_itapeva.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_itapevi..."
scrapy crawl sp_itapevi -a start=2025-05-15 --logfile=arquivos_raspadores/sp_itapevi.log -o arquivos_raspadores/sp_itapevi.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_itapirapua_paulista..."
scrapy crawl sp_itapirapua_paulista -a start=2025-05-15 --logfile=arquivos_raspadores/sp_itapirapua_paulista.log -o arquivos_raspadores/sp_itapirapua_paulista.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_itapolis..."
scrapy crawl sp_itapolis -a start=2025-05-15 --logfile=arquivos_raspadores/sp_itapolis.log -o arquivos_raspadores/sp_itapolis.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_itaporanga..."
scrapy crawl sp_itaporanga -a start=2025-05-15 --logfile=arquivos_raspadores/sp_itaporanga.log -o arquivos_raspadores/sp_itaporanga.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_itapui..."
scrapy crawl sp_itapui -a start=2025-05-15 --logfile=arquivos_raspadores/sp_itapui.log -o arquivos_raspadores/sp_itapui.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_itariri..."
scrapy crawl sp_itariri -a start=2025-05-15 --logfile=arquivos_raspadores/sp_itariri.log -o arquivos_raspadores/sp_itariri.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_itobi..."
scrapy crawl sp_itobi -a start=2025-05-15 --logfile=arquivos_raspadores/sp_itobi.log -o arquivos_raspadores/sp_itobi.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_itu..."
scrapy crawl sp_itu -a start=2025-05-15 --logfile=arquivos_raspadores/sp_itu.log -o arquivos_raspadores/sp_itu.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_jaboticabal..."
scrapy crawl sp_jaboticabal -a start=2025-05-15 --logfile=arquivos_raspadores/sp_jaboticabal.log -o arquivos_raspadores/sp_jaboticabal.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_jandira..."
scrapy crawl sp_jandira -a start=2025-05-15 --logfile=arquivos_raspadores/sp_jandira.log -o arquivos_raspadores/sp_jandira.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_jau_2023..."
scrapy crawl sp_jau_2023 -a start=2025-05-15 --logfile=arquivos_raspadores/sp_jau_2023.log -o arquivos_raspadores/sp_jau_2023.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_joanopolis..."
scrapy crawl sp_joanopolis -a start=2025-05-15 --logfile=arquivos_raspadores/sp_joanopolis.log -o arquivos_raspadores/sp_joanopolis.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_joao_ramalho..."
scrapy crawl sp_joao_ramalho -a start=2025-05-15 --logfile=arquivos_raspadores/sp_joao_ramalho.log -o arquivos_raspadores/sp_joao_ramalho.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_jundiai..."
scrapy crawl sp_jundiai -a start=2025-05-15 --logfile=arquivos_raspadores/sp_jundiai.log -o arquivos_raspadores/sp_jundiai.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_junqueiropolis..."
scrapy crawl sp_junqueiropolis -a start=2025-05-15 --logfile=arquivos_raspadores/sp_junqueiropolis.log -o arquivos_raspadores/sp_junqueiropolis.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_lagoinha..."
scrapy crawl sp_lagoinha -a start=2025-05-15 --logfile=arquivos_raspadores/sp_lagoinha.log -o arquivos_raspadores/sp_lagoinha.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_lavinia..."
scrapy crawl sp_lavinia -a start=2025-05-15 --logfile=arquivos_raspadores/sp_lavinia.log -o arquivos_raspadores/sp_lavinia.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_luiziania..."
scrapy crawl sp_luiziania -a start=2025-05-15 --logfile=arquivos_raspadores/sp_luiziania.log -o arquivos_raspadores/sp_luiziania.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_macatuba..."
scrapy crawl sp_macatuba -a start=2025-05-15 --logfile=arquivos_raspadores/sp_macatuba.log -o arquivos_raspadores/sp_macatuba.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_macaubal..."
scrapy crawl sp_macaubal -a start=2025-05-15 --logfile=arquivos_raspadores/sp_macaubal.log -o arquivos_raspadores/sp_macaubal.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_marilia..."
scrapy crawl sp_marilia -a start=2025-05-15 --logfile=arquivos_raspadores/sp_marilia.log -o arquivos_raspadores/sp_marilia.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_mira_estrela..."
scrapy crawl sp_mira_estrela -a start=2025-05-15 --logfile=arquivos_raspadores/sp_mira_estrela.log -o arquivos_raspadores/sp_mira_estrela.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_mirante_do_paranapanema..."
scrapy crawl sp_mirante_do_paranapanema -a start=2025-05-15 --logfile=arquivos_raspadores/sp_mirante_do_paranapanema.log -o arquivos_raspadores/sp_mirante_do_paranapanema.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_mogi_guacu..."
scrapy crawl sp_mogi_guacu -a start=2025-05-15 --logfile=arquivos_raspadores/sp_mogi_guacu.log -o arquivos_raspadores/sp_mogi_guacu.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_monte_alto_2017..."
scrapy crawl sp_monte_alto_2017 -a start=2025-05-15 --logfile=arquivos_raspadores/sp_monte_alto_2017.log -o arquivos_raspadores/sp_monte_alto_2017.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_monte_mor..."
scrapy crawl sp_monte_mor -a start=2025-05-15 --logfile=arquivos_raspadores/sp_monte_mor.log -o arquivos_raspadores/sp_monte_mor.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_monteiro_lobato..."
scrapy crawl sp_monteiro_lobato -a start=2025-05-15 --logfile=arquivos_raspadores/sp_monteiro_lobato.log -o arquivos_raspadores/sp_monteiro_lobato.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_nhandeara..."
scrapy crawl sp_nhandeara -a start=2025-05-15 --logfile=arquivos_raspadores/sp_nhandeara.log -o arquivos_raspadores/sp_nhandeara.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_nova_castilho..."
scrapy crawl sp_nova_castilho -a start=2025-05-15 --logfile=arquivos_raspadores/sp_nova_castilho.log -o arquivos_raspadores/sp_nova_castilho.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_nova_luzitania..."
scrapy crawl sp_nova_luzitania -a start=2025-05-15 --logfile=arquivos_raspadores/sp_nova_luzitania.log -o arquivos_raspadores/sp_nova_luzitania.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_osasco..."
scrapy crawl sp_osasco -a start=2025-05-15 --logfile=arquivos_raspadores/sp_osasco.log -o arquivos_raspadores/sp_osasco.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_ourinhos..."
scrapy crawl sp_ourinhos -a start=2025-05-15 --logfile=arquivos_raspadores/sp_ourinhos.log -o arquivos_raspadores/sp_ourinhos.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_palmital..."
scrapy crawl sp_palmital -a start=2025-05-15 --logfile=arquivos_raspadores/sp_palmital.log -o arquivos_raspadores/sp_palmital.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_parisi..."
scrapy crawl sp_parisi -a start=2025-05-15 --logfile=arquivos_raspadores/sp_parisi.log -o arquivos_raspadores/sp_parisi.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_patrocinio_paulista..."
scrapy crawl sp_patrocinio_paulista -a start=2025-05-15 --logfile=arquivos_raspadores/sp_patrocinio_paulista.log -o arquivos_raspadores/sp_patrocinio_paulista.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_paulinia..."
scrapy crawl sp_paulinia -a start=2025-05-15 --logfile=arquivos_raspadores/sp_paulinia.log -o arquivos_raspadores/sp_paulinia.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_penapolis..."
scrapy crawl sp_penapolis -a start=2025-05-15 --logfile=arquivos_raspadores/sp_penapolis.log -o arquivos_raspadores/sp_penapolis.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_piedade..."
scrapy crawl sp_piedade -a start=2025-05-15 --logfile=arquivos_raspadores/sp_piedade.log -o arquivos_raspadores/sp_piedade.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_pindorama..."
scrapy crawl sp_pindorama -a start=2025-05-15 --logfile=arquivos_raspadores/sp_pindorama.log -o arquivos_raspadores/sp_pindorama.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_planalto..."
scrapy crawl sp_planalto -a start=2025-05-15 --logfile=arquivos_raspadores/sp_planalto.log -o arquivos_raspadores/sp_planalto.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_poloni..."
scrapy crawl sp_poloni -a start=2025-05-15 --logfile=arquivos_raspadores/sp_poloni.log -o arquivos_raspadores/sp_poloni.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_pontes_gestal..."
scrapy crawl sp_pontes_gestal -a start=2025-05-15 --logfile=arquivos_raspadores/sp_pontes_gestal.log -o arquivos_raspadores/sp_pontes_gestal.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_porangaba..."
scrapy crawl sp_porangaba -a start=2025-05-15 --logfile=arquivos_raspadores/sp_porangaba.log -o arquivos_raspadores/sp_porangaba.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_potirendaba..."
scrapy crawl sp_potirendaba -a start=2025-05-15 --logfile=arquivos_raspadores/sp_potirendaba.log -o arquivos_raspadores/sp_potirendaba.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_pratania..."
scrapy crawl sp_pratania -a start=2025-05-15 --logfile=arquivos_raspadores/sp_pratania.log -o arquivos_raspadores/sp_pratania.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_presidente_epitacio..."
scrapy crawl sp_presidente_epitacio -a start=2025-05-15 --logfile=arquivos_raspadores/sp_presidente_epitacio.log -o arquivos_raspadores/sp_presidente_epitacio.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_rio_claro..."
scrapy crawl sp_rio_claro -a start=2025-05-15 --logfile=arquivos_raspadores/sp_rio_claro.log -o arquivos_raspadores/sp_rio_claro.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_salto..."
scrapy crawl sp_salto -a start=2025-05-15 --logfile=arquivos_raspadores/sp_salto.log -o arquivos_raspadores/sp_salto.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_santa_ernestina..."
scrapy crawl sp_santa_ernestina -a start=2025-05-15 --logfile=arquivos_raspadores/sp_santa_ernestina.log -o arquivos_raspadores/sp_santa_ernestina.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_santa_maria_da_serra..."
scrapy crawl sp_santa_maria_da_serra -a start=2025-05-15 --logfile=arquivos_raspadores/sp_santa_maria_da_serra.log -o arquivos_raspadores/sp_santa_maria_da_serra.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_santo_andre..."
scrapy crawl sp_santo_andre -a start=2025-05-15 --logfile=arquivos_raspadores/sp_santo_andre.log -o arquivos_raspadores/sp_santo_andre.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_santos..."
scrapy crawl sp_santos -a start=2025-05-15 --logfile=arquivos_raspadores/sp_santos.log -o arquivos_raspadores/sp_santos.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_sao_bernardo_do_campo..."
scrapy crawl sp_sao_bernardo_do_campo -a start=2025-05-15 --logfile=arquivos_raspadores/sp_sao_bernardo_do_campo.log -o arquivos_raspadores/sp_sao_bernardo_do_campo.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_sao_jose_dos_campos..."
scrapy crawl sp_sao_jose_dos_campos -a start=2025-05-15 --logfile=arquivos_raspadores/sp_sao_jose_dos_campos.log -o arquivos_raspadores/sp_sao_jose_dos_campos.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_sao_manuel..."
scrapy crawl sp_sao_manuel -a start=2025-05-15 --logfile=arquivos_raspadores/sp_sao_manuel.log -o arquivos_raspadores/sp_sao_manuel.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_sao_pedro..."
scrapy crawl sp_sao_pedro -a start=2025-05-15 --logfile=arquivos_raspadores/sp_sao_pedro.log -o arquivos_raspadores/sp_sao_pedro.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_sao_roque..."
scrapy crawl sp_sao_roque -a start=2025-05-15 --logfile=arquivos_raspadores/sp_sao_roque.log -o arquivos_raspadores/sp_sao_roque.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_sarutaia..."
scrapy crawl sp_sarutaia -a start=2025-05-15 --logfile=arquivos_raspadores/sp_sarutaia.log -o arquivos_raspadores/sp_sarutaia.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_sebastianopolis_do_sul..."
scrapy crawl sp_sebastianopolis_do_sul -a start=2025-05-15 --logfile=arquivos_raspadores/sp_sebastianopolis_do_sul.log -o arquivos_raspadores/sp_sebastianopolis_do_sul.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_sertaozinho..."
scrapy crawl sp_sertaozinho -a start=2025-05-15 --logfile=arquivos_raspadores/sp_sertaozinho.log -o arquivos_raspadores/sp_sertaozinho.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_sumare..."
scrapy crawl sp_sumare -a start=2025-05-15 --logfile=arquivos_raspadores/sp_sumare.log -o arquivos_raspadores/sp_sumare.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_tapirai..."
scrapy crawl sp_tapirai -a start=2025-05-15 --logfile=arquivos_raspadores/sp_tapirai.log -o arquivos_raspadores/sp_tapirai.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_taquaral..."
scrapy crawl sp_taquaral -a start=2025-05-15 --logfile=arquivos_raspadores/sp_taquaral.log -o arquivos_raspadores/sp_taquaral.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_taubate..."
scrapy crawl sp_taubate -a start=2025-05-15 --logfile=arquivos_raspadores/sp_taubate.log -o arquivos_raspadores/sp_taubate.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_terra_roxa..."
scrapy crawl sp_terra_roxa -a start=2025-05-15 --logfile=arquivos_raspadores/sp_terra_roxa.log -o arquivos_raspadores/sp_terra_roxa.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_tremembe..."
scrapy crawl sp_tremembe -a start=2025-05-15 --logfile=arquivos_raspadores/sp_tremembe.log -o arquivos_raspadores/sp_tremembe.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_turiuba..."
scrapy crawl sp_turiuba -a start=2025-05-15 --logfile=arquivos_raspadores/sp_turiuba.log -o arquivos_raspadores/sp_turiuba.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_uniao_paulista..."
scrapy crawl sp_uniao_paulista -a start=2025-05-15 --logfile=arquivos_raspadores/sp_uniao_paulista.log -o arquivos_raspadores/sp_uniao_paulista.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_valinhos..."
scrapy crawl sp_valinhos -a start=2025-05-15 --logfile=arquivos_raspadores/sp_valinhos.log -o arquivos_raspadores/sp_valinhos.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_valparaiso..."
scrapy crawl sp_valparaiso -a start=2025-05-15 --logfile=arquivos_raspadores/sp_valparaiso.log -o arquivos_raspadores/sp_valparaiso.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_vera_cruz..."
scrapy crawl sp_vera_cruz -a start=2025-05-15 --logfile=arquivos_raspadores/sp_vera_cruz.log -o arquivos_raspadores/sp_vera_cruz.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_vinhedo..."
scrapy crawl sp_vinhedo -a start=2025-05-15 --logfile=arquivos_raspadores/sp_vinhedo.log -o arquivos_raspadores/sp_vinhedo.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_votorantim..."
scrapy crawl sp_votorantim -a start=2025-05-15 --logfile=arquivos_raspadores/sp_votorantim.log -o arquivos_raspadores/sp_votorantim.csv
rm -rf data/
rm *.db
echo "Testando raspador para sp_votuporanga..."
scrapy crawl sp_votuporanga -a start=2025-05-15 --logfile=arquivos_raspadores/sp_votuporanga.log -o arquivos_raspadores/sp_votuporanga.csv
rm -rf data/
rm *.db
echo "Testando raspador para to_aguiarnopolis..."
scrapy crawl to_aguiarnopolis -a start=2025-05-15 --logfile=arquivos_raspadores/to_aguiarnopolis.log -o arquivos_raspadores/to_aguiarnopolis.csv
rm -rf data/
rm *.db
echo "Testando raspador para to_aparecida_do_rio_negro..."
scrapy crawl to_aparecida_do_rio_negro -a start=2025-05-15 --logfile=arquivos_raspadores/to_aparecida_do_rio_negro.log -o arquivos_raspadores/to_aparecida_do_rio_negro.csv
rm -rf data/
rm *.db
echo "Testando raspador para to_araguaina..."
scrapy crawl to_araguaina -a start=2025-05-15 --logfile=arquivos_raspadores/to_araguaina.log -o arquivos_raspadores/to_araguaina.csv
rm -rf data/
rm *.db
echo "Testando raspador para to_axixa_do_tocantins..."
scrapy crawl to_axixa_do_tocantins -a start=2025-05-15 --logfile=arquivos_raspadores/to_axixa_do_tocantins.log -o arquivos_raspadores/to_axixa_do_tocantins.csv
rm -rf data/
rm *.db
echo "Testando raspador para to_campos_lindos..."
scrapy crawl to_campos_lindos -a start=2025-05-15 --logfile=arquivos_raspadores/to_campos_lindos.log -o arquivos_raspadores/to_campos_lindos.csv
rm -rf data/
rm *.db
echo "Testando raspador para to_caseara..."
scrapy crawl to_caseara -a start=2025-05-15 --logfile=arquivos_raspadores/to_caseara.log -o arquivos_raspadores/to_caseara.csv
rm -rf data/
rm *.db
echo "Testando raspador para to_centenario..."
scrapy crawl to_centenario -a start=2025-05-15 --logfile=arquivos_raspadores/to_centenario.log -o arquivos_raspadores/to_centenario.csv
rm -rf data/
rm *.db
echo "Testando raspador para to_divinopolis_do_tocantins..."
scrapy crawl to_divinopolis_do_tocantins -a start=2025-05-15 --logfile=arquivos_raspadores/to_divinopolis_do_tocantins.log -o arquivos_raspadores/to_divinopolis_do_tocantins.csv
rm -rf data/
rm *.db
echo "Testando raspador para to_goiatins..."
scrapy crawl to_goiatins -a start=2025-05-15 --logfile=arquivos_raspadores/to_goiatins.log -o arquivos_raspadores/to_goiatins.csv
rm -rf data/
rm *.db
echo "Testando raspador para to_gurupi..."
scrapy crawl to_gurupi -a start=2025-05-15 --logfile=arquivos_raspadores/to_gurupi.log -o arquivos_raspadores/to_gurupi.csv
rm -rf data/
rm *.db
echo "Testando raspador para to_lagoa_da_confusao..."
scrapy crawl to_lagoa_da_confusao -a start=2025-05-15 --logfile=arquivos_raspadores/to_lagoa_da_confusao.log -o arquivos_raspadores/to_lagoa_da_confusao.csv
rm -rf data/
rm *.db
echo "Testando raspador para to_lagoa_do_tocantins..."
scrapy crawl to_lagoa_do_tocantins -a start=2025-05-15 --logfile=arquivos_raspadores/to_lagoa_do_tocantins.log -o arquivos_raspadores/to_lagoa_do_tocantins.csv
rm -rf data/
rm *.db
echo "Testando raspador para to_miracema_do_tocantins..."
scrapy crawl to_miracema_do_tocantins -a start=2025-05-15 --logfile=arquivos_raspadores/to_miracema_do_tocantins.log -o arquivos_raspadores/to_miracema_do_tocantins.csv
rm -rf data/
rm *.db
echo "Testando raspador para to_muricilandia..."
scrapy crawl to_muricilandia -a start=2025-05-15 --logfile=arquivos_raspadores/to_muricilandia.log -o arquivos_raspadores/to_muricilandia.csv
rm -rf data/
rm *.db
echo "Testando raspador para to_nazare..."
scrapy crawl to_nazare -a start=2025-05-15 --logfile=arquivos_raspadores/to_nazare.log -o arquivos_raspadores/to_nazare.csv
rm -rf data/
rm *.db
echo "Testando raspador para to_palmas..."
scrapy crawl to_palmas -a start=2025-05-15 --logfile=arquivos_raspadores/to_palmas.log -o arquivos_raspadores/to_palmas.csv
rm -rf data/
rm *.db
echo "Testando raspador para to_peixe..."
scrapy crawl to_peixe -a start=2025-05-15 --logfile=arquivos_raspadores/to_peixe.log -o arquivos_raspadores/to_peixe.csv
rm -rf data/
rm *.db
echo "Testando raspador para to_ponte_alta_do_tocantins..."
scrapy crawl to_ponte_alta_do_tocantins -a start=2025-05-15 --logfile=arquivos_raspadores/to_ponte_alta_do_tocantins.log -o arquivos_raspadores/to_ponte_alta_do_tocantins.csv
rm -rf data/
rm *.db
echo "Testando raspador para to_pugmil..."
scrapy crawl to_pugmil -a start=2025-05-15 --logfile=arquivos_raspadores/to_pugmil.log -o arquivos_raspadores/to_pugmil.csv
rm -rf data/
rm *.db
echo "Testando raspador para to_recursolandia..."
scrapy crawl to_recursolandia -a start=2025-05-15 --logfile=arquivos_raspadores/to_recursolandia.log -o arquivos_raspadores/to_recursolandia.csv
rm -rf data/
rm *.db
echo "Testando raspador para to_sampaio..."
scrapy crawl to_sampaio -a start=2025-05-15 --logfile=arquivos_raspadores/to_sampaio.log -o arquivos_raspadores/to_sampaio.csv
rm -rf data/
rm *.db
echo "Testando raspador para to_santa_fe_do_araguaia..."
scrapy crawl to_santa_fe_do_araguaia -a start=2025-05-15 --logfile=arquivos_raspadores/to_santa_fe_do_araguaia.log -o arquivos_raspadores/to_santa_fe_do_araguaia.csv
rm -rf data/
rm *.db
echo "Testando raspador para to_talisma..."
scrapy crawl to_talisma -a start=2025-05-15 --logfile=arquivos_raspadores/to_talisma.log -o arquivos_raspadores/to_talisma.csv
rm -rf data/
rm *.db
echo "Testando raspador para to_tocantinia..."
scrapy crawl to_tocantinia -a start=2025-05-15 --logfile=arquivos_raspadores/to_tocantinia.log -o arquivos_raspadores/to_tocantinia.csv
rm -rf data/
rm *.db
echo "Testando raspador para to_tocantinopolis..."
scrapy crawl to_tocantinopolis -a start=2025-05-15 --logfile=arquivos_raspadores/to_tocantinopolis.log -o arquivos_raspadores/to_tocantinopolis.csv
rm -rf data/
rm *.db
echo "Testando raspador para to_tupirama..."
scrapy crawl to_tupirama -a start=2025-05-15 --logfile=arquivos_raspadores/to_tupirama.log -o arquivos_raspadores/to_tupirama.csv
rm -rf data/
rm *.db
