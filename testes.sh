cd data_collection
rm *.log
rm *.csv
rm *.db

echo "------------------------------------------------ TESTANDO RASPADOR al_associacao_municipios ------------------------------------------------"
scrapy crawl al_associacao_municipios -a start=2025-04-28 -o al_associacao_municipios.csv --logfile=al_associacao_municipios.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR al_igaci ------------------------------------------------"
scrapy crawl al_igaci -a start=2025-04-28 -o al_igaci.csv --logfile=al_igaci.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR al_maceio ------------------------------------------------"
scrapy crawl al_maceio -a start=2025-04-28 -o al_maceio.csv --logfile=al_maceio.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR al_maragogi ------------------------------------------------"
scrapy crawl al_maragogi -a start=2025-04-28 -o al_maragogi.csv --logfile=al_maragogi.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR am_associacao_municipios ------------------------------------------------"
scrapy crawl am_associacao_municipios -a start=2025-04-28 -o am_associacao_municipios.csv --logfile=am_associacao_municipios.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR am_manaus ------------------------------------------------"
scrapy crawl am_manaus -a start=2025-04-28 -o am_manaus.csv --logfile=am_manaus.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ap_macapa ------------------------------------------------"
scrapy crawl ap_macapa -a start=2025-04-28 -o ap_macapa.csv --logfile=ap_macapa.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ap_santana ------------------------------------------------"
scrapy crawl ap_santana -a start=2025-04-28 -o ap_santana.csv --logfile=ap_santana.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ap_tartarugalzinho ------------------------------------------------"
scrapy crawl ap_tartarugalzinho -a start=2025-04-28 -o ap_tartarugalzinho.csv --logfile=ap_tartarugalzinho.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ba_abare ------------------------------------------------"
scrapy crawl ba_abare -a start=2025-04-28 -o ba_abare.csv --logfile=ba_abare.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ba_acajutiba ------------------------------------------------"
scrapy crawl ba_acajutiba -a start=2025-04-28 -o ba_acajutiba.csv --logfile=ba_acajutiba.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ba_adustina ------------------------------------------------"
scrapy crawl ba_adustina -a start=2025-04-28 -o ba_adustina.csv --logfile=ba_adustina.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ba_alagoinhas ------------------------------------------------"
scrapy crawl ba_alagoinhas -a start=2025-04-28 -o ba_alagoinhas.csv --logfile=ba_alagoinhas.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ba_alcobaca ------------------------------------------------"
scrapy crawl ba_alcobaca -a start=2025-04-28 -o ba_alcobaca.csv --logfile=ba_alcobaca.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ba_almadina ------------------------------------------------"
scrapy crawl ba_almadina -a start=2025-04-28 -o ba_almadina.csv --logfile=ba_almadina.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ba_amelia_rodrigues ------------------------------------------------"
scrapy crawl ba_amelia_rodrigues -a start=2025-04-28 -o ba_amelia_rodrigues.csv --logfile=ba_amelia_rodrigues.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ba_anage ------------------------------------------------"
scrapy crawl ba_anage -a start=2025-04-28 -o ba_anage.csv --logfile=ba_anage.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ba_andorinha ------------------------------------------------"
scrapy crawl ba_andorinha -a start=2025-04-28 -o ba_andorinha.csv --logfile=ba_andorinha.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ba_angical ------------------------------------------------"
scrapy crawl ba_angical -a start=2025-04-28 -o ba_angical.csv --logfile=ba_angical.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ba_antas ------------------------------------------------"
scrapy crawl ba_antas -a start=2025-04-28 -o ba_antas.csv --logfile=ba_antas.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ba_antonio_cardoso_2017 ------------------------------------------------"
scrapy crawl ba_antonio_cardoso_2017 -a start=2025-04-28 -o ba_antonio_cardoso_2017.csv --logfile=ba_antonio_cardoso_2017.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ba_apuarema ------------------------------------------------"
scrapy crawl ba_apuarema -a start=2025-04-28 -o ba_apuarema.csv --logfile=ba_apuarema.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ba_aracas ------------------------------------------------"
scrapy crawl ba_aracas -a start=2025-04-28 -o ba_aracas.csv --logfile=ba_aracas.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ba_aramari ------------------------------------------------"
scrapy crawl ba_aramari -a start=2025-04-28 -o ba_aramari.csv --logfile=ba_aramari.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ba_arataca ------------------------------------------------"
scrapy crawl ba_arataca -a start=2025-04-28 -o ba_arataca.csv --logfile=ba_arataca.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ba_associacao_municipios ------------------------------------------------"
scrapy crawl ba_associacao_municipios -a start=2025-04-28 -o ba_associacao_municipios.csv --logfile=ba_associacao_municipios.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ba_banzae ------------------------------------------------"
scrapy crawl ba_banzae -a start=2025-04-28 -o ba_banzae.csv --logfile=ba_banzae.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ba_barra_do_choca_2017 ------------------------------------------------"
scrapy crawl ba_barra_do_choca_2017 -a start=2025-04-28 -o ba_barra_do_choca_2017.csv --logfile=ba_barra_do_choca_2017.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ba_barreiras ------------------------------------------------"
scrapy crawl ba_barreiras -a start=2025-04-28 -o ba_barreiras.csv --logfile=ba_barreiras.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ba_barrocas_2017 ------------------------------------------------"
scrapy crawl ba_barrocas_2017 -a start=2025-04-28 -o ba_barrocas_2017.csv --logfile=ba_barrocas_2017.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ba_brotas_de_macaubas ------------------------------------------------"
scrapy crawl ba_brotas_de_macaubas -a start=2025-04-28 -o ba_brotas_de_macaubas.csv --logfile=ba_brotas_de_macaubas.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ba_cachoeira_2017 ------------------------------------------------"
scrapy crawl ba_cachoeira_2017 -a start=2025-04-28 -o ba_cachoeira_2017.csv --logfile=ba_cachoeira_2017.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ba_cacule_2014 ------------------------------------------------"
scrapy crawl ba_cacule_2014 -a start=2025-04-28 -o ba_cacule_2014.csv --logfile=ba_cacule_2014.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ba_caetite ------------------------------------------------"
scrapy crawl ba_caetite -a start=2025-04-28 -o ba_caetite.csv --logfile=ba_caetite.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ba_camamu_2017 ------------------------------------------------"
scrapy crawl ba_camamu_2017 -a start=2025-04-28 -o ba_camamu_2017.csv --logfile=ba_camamu_2017.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ba_campo_alegre_de_lourdes ------------------------------------------------"
scrapy crawl ba_campo_alegre_de_lourdes -a start=2025-04-28 -o ba_campo_alegre_de_lourdes.csv --logfile=ba_campo_alegre_de_lourdes.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ba_campo_formoso ------------------------------------------------"
scrapy crawl ba_campo_formoso -a start=2025-04-28 -o ba_campo_formoso.csv --logfile=ba_campo_formoso.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ba_canudos ------------------------------------------------"
scrapy crawl ba_canudos -a start=2025-04-28 -o ba_canudos.csv --logfile=ba_canudos.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ba_catolandia_2015 ------------------------------------------------"
scrapy crawl ba_catolandia_2015 -a start=2025-04-28 -o ba_catolandia_2015.csv --logfile=ba_catolandia_2015.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ba_catu_2014 ------------------------------------------------"
scrapy crawl ba_catu_2014 -a start=2025-04-28 -o ba_catu_2014.csv --logfile=ba_catu_2014.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ba_cicero_dantas ------------------------------------------------"
scrapy crawl ba_cicero_dantas -a start=2025-04-28 -o ba_cicero_dantas.csv --logfile=ba_cicero_dantas.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ba_cipo ------------------------------------------------"
scrapy crawl ba_cipo -a start=2025-04-28 -o ba_cipo.csv --logfile=ba_cipo.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ba_conceicao_do_almeida ------------------------------------------------"
scrapy crawl ba_conceicao_do_almeida -a start=2025-04-28 -o ba_conceicao_do_almeida.csv --logfile=ba_conceicao_do_almeida.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ba_correntina_2007 ------------------------------------------------"
scrapy crawl ba_correntina_2007 -a start=2025-04-28 -o ba_correntina_2007.csv --logfile=ba_correntina_2007.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ba_correntina_2025 ------------------------------------------------"
scrapy crawl ba_correntina_2025 -a start=2025-04-28 -o ba_correntina_2025.csv --logfile=ba_correntina_2025.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ba_cotegipe ------------------------------------------------"
scrapy crawl ba_cotegipe -a start=2025-04-28 -o ba_cotegipe.csv --logfile=ba_cotegipe.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ba_cristopolis ------------------------------------------------"
scrapy crawl ba_cristopolis -a start=2025-04-28 -o ba_cristopolis.csv --logfile=ba_cristopolis.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ba_cruz_das_almas ------------------------------------------------"
scrapy crawl ba_cruz_das_almas -a start=2025-04-28 -o ba_cruz_das_almas.csv --logfile=ba_cruz_das_almas.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ba_esplanada ------------------------------------------------"
scrapy crawl ba_esplanada -a start=2025-04-28 -o ba_esplanada.csv --logfile=ba_esplanada.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ba_feira_de_santana ------------------------------------------------"
scrapy crawl ba_feira_de_santana -a start=2025-04-28 -o ba_feira_de_santana.csv --logfile=ba_feira_de_santana.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ba_floresta_azul_2017 ------------------------------------------------"
scrapy crawl ba_floresta_azul_2017 -a start=2025-04-28 -o ba_floresta_azul_2017.csv --logfile=ba_floresta_azul_2017.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ba_formosa_do_rio_preto ------------------------------------------------"
scrapy crawl ba_formosa_do_rio_preto -a start=2025-04-28 -o ba_formosa_do_rio_preto.csv --logfile=ba_formosa_do_rio_preto.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ba_gentio_do_ouro ------------------------------------------------"
scrapy crawl ba_gentio_do_ouro -a start=2025-04-28 -o ba_gentio_do_ouro.csv --logfile=ba_gentio_do_ouro.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ba_gongogi ------------------------------------------------"
scrapy crawl ba_gongogi -a start=2025-04-28 -o ba_gongogi.csv --logfile=ba_gongogi.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ba_governador_mangabeira ------------------------------------------------"
scrapy crawl ba_governador_mangabeira -a start=2025-04-28 -o ba_governador_mangabeira.csv --logfile=ba_governador_mangabeira.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ba_inhambupe ------------------------------------------------"
scrapy crawl ba_inhambupe -a start=2025-04-28 -o ba_inhambupe.csv --logfile=ba_inhambupe.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ba_ipiau ------------------------------------------------"
scrapy crawl ba_ipiau -a start=2025-04-28 -o ba_ipiau.csv --logfile=ba_ipiau.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ba_irara ------------------------------------------------"
scrapy crawl ba_irara -a start=2025-04-28 -o ba_irara.csv --logfile=ba_irara.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ba_itaberaba ------------------------------------------------"
scrapy crawl ba_itaberaba -a start=2025-04-28 -o ba_itaberaba.csv --logfile=ba_itaberaba.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ba_itamaraju ------------------------------------------------"
scrapy crawl ba_itamaraju -a start=2025-04-28 -o ba_itamaraju.csv --logfile=ba_itamaraju.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ba_itapetinga ------------------------------------------------"
scrapy crawl ba_itapetinga -a start=2025-04-28 -o ba_itapetinga.csv --logfile=ba_itapetinga.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ba_itapicuru ------------------------------------------------"
scrapy crawl ba_itapicuru -a start=2025-04-28 -o ba_itapicuru.csv --logfile=ba_itapicuru.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ba_itaquara ------------------------------------------------"
scrapy crawl ba_itaquara -a start=2025-04-28 -o ba_itaquara.csv --logfile=ba_itaquara.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ba_itatim ------------------------------------------------"
scrapy crawl ba_itatim -a start=2025-04-28 -o ba_itatim.csv --logfile=ba_itatim.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ba_ituacu ------------------------------------------------"
scrapy crawl ba_ituacu -a start=2025-04-28 -o ba_ituacu.csv --logfile=ba_ituacu.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ba_jaborandi ------------------------------------------------"
scrapy crawl ba_jaborandi -a start=2025-04-28 -o ba_jaborandi.csv --logfile=ba_jaborandi.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ba_jaguaquara ------------------------------------------------"
scrapy crawl ba_jaguaquara -a start=2025-04-28 -o ba_jaguaquara.csv --logfile=ba_jaguaquara.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ba_jaguarari ------------------------------------------------"
scrapy crawl ba_jaguarari -a start=2025-04-28 -o ba_jaguarari.csv --logfile=ba_jaguarari.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ba_jeremoabo ------------------------------------------------"
scrapy crawl ba_jeremoabo -a start=2025-04-28 -o ba_jeremoabo.csv --logfile=ba_jeremoabo.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ba_juazeiro ------------------------------------------------"
scrapy crawl ba_juazeiro -a start=2025-04-28 -o ba_juazeiro.csv --logfile=ba_juazeiro.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ba_laje ------------------------------------------------"
scrapy crawl ba_laje -a start=2025-04-28 -o ba_laje.csv --logfile=ba_laje.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ba_lajedao ------------------------------------------------"
scrapy crawl ba_lajedao -a start=2025-04-28 -o ba_lajedao.csv --logfile=ba_lajedao.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ba_lauro_de_freitas ------------------------------------------------"
scrapy crawl ba_lauro_de_freitas -a start=2025-04-28 -o ba_lauro_de_freitas.csv --logfile=ba_lauro_de_freitas.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ba_luis_eduardo_magalhaes ------------------------------------------------"
scrapy crawl ba_luis_eduardo_magalhaes -a start=2025-04-28 -o ba_luis_eduardo_magalhaes.csv --logfile=ba_luis_eduardo_magalhaes.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ba_macajuba ------------------------------------------------"
scrapy crawl ba_macajuba -a start=2025-04-28 -o ba_macajuba.csv --logfile=ba_macajuba.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ba_maragogipe ------------------------------------------------"
scrapy crawl ba_maragogipe -a start=2025-04-28 -o ba_maragogipe.csv --logfile=ba_maragogipe.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ba_mascote ------------------------------------------------"
scrapy crawl ba_mascote -a start=2025-04-28 -o ba_mascote.csv --logfile=ba_mascote.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ba_medeiros_neto_2018 ------------------------------------------------"
scrapy crawl ba_medeiros_neto_2018 -a start=2025-04-28 -o ba_medeiros_neto_2018.csv --logfile=ba_medeiros_neto_2018.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ba_monte_santo ------------------------------------------------"
scrapy crawl ba_monte_santo -a start=2025-04-28 -o ba_monte_santo.csv --logfile=ba_monte_santo.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ba_morro_do_chapeu ------------------------------------------------"
scrapy crawl ba_morro_do_chapeu -a start=2025-04-28 -o ba_morro_do_chapeu.csv --logfile=ba_morro_do_chapeu.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ba_mucuri ------------------------------------------------"
scrapy crawl ba_mucuri -a start=2025-04-28 -o ba_mucuri.csv --logfile=ba_mucuri.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ba_muniz_ferreira ------------------------------------------------"
scrapy crawl ba_muniz_ferreira -a start=2025-04-28 -o ba_muniz_ferreira.csv --logfile=ba_muniz_ferreira.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ba_paratinga ------------------------------------------------"
scrapy crawl ba_paratinga -a start=2025-04-28 -o ba_paratinga.csv --logfile=ba_paratinga.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ba_pe_de_serra ------------------------------------------------"
scrapy crawl ba_pe_de_serra -a start=2025-04-28 -o ba_pe_de_serra.csv --logfile=ba_pe_de_serra.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ba_prado ------------------------------------------------"
scrapy crawl ba_prado -a start=2025-04-28 -o ba_prado.csv --logfile=ba_prado.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ba_riachao_das_neves ------------------------------------------------"
scrapy crawl ba_riachao_das_neves -a start=2025-04-28 -o ba_riachao_das_neves.csv --logfile=ba_riachao_das_neves.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ba_ribeira_do_pombal_2014 ------------------------------------------------"
scrapy crawl ba_ribeira_do_pombal_2014 -a start=2025-04-28 -o ba_ribeira_do_pombal_2014.csv --logfile=ba_ribeira_do_pombal_2014.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ba_salvador ------------------------------------------------"
scrapy crawl ba_salvador -a start=2025-04-28 -o ba_salvador.csv --logfile=ba_salvador.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ba_santa_cruz_cabralia ------------------------------------------------"
scrapy crawl ba_santa_cruz_cabralia -a start=2025-04-28 -o ba_santa_cruz_cabralia.csv --logfile=ba_santa_cruz_cabralia.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ba_santa_luzia_2021 ------------------------------------------------"
scrapy crawl ba_santa_luzia_2021 -a start=2025-04-28 -o ba_santa_luzia_2021.csv --logfile=ba_santa_luzia_2021.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ba_santa_luzia_2024 ------------------------------------------------"
scrapy crawl ba_santa_luzia_2024 -a start=2025-04-28 -o ba_santa_luzia_2024.csv --logfile=ba_santa_luzia_2024.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ba_santa_rita_de_cassia ------------------------------------------------"
scrapy crawl ba_santa_rita_de_cassia -a start=2025-04-28 -o ba_santa_rita_de_cassia.csv --logfile=ba_santa_rita_de_cassia.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ba_santo_amaro_2012 ------------------------------------------------"
scrapy crawl ba_santo_amaro_2012 -a start=2025-04-28 -o ba_santo_amaro_2012.csv --logfile=ba_santo_amaro_2012.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ba_santo_estevao ------------------------------------------------"
scrapy crawl ba_santo_estevao -a start=2025-04-28 -o ba_santo_estevao.csv --logfile=ba_santo_estevao.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ba_sao_felipe ------------------------------------------------"
scrapy crawl ba_sao_felipe -a start=2025-04-28 -o ba_sao_felipe.csv --logfile=ba_sao_felipe.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ba_sao_felix ------------------------------------------------"
scrapy crawl ba_sao_felix -a start=2025-04-28 -o ba_sao_felix.csv --logfile=ba_sao_felix.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ba_sao_francisco_do_conde ------------------------------------------------"
scrapy crawl ba_sao_francisco_do_conde -a start=2025-04-28 -o ba_sao_francisco_do_conde.csv --logfile=ba_sao_francisco_do_conde.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ba_sao_miguel_das_matas ------------------------------------------------"
scrapy crawl ba_sao_miguel_das_matas -a start=2025-04-28 -o ba_sao_miguel_das_matas.csv --logfile=ba_sao_miguel_das_matas.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ba_sapeacu ------------------------------------------------"
scrapy crawl ba_sapeacu -a start=2025-04-28 -o ba_sapeacu.csv --logfile=ba_sapeacu.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ba_satiro_dias ------------------------------------------------"
scrapy crawl ba_satiro_dias -a start=2025-04-28 -o ba_satiro_dias.csv --logfile=ba_satiro_dias.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ba_saude ------------------------------------------------"
scrapy crawl ba_saude -a start=2025-04-28 -o ba_saude.csv --logfile=ba_saude.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ba_senhor_do_bonfim ------------------------------------------------"
scrapy crawl ba_senhor_do_bonfim -a start=2025-04-28 -o ba_senhor_do_bonfim.csv --logfile=ba_senhor_do_bonfim.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ba_sento_se ------------------------------------------------"
scrapy crawl ba_sento_se -a start=2025-04-28 -o ba_sento_se.csv --logfile=ba_sento_se.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ba_serrinha ------------------------------------------------"
scrapy crawl ba_serrinha -a start=2025-04-28 -o ba_serrinha.csv --logfile=ba_serrinha.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ba_tabocas_do_brejo_velho_2013 ------------------------------------------------"
scrapy crawl ba_tabocas_do_brejo_velho_2013 -a start=2025-04-28 -o ba_tabocas_do_brejo_velho_2013.csv --logfile=ba_tabocas_do_brejo_velho_2013.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ba_tapiramuta ------------------------------------------------"
scrapy crawl ba_tapiramuta -a start=2025-04-28 -o ba_tapiramuta.csv --logfile=ba_tapiramuta.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ba_teixeira_de_freitas_2021 ------------------------------------------------"
scrapy crawl ba_teixeira_de_freitas_2021 -a start=2025-04-28 -o ba_teixeira_de_freitas_2021.csv --logfile=ba_teixeira_de_freitas_2021.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ba_teolandia ------------------------------------------------"
scrapy crawl ba_teolandia -a start=2025-04-28 -o ba_teolandia.csv --logfile=ba_teolandia.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ba_tucano ------------------------------------------------"
scrapy crawl ba_tucano -a start=2025-04-28 -o ba_tucano.csv --logfile=ba_tucano.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ba_vera_cruz ------------------------------------------------"
scrapy crawl ba_vera_cruz -a start=2025-04-28 -o ba_vera_cruz.csv --logfile=ba_vera_cruz.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ba_vitoria_da_conquista ------------------------------------------------"
scrapy crawl ba_vitoria_da_conquista -a start=2025-04-28 -o ba_vitoria_da_conquista.csv --logfile=ba_vitoria_da_conquista.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ba_wenceslau_guimaraes ------------------------------------------------"
scrapy crawl ba_wenceslau_guimaraes -a start=2025-04-28 -o ba_wenceslau_guimaraes.csv --logfile=ba_wenceslau_guimaraes.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ba_xique_xique ------------------------------------------------"
scrapy crawl ba_xique_xique -a start=2025-04-28 -o ba_xique_xique.csv --logfile=ba_xique_xique.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ce_associacao_municipios ------------------------------------------------"
scrapy crawl ce_associacao_municipios -a start=2025-04-28 -o ce_associacao_municipios.csv --logfile=ce_associacao_municipios.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ce_aurora ------------------------------------------------"
scrapy crawl ce_aurora -a start=2025-04-28 -o ce_aurora.csv --logfile=ce_aurora.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ce_caninde ------------------------------------------------"
scrapy crawl ce_caninde -a start=2025-04-28 -o ce_caninde.csv --logfile=ce_caninde.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ce_caririacu ------------------------------------------------"
scrapy crawl ce_caririacu -a start=2025-04-28 -o ce_caririacu.csv --logfile=ce_caririacu.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ce_caucaia ------------------------------------------------"
scrapy crawl ce_caucaia -a start=2025-04-28 -o ce_caucaia.csv --logfile=ce_caucaia.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ce_cedro ------------------------------------------------"
scrapy crawl ce_cedro -a start=2025-04-28 -o ce_cedro.csv --logfile=ce_cedro.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ce_coreau ------------------------------------------------"
scrapy crawl ce_coreau -a start=2025-04-28 -o ce_coreau.csv --logfile=ce_coreau.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ce_crateus ------------------------------------------------"
scrapy crawl ce_crateus -a start=2025-04-28 -o ce_crateus.csv --logfile=ce_crateus.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ce_fortaleza ------------------------------------------------"
scrapy crawl ce_fortaleza -a start=2025-04-28 -o ce_fortaleza.csv --logfile=ce_fortaleza.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ce_general_sampaio ------------------------------------------------"
scrapy crawl ce_general_sampaio -a start=2025-04-28 -o ce_general_sampaio.csv --logfile=ce_general_sampaio.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ce_hidrolandia ------------------------------------------------"
scrapy crawl ce_hidrolandia -a start=2025-04-28 -o ce_hidrolandia.csv --logfile=ce_hidrolandia.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ce_horizonte ------------------------------------------------"
scrapy crawl ce_horizonte -a start=2025-04-28 -o ce_horizonte.csv --logfile=ce_horizonte.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ce_itaitinga ------------------------------------------------"
scrapy crawl ce_itaitinga -a start=2025-04-28 -o ce_itaitinga.csv --logfile=ce_itaitinga.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ce_jaguaribe ------------------------------------------------"
scrapy crawl ce_jaguaribe -a start=2025-04-28 -o ce_jaguaribe.csv --logfile=ce_jaguaribe.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ce_juazeiro_do_norte ------------------------------------------------"
scrapy crawl ce_juazeiro_do_norte -a start=2025-04-28 -o ce_juazeiro_do_norte.csv --logfile=ce_juazeiro_do_norte.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ce_sobral ------------------------------------------------"
scrapy crawl ce_sobral -a start=2025-04-28 -o ce_sobral.csv --logfile=ce_sobral.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR df_brasilia ------------------------------------------------"
scrapy crawl df_brasilia -a start=2025-04-28 -o df_brasilia.csv --logfile=df_brasilia.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR es_associacao_municipios ------------------------------------------------"
scrapy crawl es_associacao_municipios -a start=2025-04-28 -o es_associacao_municipios.csv --logfile=es_associacao_municipios.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR es_cariacica ------------------------------------------------"
scrapy crawl es_cariacica -a start=2025-04-28 -o es_cariacica.csv --logfile=es_cariacica.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR es_serra ------------------------------------------------"
scrapy crawl es_serra -a start=2025-04-28 -o es_serra.csv --logfile=es_serra.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR es_vila_velha ------------------------------------------------"
scrapy crawl es_vila_velha -a start=2025-04-28 -o es_vila_velha.csv --logfile=es_vila_velha.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR es_vitoria ------------------------------------------------"
scrapy crawl es_vitoria -a start=2025-04-28 -o es_vitoria.csv --logfile=es_vitoria.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR go_aparecida_de_goiania ------------------------------------------------"
scrapy crawl go_aparecida_de_goiania -a start=2025-04-28 -o go_aparecida_de_goiania.csv --logfile=go_aparecida_de_goiania.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR go_associacao_municipios ------------------------------------------------"
scrapy crawl go_associacao_municipios -a start=2025-04-28 -o go_associacao_municipios.csv --logfile=go_associacao_municipios.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR go_federacao_municipios ------------------------------------------------"
scrapy crawl go_federacao_municipios -a start=2025-04-28 -o go_federacao_municipios.csv --logfile=go_federacao_municipios.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR go_goiania ------------------------------------------------"
scrapy crawl go_goiania -a start=2025-04-28 -o go_goiania.csv --logfile=go_goiania.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ma_afonso_cunha ------------------------------------------------"
scrapy crawl ma_afonso_cunha -a start=2025-04-28 -o ma_afonso_cunha.csv --logfile=ma_afonso_cunha.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ma_aldeias_altas ------------------------------------------------"
scrapy crawl ma_aldeias_altas -a start=2025-04-28 -o ma_aldeias_altas.csv --logfile=ma_aldeias_altas.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ma_anajatuba ------------------------------------------------"
scrapy crawl ma_anajatuba -a start=2025-04-28 -o ma_anajatuba.csv --logfile=ma_anajatuba.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ma_axixa ------------------------------------------------"
scrapy crawl ma_axixa -a start=2025-04-28 -o ma_axixa.csv --logfile=ma_axixa.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ma_bacabal ------------------------------------------------"
scrapy crawl ma_bacabal -a start=2025-04-28 -o ma_bacabal.csv --logfile=ma_bacabal.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ma_bacuri ------------------------------------------------"
scrapy crawl ma_bacuri -a start=2025-04-28 -o ma_bacuri.csv --logfile=ma_bacuri.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ma_bacurituba ------------------------------------------------"
scrapy crawl ma_bacurituba -a start=2025-04-28 -o ma_bacurituba.csv --logfile=ma_bacurituba.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ma_boa_vista_do_gurupi ------------------------------------------------"
scrapy crawl ma_boa_vista_do_gurupi -a start=2025-04-28 -o ma_boa_vista_do_gurupi.csv --logfile=ma_boa_vista_do_gurupi.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ma_bom_jardim ------------------------------------------------"
scrapy crawl ma_bom_jardim -a start=2025-04-28 -o ma_bom_jardim.csv --logfile=ma_bom_jardim.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ma_bom_lugar ------------------------------------------------"
scrapy crawl ma_bom_lugar -a start=2025-04-28 -o ma_bom_lugar.csv --logfile=ma_bom_lugar.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ma_buriticupu ------------------------------------------------"
scrapy crawl ma_buriticupu -a start=2025-04-28 -o ma_buriticupu.csv --logfile=ma_buriticupu.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ma_caxias_2017 ------------------------------------------------"
scrapy crawl ma_caxias_2017 -a start=2025-04-28 -o ma_caxias_2017.csv --logfile=ma_caxias_2017.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ma_caxias_2021 ------------------------------------------------"
scrapy crawl ma_caxias_2021 -a start=2025-04-28 -o ma_caxias_2021.csv --logfile=ma_caxias_2021.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ma_centro_do_guilherme ------------------------------------------------"
scrapy crawl ma_centro_do_guilherme -a start=2025-04-28 -o ma_centro_do_guilherme.csv --logfile=ma_centro_do_guilherme.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ma_codo ------------------------------------------------"
scrapy crawl ma_codo -a start=2025-04-28 -o ma_codo.csv --logfile=ma_codo.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ma_coroata ------------------------------------------------"
scrapy crawl ma_coroata -a start=2025-04-28 -o ma_coroata.csv --logfile=ma_coroata.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ma_duque_bacelar ------------------------------------------------"
scrapy crawl ma_duque_bacelar -a start=2025-04-28 -o ma_duque_bacelar.csv --logfile=ma_duque_bacelar.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ma_feira_nova_do_maranhao ------------------------------------------------"
scrapy crawl ma_feira_nova_do_maranhao -a start=2025-04-28 -o ma_feira_nova_do_maranhao.csv --logfile=ma_feira_nova_do_maranhao.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ma_itapecuru_mirim ------------------------------------------------"
scrapy crawl ma_itapecuru_mirim -a start=2025-04-28 -o ma_itapecuru_mirim.csv --logfile=ma_itapecuru_mirim.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ma_maracacume ------------------------------------------------"
scrapy crawl ma_maracacume -a start=2025-04-28 -o ma_maracacume.csv --logfile=ma_maracacume.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ma_maranhaozinho ------------------------------------------------"
scrapy crawl ma_maranhaozinho -a start=2025-04-28 -o ma_maranhaozinho.csv --logfile=ma_maranhaozinho.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ma_milagres_do_maranhao ------------------------------------------------"
scrapy crawl ma_milagres_do_maranhao -a start=2025-04-28 -o ma_milagres_do_maranhao.csv --logfile=ma_milagres_do_maranhao.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ma_nina_rodrigues ------------------------------------------------"
scrapy crawl ma_nina_rodrigues -a start=2025-04-28 -o ma_nina_rodrigues.csv --logfile=ma_nina_rodrigues.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ma_nova_iorque ------------------------------------------------"
scrapy crawl ma_nova_iorque -a start=2025-04-28 -o ma_nova_iorque.csv --logfile=ma_nova_iorque.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ma_peritoro ------------------------------------------------"
scrapy crawl ma_peritoro -a start=2025-04-28 -o ma_peritoro.csv --logfile=ma_peritoro.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ma_santo_antonio_dos_lopes ------------------------------------------------"
scrapy crawl ma_santo_antonio_dos_lopes -a start=2025-04-28 -o ma_santo_antonio_dos_lopes.csv --logfile=ma_santo_antonio_dos_lopes.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ma_sao_jose_dos_basilios ------------------------------------------------"
scrapy crawl ma_sao_jose_dos_basilios -a start=2025-04-28 -o ma_sao_jose_dos_basilios.csv --logfile=ma_sao_jose_dos_basilios.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ma_sao_luis ------------------------------------------------"
scrapy crawl ma_sao_luis -a start=2025-04-28 -o ma_sao_luis.csv --logfile=ma_sao_luis.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ma_sao_vicente_ferrer ------------------------------------------------"
scrapy crawl ma_sao_vicente_ferrer -a start=2025-04-28 -o ma_sao_vicente_ferrer.csv --logfile=ma_sao_vicente_ferrer.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ma_turilandia ------------------------------------------------"
scrapy crawl ma_turilandia -a start=2025-04-28 -o ma_turilandia.csv --logfile=ma_turilandia.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ma_viana ------------------------------------------------"
scrapy crawl ma_viana -a start=2025-04-28 -o ma_viana.csv --logfile=ma_viana.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ma_ze_doca ------------------------------------------------"
scrapy crawl ma_ze_doca -a start=2025-04-28 -o ma_ze_doca.csv --logfile=ma_ze_doca.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR mg_associacao_municipios ------------------------------------------------"
scrapy crawl mg_associacao_municipios -a start=2025-04-28 -o mg_associacao_municipios.csv --logfile=mg_associacao_municipios.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR mg_belo_horizonte ------------------------------------------------"
scrapy crawl mg_belo_horizonte -a start=2025-04-28 -o mg_belo_horizonte.csv --logfile=mg_belo_horizonte.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR mg_betim ------------------------------------------------"
scrapy crawl mg_betim -a start=2025-04-28 -o mg_betim.csv --logfile=mg_betim.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR mg_campo_belo ------------------------------------------------"
scrapy crawl mg_campo_belo -a start=2025-04-28 -o mg_campo_belo.csv --logfile=mg_campo_belo.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR mg_candeias ------------------------------------------------"
scrapy crawl mg_candeias -a start=2025-04-28 -o mg_candeias.csv --logfile=mg_candeias.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR mg_carmo_da_cachoeira ------------------------------------------------"
scrapy crawl mg_carmo_da_cachoeira -a start=2025-04-28 -o mg_carmo_da_cachoeira.csv --logfile=mg_carmo_da_cachoeira.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR mg_carmo_do_rio_claro ------------------------------------------------"
scrapy crawl mg_carmo_do_rio_claro -a start=2025-04-28 -o mg_carmo_do_rio_claro.csv --logfile=mg_carmo_do_rio_claro.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR mg_contagem ------------------------------------------------"
scrapy crawl mg_contagem -a start=2025-04-28 -o mg_contagem.csv --logfile=mg_contagem.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR mg_crucilandia ------------------------------------------------"
scrapy crawl mg_crucilandia -a start=2025-04-28 -o mg_crucilandia.csv --logfile=mg_crucilandia.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR mg_governador_valadares ------------------------------------------------"
scrapy crawl mg_governador_valadares -a start=2025-04-28 -o mg_governador_valadares.csv --logfile=mg_governador_valadares.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR mg_itajuba ------------------------------------------------"
scrapy crawl mg_itajuba -a start=2025-04-28 -o mg_itajuba.csv --logfile=mg_itajuba.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR mg_itauna ------------------------------------------------"
scrapy crawl mg_itauna -a start=2025-04-28 -o mg_itauna.csv --logfile=mg_itauna.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR mg_januaria ------------------------------------------------"
scrapy crawl mg_januaria -a start=2025-04-28 -o mg_januaria.csv --logfile=mg_januaria.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR mg_juatuba ------------------------------------------------"
scrapy crawl mg_juatuba -a start=2025-04-28 -o mg_juatuba.csv --logfile=mg_juatuba.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR mg_nova_serrana ------------------------------------------------"
scrapy crawl mg_nova_serrana -a start=2025-04-28 -o mg_nova_serrana.csv --logfile=mg_nova_serrana.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR mg_onca_de_pitangui ------------------------------------------------"
scrapy crawl mg_onca_de_pitangui -a start=2025-04-28 -o mg_onca_de_pitangui.csv --logfile=mg_onca_de_pitangui.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR mg_piranguinho ------------------------------------------------"
scrapy crawl mg_piranguinho -a start=2025-04-28 -o mg_piranguinho.csv --logfile=mg_piranguinho.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR mg_salinas ------------------------------------------------"
scrapy crawl mg_salinas -a start=2025-04-28 -o mg_salinas.csv --logfile=mg_salinas.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR mg_taiobeiras ------------------------------------------------"
scrapy crawl mg_taiobeiras -a start=2025-04-28 -o mg_taiobeiras.csv --logfile=mg_taiobeiras.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR mg_uberaba_2003 ------------------------------------------------"
scrapy crawl mg_uberaba_2003 -a start=2025-04-28 -o mg_uberaba_2003.csv --logfile=mg_uberaba_2003.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR mg_uberaba_2021 ------------------------------------------------"
scrapy crawl mg_uberaba_2021 -a start=2025-04-28 -o mg_uberaba_2021.csv --logfile=mg_uberaba_2021.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR mg_uberlandia ------------------------------------------------"
scrapy crawl mg_uberlandia -a start=2025-04-28 -o mg_uberlandia.csv --logfile=mg_uberlandia.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR mg_varzea_da_palma ------------------------------------------------"
scrapy crawl mg_varzea_da_palma -a start=2025-04-28 -o mg_varzea_da_palma.csv --logfile=mg_varzea_da_palma.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ms_associacao_municipios ------------------------------------------------"
scrapy crawl ms_associacao_municipios -a start=2025-04-28 -o ms_associacao_municipios.csv --logfile=ms_associacao_municipios.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ms_bela_vista ------------------------------------------------"
scrapy crawl ms_bela_vista -a start=2025-04-28 -o ms_bela_vista.csv --logfile=ms_bela_vista.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ms_campo_grande ------------------------------------------------"
scrapy crawl ms_campo_grande -a start=2025-04-28 -o ms_campo_grande.csv --logfile=ms_campo_grande.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ms_corumba ------------------------------------------------"
scrapy crawl ms_corumba -a start=2025-04-28 -o ms_corumba.csv --logfile=ms_corumba.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ms_costa_rica ------------------------------------------------"
scrapy crawl ms_costa_rica -a start=2025-04-28 -o ms_costa_rica.csv --logfile=ms_costa_rica.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ms_deodapolis ------------------------------------------------"
scrapy crawl ms_deodapolis -a start=2025-04-28 -o ms_deodapolis.csv --logfile=ms_deodapolis.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ms_gloria_de_dourados ------------------------------------------------"
scrapy crawl ms_gloria_de_dourados -a start=2025-04-28 -o ms_gloria_de_dourados.csv --logfile=ms_gloria_de_dourados.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ms_inocencia ------------------------------------------------"
scrapy crawl ms_inocencia -a start=2025-04-28 -o ms_inocencia.csv --logfile=ms_inocencia.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ms_maracaju ------------------------------------------------"
scrapy crawl ms_maracaju -a start=2025-04-28 -o ms_maracaju.csv --logfile=ms_maracaju.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ms_paranhos ------------------------------------------------"
scrapy crawl ms_paranhos -a start=2025-04-28 -o ms_paranhos.csv --logfile=ms_paranhos.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ms_rio_brilhante ------------------------------------------------"
scrapy crawl ms_rio_brilhante -a start=2025-04-28 -o ms_rio_brilhante.csv --logfile=ms_rio_brilhante.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR mt_associacao_municipios ------------------------------------------------"
scrapy crawl mt_associacao_municipios -a start=2025-04-28 -o mt_associacao_municipios.csv --logfile=mt_associacao_municipios.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR mt_cotriguacu ------------------------------------------------"
scrapy crawl mt_cotriguacu -a start=2025-04-28 -o mt_cotriguacu.csv --logfile=mt_cotriguacu.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR mt_cuiaba ------------------------------------------------"
scrapy crawl mt_cuiaba -a start=2025-04-28 -o mt_cuiaba.csv --logfile=mt_cuiaba.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR mt_rondonopolis ------------------------------------------------"
scrapy crawl mt_rondonopolis -a start=2025-04-28 -o mt_rondonopolis.csv --logfile=mt_rondonopolis.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR pa_ananindeua ------------------------------------------------"
scrapy crawl pa_ananindeua -a start=2025-04-28 -o pa_ananindeua.csv --logfile=pa_ananindeua.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR pa_belem ------------------------------------------------"
scrapy crawl pa_belem -a start=2025-04-28 -o pa_belem.csv --logfile=pa_belem.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR pa_federacao_municipios ------------------------------------------------"
scrapy crawl pa_federacao_municipios -a start=2025-04-28 -o pa_federacao_municipios.csv --logfile=pa_federacao_municipios.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR pa_garrafao_do_norte ------------------------------------------------"
scrapy crawl pa_garrafao_do_norte -a start=2025-04-28 -o pa_garrafao_do_norte.csv --logfile=pa_garrafao_do_norte.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR pa_santana_do_araguaia ------------------------------------------------"
scrapy crawl pa_santana_do_araguaia -a start=2025-04-28 -o pa_santana_do_araguaia.csv --logfile=pa_santana_do_araguaia.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR pb_campina_grande ------------------------------------------------"
scrapy crawl pb_campina_grande -a start=2025-04-28 -o pb_campina_grande.csv --logfile=pb_campina_grande.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR pb_federacao_municipios ------------------------------------------------"
scrapy crawl pb_federacao_municipios -a start=2025-04-28 -o pb_federacao_municipios.csv --logfile=pb_federacao_municipios.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR pb_jacarau ------------------------------------------------"
scrapy crawl pb_jacarau -a start=2025-04-28 -o pb_jacarau.csv --logfile=pb_jacarau.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR pb_jerico ------------------------------------------------"
scrapy crawl pb_jerico -a start=2025-04-28 -o pb_jerico.csv --logfile=pb_jerico.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR pb_joao_pessoa ------------------------------------------------"
scrapy crawl pb_joao_pessoa -a start=2025-04-28 -o pb_joao_pessoa.csv --logfile=pb_joao_pessoa.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR pb_marizopolis ------------------------------------------------"
scrapy crawl pb_marizopolis -a start=2025-04-28 -o pb_marizopolis.csv --logfile=pb_marizopolis.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR pb_piloezinhos ------------------------------------------------"
scrapy crawl pb_piloezinhos -a start=2025-04-28 -o pb_piloezinhos.csv --logfile=pb_piloezinhos.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR pb_riachao ------------------------------------------------"
scrapy crawl pb_riachao -a start=2025-04-28 -o pb_riachao.csv --logfile=pb_riachao.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR pb_sao_jose_dos_ramos ------------------------------------------------"
scrapy crawl pb_sao_jose_dos_ramos -a start=2025-04-28 -o pb_sao_jose_dos_ramos.csv --logfile=pb_sao_jose_dos_ramos.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR pb_serraria ------------------------------------------------"
scrapy crawl pb_serraria -a start=2025-04-28 -o pb_serraria.csv --logfile=pb_serraria.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR pb_sertaozinho ------------------------------------------------"
scrapy crawl pb_sertaozinho -a start=2025-04-28 -o pb_sertaozinho.csv --logfile=pb_sertaozinho.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR pb_tacima ------------------------------------------------"
scrapy crawl pb_tacima -a start=2025-04-28 -o pb_tacima.csv --logfile=pb_tacima.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR pe_associacao_municipios ------------------------------------------------"
scrapy crawl pe_associacao_municipios -a start=2025-04-28 -o pe_associacao_municipios.csv --logfile=pe_associacao_municipios.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR pe_cabrobo ------------------------------------------------"
scrapy crawl pe_cabrobo -a start=2025-04-28 -o pe_cabrobo.csv --logfile=pe_cabrobo.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR pe_jaboatao_dos_guararapes ------------------------------------------------"
scrapy crawl pe_jaboatao_dos_guararapes -a start=2025-04-28 -o pe_jaboatao_dos_guararapes.csv --logfile=pe_jaboatao_dos_guararapes.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR pe_moreilandia ------------------------------------------------"
scrapy crawl pe_moreilandia -a start=2025-04-28 -o pe_moreilandia.csv --logfile=pe_moreilandia.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR pe_petrolina ------------------------------------------------"
scrapy crawl pe_petrolina -a start=2025-04-28 -o pe_petrolina.csv --logfile=pe_petrolina.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR pe_recife_2015 ------------------------------------------------"
scrapy crawl pe_recife_2015 -a start=2025-04-28 -o pe_recife_2015.csv --logfile=pe_recife_2015.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR pe_recife_2020 ------------------------------------------------"
scrapy crawl pe_recife_2020 -a start=2025-04-28 -o pe_recife_2020.csv --logfile=pe_recife_2020.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR pi_associacao_municipios ------------------------------------------------"
scrapy crawl pi_associacao_municipios -a start=2025-04-28 -o pi_associacao_municipios.csv --logfile=pi_associacao_municipios.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR pi_teresina ------------------------------------------------"
scrapy crawl pi_teresina -a start=2025-04-28 -o pi_teresina.csv --logfile=pi_teresina.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR pr_antonio_olinto ------------------------------------------------"
scrapy crawl pr_antonio_olinto -a start=2025-04-28 -o pr_antonio_olinto.csv --logfile=pr_antonio_olinto.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR pr_apucarana ------------------------------------------------"
scrapy crawl pr_apucarana -a start=2025-04-28 -o pr_apucarana.csv --logfile=pr_apucarana.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR pr_arapongas ------------------------------------------------"
scrapy crawl pr_arapongas -a start=2025-04-28 -o pr_arapongas.csv --logfile=pr_arapongas.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR pr_associacao_municipios ------------------------------------------------"
scrapy crawl pr_associacao_municipios -a start=2025-04-28 -o pr_associacao_municipios.csv --logfile=pr_associacao_municipios.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR pr_cafelandia ------------------------------------------------"
scrapy crawl pr_cafelandia -a start=2025-04-28 -o pr_cafelandia.csv --logfile=pr_cafelandia.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR pr_cafezal_do_sul ------------------------------------------------"
scrapy crawl pr_cafezal_do_sul -a start=2025-04-28 -o pr_cafezal_do_sul.csv --logfile=pr_cafezal_do_sul.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR pr_campo_largo ------------------------------------------------"
scrapy crawl pr_campo_largo -a start=2025-04-28 -o pr_campo_largo.csv --logfile=pr_campo_largo.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR pr_campo_mourao ------------------------------------------------"
scrapy crawl pr_campo_mourao -a start=2025-04-28 -o pr_campo_mourao.csv --logfile=pr_campo_mourao.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR pr_carambei ------------------------------------------------"
scrapy crawl pr_carambei -a start=2025-04-28 -o pr_carambei.csv --logfile=pr_carambei.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR pr_cascavel ------------------------------------------------"
scrapy crawl pr_cascavel -a start=2025-04-28 -o pr_cascavel.csv --logfile=pr_cascavel.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR pr_castro ------------------------------------------------"
scrapy crawl pr_castro -a start=2025-04-28 -o pr_castro.csv --logfile=pr_castro.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR pr_corbelia ------------------------------------------------"
scrapy crawl pr_corbelia -a start=2025-04-28 -o pr_corbelia.csv --logfile=pr_corbelia.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR pr_curitiba ------------------------------------------------"
scrapy crawl pr_curitiba -a start=2025-04-28 -o pr_curitiba.csv --logfile=pr_curitiba.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR pr_foz_do_iguacu ------------------------------------------------"
scrapy crawl pr_foz_do_iguacu -a start=2025-04-28 -o pr_foz_do_iguacu.csv --logfile=pr_foz_do_iguacu.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR pr_guaraniacu ------------------------------------------------"
scrapy crawl pr_guaraniacu -a start=2025-04-28 -o pr_guaraniacu.csv --logfile=pr_guaraniacu.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR pr_ipiranga ------------------------------------------------"
scrapy crawl pr_ipiranga -a start=2025-04-28 -o pr_ipiranga.csv --logfile=pr_ipiranga.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR pr_jaboti ------------------------------------------------"
scrapy crawl pr_jaboti -a start=2025-04-28 -o pr_jaboti.csv --logfile=pr_jaboti.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR pr_juranda ------------------------------------------------"
scrapy crawl pr_juranda -a start=2025-04-28 -o pr_juranda.csv --logfile=pr_juranda.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR pr_londrina ------------------------------------------------"
scrapy crawl pr_londrina -a start=2025-04-28 -o pr_londrina.csv --logfile=pr_londrina.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR pr_mambore ------------------------------------------------"
scrapy crawl pr_mambore -a start=2025-04-28 -o pr_mambore.csv --logfile=pr_mambore.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR pr_marilandia_do_sul ------------------------------------------------"
scrapy crawl pr_marilandia_do_sul -a start=2025-04-28 -o pr_marilandia_do_sul.csv --logfile=pr_marilandia_do_sul.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR pr_maringa ------------------------------------------------"
scrapy crawl pr_maringa -a start=2025-04-28 -o pr_maringa.csv --logfile=pr_maringa.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR pr_ouro_verde_do_oeste ------------------------------------------------"
scrapy crawl pr_ouro_verde_do_oeste -a start=2025-04-28 -o pr_ouro_verde_do_oeste.csv --logfile=pr_ouro_verde_do_oeste.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR pr_pinhais ------------------------------------------------"
scrapy crawl pr_pinhais -a start=2025-04-28 -o pr_pinhais.csv --logfile=pr_pinhais.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR pr_ponta_grossa ------------------------------------------------"
scrapy crawl pr_ponta_grossa -a start=2025-04-28 -o pr_ponta_grossa.csv --logfile=pr_ponta_grossa.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR pr_primeiro_de_maio ------------------------------------------------"
scrapy crawl pr_primeiro_de_maio -a start=2025-04-28 -o pr_primeiro_de_maio.csv --logfile=pr_primeiro_de_maio.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR pr_santo_antonio_do_paraiso ------------------------------------------------"
scrapy crawl pr_santo_antonio_do_paraiso -a start=2025-04-28 -o pr_santo_antonio_do_paraiso.csv --logfile=pr_santo_antonio_do_paraiso.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR pr_sao_joao_do_triunfo ------------------------------------------------"
scrapy crawl pr_sao_joao_do_triunfo -a start=2025-04-28 -o pr_sao_joao_do_triunfo.csv --logfile=pr_sao_joao_do_triunfo.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR pr_sao_jose_pinhais ------------------------------------------------"
scrapy crawl pr_sao_jose_pinhais -a start=2025-04-28 -o pr_sao_jose_pinhais.csv --logfile=pr_sao_jose_pinhais.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR pr_sao_mateus_do_sul ------------------------------------------------"
scrapy crawl pr_sao_mateus_do_sul -a start=2025-04-28 -o pr_sao_mateus_do_sul.csv --logfile=pr_sao_mateus_do_sul.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR pr_tamboara ------------------------------------------------"
scrapy crawl pr_tamboara -a start=2025-04-28 -o pr_tamboara.csv --logfile=pr_tamboara.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR rj_angra_dos_reis ------------------------------------------------"
scrapy crawl rj_angra_dos_reis -a start=2025-04-28 -o rj_angra_dos_reis.csv --logfile=rj_angra_dos_reis.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR rj_areal ------------------------------------------------"
scrapy crawl rj_areal -a start=2025-04-28 -o rj_areal.csv --logfile=rj_areal.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR rj_armacao_dos_buzios ------------------------------------------------"
scrapy crawl rj_armacao_dos_buzios -a start=2025-04-28 -o rj_armacao_dos_buzios.csv --logfile=rj_armacao_dos_buzios.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR rj_arraial_do_cabo ------------------------------------------------"
scrapy crawl rj_arraial_do_cabo -a start=2025-04-28 -o rj_arraial_do_cabo.csv --logfile=rj_arraial_do_cabo.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR rj_associacao_municipios ------------------------------------------------"
scrapy crawl rj_associacao_municipios -a start=2025-04-28 -o rj_associacao_municipios.csv --logfile=rj_associacao_municipios.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR rj_barra_mansa ------------------------------------------------"
scrapy crawl rj_barra_mansa -a start=2025-04-28 -o rj_barra_mansa.csv --logfile=rj_barra_mansa.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR rj_belford_roxo ------------------------------------------------"
scrapy crawl rj_belford_roxo -a start=2025-04-28 -o rj_belford_roxo.csv --logfile=rj_belford_roxo.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR rj_cabo_frio ------------------------------------------------"
scrapy crawl rj_cabo_frio -a start=2025-04-28 -o rj_cabo_frio.csv --logfile=rj_cabo_frio.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR rj_campos_dos_goytacazes ------------------------------------------------"
scrapy crawl rj_campos_dos_goytacazes -a start=2025-04-28 -o rj_campos_dos_goytacazes.csv --logfile=rj_campos_dos_goytacazes.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR rj_casimiro_de_abreu ------------------------------------------------"
scrapy crawl rj_casimiro_de_abreu -a start=2025-04-28 -o rj_casimiro_de_abreu.csv --logfile=rj_casimiro_de_abreu.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR rj_comendador_levy_gasparian ------------------------------------------------"
scrapy crawl rj_comendador_levy_gasparian -a start=2025-04-28 -o rj_comendador_levy_gasparian.csv --logfile=rj_comendador_levy_gasparian.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR rj_cordeiro ------------------------------------------------"
scrapy crawl rj_cordeiro -a start=2025-04-28 -o rj_cordeiro.csv --logfile=rj_cordeiro.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR rj_duque_de_caxias ------------------------------------------------"
scrapy crawl rj_duque_de_caxias -a start=2025-04-28 -o rj_duque_de_caxias.csv --logfile=rj_duque_de_caxias.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR rj_iguaba_grande ------------------------------------------------"
scrapy crawl rj_iguaba_grande -a start=2025-04-28 -o rj_iguaba_grande.csv --logfile=rj_iguaba_grande.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR rj_itaguai ------------------------------------------------"
scrapy crawl rj_itaguai -a start=2025-04-28 -o rj_itaguai.csv --logfile=rj_itaguai.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR rj_macae ------------------------------------------------"
scrapy crawl rj_macae -a start=2025-04-28 -o rj_macae.csv --logfile=rj_macae.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR rj_marica ------------------------------------------------"
scrapy crawl rj_marica -a start=2025-04-28 -o rj_marica.csv --logfile=rj_marica.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR rj_mesquita ------------------------------------------------"
scrapy crawl rj_mesquita -a start=2025-04-28 -o rj_mesquita.csv --logfile=rj_mesquita.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR rj_miguel_pereira ------------------------------------------------"
scrapy crawl rj_miguel_pereira -a start=2025-04-28 -o rj_miguel_pereira.csv --logfile=rj_miguel_pereira.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR rj_niteroi ------------------------------------------------"
scrapy crawl rj_niteroi -a start=2025-04-28 -o rj_niteroi.csv --logfile=rj_niteroi.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR rj_nova_friburgo ------------------------------------------------"
scrapy crawl rj_nova_friburgo -a start=2025-04-28 -o rj_nova_friburgo.csv --logfile=rj_nova_friburgo.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR rj_nova_iguacu ------------------------------------------------"
scrapy crawl rj_nova_iguacu -a start=2025-04-28 -o rj_nova_iguacu.csv --logfile=rj_nova_iguacu.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR rj_quatis ------------------------------------------------"
scrapy crawl rj_quatis -a start=2025-04-28 -o rj_quatis.csv --logfile=rj_quatis.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR rj_queimados ------------------------------------------------"
scrapy crawl rj_queimados -a start=2025-04-28 -o rj_queimados.csv --logfile=rj_queimados.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR rj_quissama ------------------------------------------------"
scrapy crawl rj_quissama -a start=2025-04-28 -o rj_quissama.csv --logfile=rj_quissama.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR rj_rio_de_janeiro ------------------------------------------------"
scrapy crawl rj_rio_de_janeiro -a start=2025-04-28 -o rj_rio_de_janeiro.csv --logfile=rj_rio_de_janeiro.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR rj_sao_joao_da_barra ------------------------------------------------"
scrapy crawl rj_sao_joao_da_barra -a start=2025-04-28 -o rj_sao_joao_da_barra.csv --logfile=rj_sao_joao_da_barra.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR rj_sao_joao_de_meriti ------------------------------------------------"
scrapy crawl rj_sao_joao_de_meriti -a start=2025-04-28 -o rj_sao_joao_de_meriti.csv --logfile=rj_sao_joao_de_meriti.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR rj_sao_jose_do_vale_do_rio_preto ------------------------------------------------"
scrapy crawl rj_sao_jose_do_vale_do_rio_preto -a start=2025-04-28 -o rj_sao_jose_do_vale_do_rio_preto.csv --logfile=rj_sao_jose_do_vale_do_rio_preto.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR rj_sao_pedro_da_aldeia ------------------------------------------------"
scrapy crawl rj_sao_pedro_da_aldeia -a start=2025-04-28 -o rj_sao_pedro_da_aldeia.csv --logfile=rj_sao_pedro_da_aldeia.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR rj_sapucaia ------------------------------------------------"
scrapy crawl rj_sapucaia -a start=2025-04-28 -o rj_sapucaia.csv --logfile=rj_sapucaia.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR rj_saquarema ------------------------------------------------"
scrapy crawl rj_saquarema -a start=2025-04-28 -o rj_saquarema.csv --logfile=rj_saquarema.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR rj_sumidouro ------------------------------------------------"
scrapy crawl rj_sumidouro -a start=2025-04-28 -o rj_sumidouro.csv --logfile=rj_sumidouro.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR rj_varre_sai ------------------------------------------------"
scrapy crawl rj_varre_sai -a start=2025-04-28 -o rj_varre_sai.csv --logfile=rj_varre_sai.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR rn_federacao_municipios ------------------------------------------------"
scrapy crawl rn_federacao_municipios -a start=2025-04-28 -o rn_federacao_municipios.csv --logfile=rn_federacao_municipios.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR rn_mossoro_2008 ------------------------------------------------"
scrapy crawl rn_mossoro_2008 -a start=2025-04-28 -o rn_mossoro_2008.csv --logfile=rn_mossoro_2008.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR rn_mossoro_2023 ------------------------------------------------"
scrapy crawl rn_mossoro_2023 -a start=2025-04-28 -o rn_mossoro_2023.csv --logfile=rn_mossoro_2023.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR rn_natal ------------------------------------------------"
scrapy crawl rn_natal -a start=2025-04-28 -o rn_natal.csv --logfile=rn_natal.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR rn_pau_dos_ferros_2017 ------------------------------------------------"
scrapy crawl rn_pau_dos_ferros_2017 -a start=2025-04-28 -o rn_pau_dos_ferros_2017.csv --logfile=rn_pau_dos_ferros_2017.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR rn_pau_dos_ferros_2022 ------------------------------------------------"
scrapy crawl rn_pau_dos_ferros_2022 -a start=2025-04-28 -o rn_pau_dos_ferros_2022.csv --logfile=rn_pau_dos_ferros_2022.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR rn_santa_cruz ------------------------------------------------"
scrapy crawl rn_santa_cruz -a start=2025-04-28 -o rn_santa_cruz.csv --logfile=rn_santa_cruz.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR rn_sao_francisco_do_oeste ------------------------------------------------"
scrapy crawl rn_sao_francisco_do_oeste -a start=2025-04-28 -o rn_sao_francisco_do_oeste.csv --logfile=rn_sao_francisco_do_oeste.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR rn_sao_goncalo_do_amarante ------------------------------------------------"
scrapy crawl rn_sao_goncalo_do_amarante -a start=2025-04-28 -o rn_sao_goncalo_do_amarante.csv --logfile=rn_sao_goncalo_do_amarante.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR rn_taboleiro_grande ------------------------------------------------"
scrapy crawl rn_taboleiro_grande -a start=2025-04-28 -o rn_taboleiro_grande.csv --logfile=rn_taboleiro_grande.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ro_associacao_municipios ------------------------------------------------"
scrapy crawl ro_associacao_municipios -a start=2025-04-28 -o ro_associacao_municipios.csv --logfile=ro_associacao_municipios.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ro_jaru ------------------------------------------------"
scrapy crawl ro_jaru -a start=2025-04-28 -o ro_jaru.csv --logfile=ro_jaru.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR ro_porto_velho ------------------------------------------------"
scrapy crawl ro_porto_velho -a start=2025-04-28 -o ro_porto_velho.csv --logfile=ro_porto_velho.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR rr_associacao_municipios ------------------------------------------------"
scrapy crawl rr_associacao_municipios -a start=2025-04-28 -o rr_associacao_municipios.csv --logfile=rr_associacao_municipios.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR rr_boa_vista ------------------------------------------------"
scrapy crawl rr_boa_vista -a start=2025-04-28 -o rr_boa_vista.csv --logfile=rr_boa_vista.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR rs_associacao_municipios ------------------------------------------------"
scrapy crawl rs_associacao_municipios -a start=2025-04-28 -o rs_associacao_municipios.csv --logfile=rs_associacao_municipios.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR rs_bento_goncalves ------------------------------------------------"
scrapy crawl rs_bento_goncalves -a start=2025-04-28 -o rs_bento_goncalves.csv --logfile=rs_bento_goncalves.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR rs_cachoeira_do_sul ------------------------------------------------"
scrapy crawl rs_cachoeira_do_sul -a start=2025-04-28 -o rs_cachoeira_do_sul.csv --logfile=rs_cachoeira_do_sul.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR rs_camaqua ------------------------------------------------"
scrapy crawl rs_camaqua -a start=2025-04-28 -o rs_camaqua.csv --logfile=rs_camaqua.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR rs_candelaria ------------------------------------------------"
scrapy crawl rs_candelaria -a start=2025-04-28 -o rs_candelaria.csv --logfile=rs_candelaria.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR rs_canoas ------------------------------------------------"
scrapy crawl rs_canoas -a start=2025-04-28 -o rs_canoas.csv --logfile=rs_canoas.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR rs_caxias_do_sul ------------------------------------------------"
scrapy crawl rs_caxias_do_sul -a start=2025-04-28 -o rs_caxias_do_sul.csv --logfile=rs_caxias_do_sul.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR rs_cerrito ------------------------------------------------"
scrapy crawl rs_cerrito -a start=2025-04-28 -o rs_cerrito.csv --logfile=rs_cerrito.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR rs_dois_irmaos ------------------------------------------------"
scrapy crawl rs_dois_irmaos -a start=2025-04-28 -o rs_dois_irmaos.csv --logfile=rs_dois_irmaos.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR rs_estrela ------------------------------------------------"
scrapy crawl rs_estrela -a start=2025-04-28 -o rs_estrela.csv --logfile=rs_estrela.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR rs_gravatai ------------------------------------------------"
scrapy crawl rs_gravatai -a start=2025-04-28 -o rs_gravatai.csv --logfile=rs_gravatai.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR rs_horizontina ------------------------------------------------"
scrapy crawl rs_horizontina -a start=2025-04-28 -o rs_horizontina.csv --logfile=rs_horizontina.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR rs_marau ------------------------------------------------"
scrapy crawl rs_marau -a start=2025-04-28 -o rs_marau.csv --logfile=rs_marau.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR rs_panambi ------------------------------------------------"
scrapy crawl rs_panambi -a start=2025-04-28 -o rs_panambi.csv --logfile=rs_panambi.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR rs_porto_alegre ------------------------------------------------"
scrapy crawl rs_porto_alegre -a start=2025-04-28 -o rs_porto_alegre.csv --logfile=rs_porto_alegre.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR rs_quatro_irmaos ------------------------------------------------"
scrapy crawl rs_quatro_irmaos -a start=2025-04-28 -o rs_quatro_irmaos.csv --logfile=rs_quatro_irmaos.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR rs_santa_clara_do_sul ------------------------------------------------"
scrapy crawl rs_santa_clara_do_sul -a start=2025-04-28 -o rs_santa_clara_do_sul.csv --logfile=rs_santa_clara_do_sul.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR rs_santa_rosa ------------------------------------------------"
scrapy crawl rs_santa_rosa -a start=2025-04-28 -o rs_santa_rosa.csv --logfile=rs_santa_rosa.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR rs_sao_francisco_de_paula ------------------------------------------------"
scrapy crawl rs_sao_francisco_de_paula -a start=2025-04-28 -o rs_sao_francisco_de_paula.csv --logfile=rs_sao_francisco_de_paula.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR rs_sao_joao_do_polesine ------------------------------------------------"
scrapy crawl rs_sao_joao_do_polesine -a start=2025-04-28 -o rs_sao_joao_do_polesine.csv --logfile=rs_sao_joao_do_polesine.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR rs_sobradinho ------------------------------------------------"
scrapy crawl rs_sobradinho -a start=2025-04-28 -o rs_sobradinho.csv --logfile=rs_sobradinho.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR rs_tres_arroios ------------------------------------------------"
scrapy crawl rs_tres_arroios -a start=2025-04-28 -o rs_tres_arroios.csv --logfile=rs_tres_arroios.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR rs_vera_cruz ------------------------------------------------"
scrapy crawl rs_vera_cruz -a start=2025-04-28 -o rs_vera_cruz.csv --logfile=rs_vera_cruz.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sc_florianopolis_2009 ------------------------------------------------"
scrapy crawl sc_florianopolis_2009 -a start=2025-04-28 -o sc_florianopolis_2009.csv --logfile=sc_florianopolis_2009.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sc_florianopolis_2024 ------------------------------------------------"
scrapy crawl sc_florianopolis_2024 -a start=2025-04-28 -o sc_florianopolis_2024.csv --logfile=sc_florianopolis_2024.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sc_joinville ------------------------------------------------"
scrapy crawl sc_joinville -a start=2025-04-28 -o sc_joinville.csv --logfile=sc_joinville.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR se_aquidaba ------------------------------------------------"
scrapy crawl se_aquidaba -a start=2025-04-28 -o se_aquidaba.csv --logfile=se_aquidaba.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR se_aracaju ------------------------------------------------"
scrapy crawl se_aracaju -a start=2025-04-28 -o se_aracaju.csv --logfile=se_aracaju.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR se_areia_branca ------------------------------------------------"
scrapy crawl se_areia_branca -a start=2025-04-28 -o se_areia_branca.csv --logfile=se_areia_branca.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR se_associacao_municipios ------------------------------------------------"
scrapy crawl se_associacao_municipios -a start=2025-04-28 -o se_associacao_municipios.csv --logfile=se_associacao_municipios.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR se_barra_dos_coqueiros ------------------------------------------------"
scrapy crawl se_barra_dos_coqueiros -a start=2025-04-28 -o se_barra_dos_coqueiros.csv --logfile=se_barra_dos_coqueiros.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR se_campo_do_brito ------------------------------------------------"
scrapy crawl se_campo_do_brito -a start=2025-04-28 -o se_campo_do_brito.csv --logfile=se_campo_do_brito.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR se_canhoba ------------------------------------------------"
scrapy crawl se_canhoba -a start=2025-04-28 -o se_canhoba.csv --logfile=se_canhoba.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR se_caninde_de_sao_francisco ------------------------------------------------"
scrapy crawl se_caninde_de_sao_francisco -a start=2025-04-28 -o se_caninde_de_sao_francisco.csv --logfile=se_caninde_de_sao_francisco.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR se_capela ------------------------------------------------"
scrapy crawl se_capela -a start=2025-04-28 -o se_capela.csv --logfile=se_capela.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR se_divina_pastora ------------------------------------------------"
scrapy crawl se_divina_pastora -a start=2025-04-28 -o se_divina_pastora.csv --logfile=se_divina_pastora.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR se_estancia ------------------------------------------------"
scrapy crawl se_estancia -a start=2025-04-28 -o se_estancia.csv --logfile=se_estancia.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR se_frei_paulo ------------------------------------------------"
scrapy crawl se_frei_paulo -a start=2025-04-28 -o se_frei_paulo.csv --logfile=se_frei_paulo.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR se_ilha_das_flores ------------------------------------------------"
scrapy crawl se_ilha_das_flores -a start=2025-04-28 -o se_ilha_das_flores.csv --logfile=se_ilha_das_flores.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR se_itabaiana ------------------------------------------------"
scrapy crawl se_itabaiana -a start=2025-04-28 -o se_itabaiana.csv --logfile=se_itabaiana.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR se_itabaianinha ------------------------------------------------"
scrapy crawl se_itabaianinha -a start=2025-04-28 -o se_itabaianinha.csv --logfile=se_itabaianinha.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR se_japaratuba ------------------------------------------------"
scrapy crawl se_japaratuba -a start=2025-04-28 -o se_japaratuba.csv --logfile=se_japaratuba.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR se_moita_bonita ------------------------------------------------"
scrapy crawl se_moita_bonita -a start=2025-04-28 -o se_moita_bonita.csv --logfile=se_moita_bonita.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR se_muribeca ------------------------------------------------"
scrapy crawl se_muribeca -a start=2025-04-28 -o se_muribeca.csv --logfile=se_muribeca.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR se_nossa_senhora_das_dores ------------------------------------------------"
scrapy crawl se_nossa_senhora_das_dores -a start=2025-04-28 -o se_nossa_senhora_das_dores.csv --logfile=se_nossa_senhora_das_dores.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR se_nossa_senhora_de_lourdes ------------------------------------------------"
scrapy crawl se_nossa_senhora_de_lourdes -a start=2025-04-28 -o se_nossa_senhora_de_lourdes.csv --logfile=se_nossa_senhora_de_lourdes.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR se_nossa_senhora_do_socorro ------------------------------------------------"
scrapy crawl se_nossa_senhora_do_socorro -a start=2025-04-28 -o se_nossa_senhora_do_socorro.csv --logfile=se_nossa_senhora_do_socorro.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR se_pedra_mole ------------------------------------------------"
scrapy crawl se_pedra_mole -a start=2025-04-28 -o se_pedra_mole.csv --logfile=se_pedra_mole.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR se_pirambu ------------------------------------------------"
scrapy crawl se_pirambu -a start=2025-04-28 -o se_pirambu.csv --logfile=se_pirambu.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR se_poco_verde ------------------------------------------------"
scrapy crawl se_poco_verde -a start=2025-04-28 -o se_poco_verde.csv --logfile=se_poco_verde.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR se_riachao_do_dantas ------------------------------------------------"
scrapy crawl se_riachao_do_dantas -a start=2025-04-28 -o se_riachao_do_dantas.csv --logfile=se_riachao_do_dantas.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR se_rosario_do_catete ------------------------------------------------"
scrapy crawl se_rosario_do_catete -a start=2025-04-28 -o se_rosario_do_catete.csv --logfile=se_rosario_do_catete.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR se_sao_domingos ------------------------------------------------"
scrapy crawl se_sao_domingos -a start=2025-04-28 -o se_sao_domingos.csv --logfile=se_sao_domingos.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR se_simao_dias ------------------------------------------------"
scrapy crawl se_simao_dias -a start=2025-04-28 -o se_simao_dias.csv --logfile=se_simao_dias.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR se_siriri ------------------------------------------------"
scrapy crawl se_siriri -a start=2025-04-28 -o se_siriri.csv --logfile=se_siriri.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR se_telha ------------------------------------------------"
scrapy crawl se_telha -a start=2025-04-28 -o se_telha.csv --logfile=se_telha.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_adolfo ------------------------------------------------"
scrapy crawl sp_adolfo -a start=2025-04-28 -o sp_adolfo.csv --logfile=sp_adolfo.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_aguai ------------------------------------------------"
scrapy crawl sp_aguai -a start=2025-04-28 -o sp_aguai.csv --logfile=sp_aguai.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_aguas_da_prata ------------------------------------------------"
scrapy crawl sp_aguas_da_prata -a start=2025-04-28 -o sp_aguas_da_prata.csv --logfile=sp_aguas_da_prata.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_aguas_de_sao_pedro ------------------------------------------------"
scrapy crawl sp_aguas_de_sao_pedro -a start=2025-04-28 -o sp_aguas_de_sao_pedro.csv --logfile=sp_aguas_de_sao_pedro.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_alto_alegre ------------------------------------------------"
scrapy crawl sp_alto_alegre -a start=2025-04-28 -o sp_alto_alegre.csv --logfile=sp_alto_alegre.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_alvares_florence ------------------------------------------------"
scrapy crawl sp_alvares_florence -a start=2025-04-28 -o sp_alvares_florence.csv --logfile=sp_alvares_florence.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_andradina ------------------------------------------------"
scrapy crawl sp_andradina -a start=2025-04-28 -o sp_andradina.csv --logfile=sp_andradina.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_aparecida ------------------------------------------------"
scrapy crawl sp_aparecida -a start=2025-04-28 -o sp_aparecida.csv --logfile=sp_aparecida.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_aracariguama ------------------------------------------------"
scrapy crawl sp_aracariguama -a start=2025-04-28 -o sp_aracariguama.csv --logfile=sp_aracariguama.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_aracatuba ------------------------------------------------"
scrapy crawl sp_aracatuba -a start=2025-04-28 -o sp_aracatuba.csv --logfile=sp_aracatuba.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_arapei ------------------------------------------------"
scrapy crawl sp_arapei -a start=2025-04-28 -o sp_arapei.csv --logfile=sp_arapei.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_associacao_municipios ------------------------------------------------"
scrapy crawl sp_associacao_municipios -a start=2025-04-28 -o sp_associacao_municipios.csv --logfile=sp_associacao_municipios.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_avanhandava ------------------------------------------------"
scrapy crawl sp_avanhandava -a start=2025-04-28 -o sp_avanhandava.csv --logfile=sp_avanhandava.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_avare ------------------------------------------------"
scrapy crawl sp_avare -a start=2025-04-28 -o sp_avare.csv --logfile=sp_avare.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_barao_de_antonina ------------------------------------------------"
scrapy crawl sp_barao_de_antonina -a start=2025-04-28 -o sp_barao_de_antonina.csv --logfile=sp_barao_de_antonina.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_barbosa ------------------------------------------------"
scrapy crawl sp_barbosa -a start=2025-04-28 -o sp_barbosa.csv --logfile=sp_barbosa.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_bauru ------------------------------------------------"
scrapy crawl sp_bauru -a start=2025-04-28 -o sp_bauru.csv --logfile=sp_bauru.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_birigui ------------------------------------------------"
scrapy crawl sp_birigui -a start=2025-04-28 -o sp_birigui.csv --logfile=sp_birigui.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_botucatu ------------------------------------------------"
scrapy crawl sp_botucatu -a start=2025-04-28 -o sp_botucatu.csv --logfile=sp_botucatu.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_braganca_paulista ------------------------------------------------"
scrapy crawl sp_braganca_paulista -a start=2025-04-28 -o sp_braganca_paulista.csv --logfile=sp_braganca_paulista.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_brejo_alegre ------------------------------------------------"
scrapy crawl sp_brejo_alegre -a start=2025-04-28 -o sp_brejo_alegre.csv --logfile=sp_brejo_alegre.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_cacapava ------------------------------------------------"
scrapy crawl sp_cacapava -a start=2025-04-28 -o sp_cacapava.csv --logfile=sp_cacapava.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_campinas ------------------------------------------------"
scrapy crawl sp_campinas -a start=2025-04-28 -o sp_campinas.csv --logfile=sp_campinas.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_campo_limpo_paulista ------------------------------------------------"
scrapy crawl sp_campo_limpo_paulista -a start=2025-04-28 -o sp_campo_limpo_paulista.csv --logfile=sp_campo_limpo_paulista.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_catanduva ------------------------------------------------"
scrapy crawl sp_catanduva -a start=2025-04-28 -o sp_catanduva.csv --logfile=sp_catanduva.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_charqueada ------------------------------------------------"
scrapy crawl sp_charqueada -a start=2025-04-28 -o sp_charqueada.csv --logfile=sp_charqueada.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_coronel_macedo ------------------------------------------------"
scrapy crawl sp_coronel_macedo -a start=2025-04-28 -o sp_coronel_macedo.csv --logfile=sp_coronel_macedo.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_cunha ------------------------------------------------"
scrapy crawl sp_cunha -a start=2025-04-28 -o sp_cunha.csv --logfile=sp_cunha.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_dirce_reis ------------------------------------------------"
scrapy crawl sp_dirce_reis -a start=2025-04-28 -o sp_dirce_reis.csv --logfile=sp_dirce_reis.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_dracena ------------------------------------------------"
scrapy crawl sp_dracena -a start=2025-04-28 -o sp_dracena.csv --logfile=sp_dracena.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_eldorado ------------------------------------------------"
scrapy crawl sp_eldorado -a start=2025-04-28 -o sp_eldorado.csv --logfile=sp_eldorado.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_fernandopolis ------------------------------------------------"
scrapy crawl sp_fernandopolis -a start=2025-04-28 -o sp_fernandopolis.csv --logfile=sp_fernandopolis.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_floreal ------------------------------------------------"
scrapy crawl sp_floreal -a start=2025-04-28 -o sp_floreal.csv --logfile=sp_floreal.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_franca ------------------------------------------------"
scrapy crawl sp_franca -a start=2025-04-28 -o sp_franca.csv --logfile=sp_franca.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_general_salgado ------------------------------------------------"
scrapy crawl sp_general_salgado -a start=2025-04-28 -o sp_general_salgado.csv --logfile=sp_general_salgado.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_glicerio ------------------------------------------------"
scrapy crawl sp_glicerio -a start=2025-04-28 -o sp_glicerio.csv --logfile=sp_glicerio.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_guaracai ------------------------------------------------"
scrapy crawl sp_guaracai -a start=2025-04-28 -o sp_guaracai.csv --logfile=sp_guaracai.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_guaratingueta ------------------------------------------------"
scrapy crawl sp_guaratingueta -a start=2025-04-28 -o sp_guaratingueta.csv --logfile=sp_guaratingueta.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_guaruja ------------------------------------------------"
scrapy crawl sp_guaruja -a start=2025-04-28 -o sp_guaruja.csv --logfile=sp_guaruja.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_guarulhos ------------------------------------------------"
scrapy crawl sp_guarulhos -a start=2025-04-28 -o sp_guarulhos.csv --logfile=sp_guarulhos.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_ibitinga ------------------------------------------------"
scrapy crawl sp_ibitinga -a start=2025-04-28 -o sp_ibitinga.csv --logfile=sp_ibitinga.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_iepe ------------------------------------------------"
scrapy crawl sp_iepe -a start=2025-04-28 -o sp_iepe.csv --logfile=sp_iepe.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_igaracu_do_tiete ------------------------------------------------"
scrapy crawl sp_igaracu_do_tiete -a start=2025-04-28 -o sp_igaracu_do_tiete.csv --logfile=sp_igaracu_do_tiete.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_iracemapolis ------------------------------------------------"
scrapy crawl sp_iracemapolis -a start=2025-04-28 -o sp_iracemapolis.csv --logfile=sp_iracemapolis.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_irapuru ------------------------------------------------"
scrapy crawl sp_irapuru -a start=2025-04-28 -o sp_irapuru.csv --logfile=sp_irapuru.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_itapeva ------------------------------------------------"
scrapy crawl sp_itapeva -a start=2025-04-28 -o sp_itapeva.csv --logfile=sp_itapeva.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_itapevi ------------------------------------------------"
scrapy crawl sp_itapevi -a start=2025-04-28 -o sp_itapevi.csv --logfile=sp_itapevi.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_itapirapua_paulista ------------------------------------------------"
scrapy crawl sp_itapirapua_paulista -a start=2025-04-28 -o sp_itapirapua_paulista.csv --logfile=sp_itapirapua_paulista.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_itapolis ------------------------------------------------"
scrapy crawl sp_itapolis -a start=2025-04-28 -o sp_itapolis.csv --logfile=sp_itapolis.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_itaporanga ------------------------------------------------"
scrapy crawl sp_itaporanga -a start=2025-04-28 -o sp_itaporanga.csv --logfile=sp_itaporanga.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_itapui ------------------------------------------------"
scrapy crawl sp_itapui -a start=2025-04-28 -o sp_itapui.csv --logfile=sp_itapui.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_itariri ------------------------------------------------"
scrapy crawl sp_itariri -a start=2025-04-28 -o sp_itariri.csv --logfile=sp_itariri.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_itobi ------------------------------------------------"
scrapy crawl sp_itobi -a start=2025-04-28 -o sp_itobi.csv --logfile=sp_itobi.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_itu ------------------------------------------------"
scrapy crawl sp_itu -a start=2025-04-28 -o sp_itu.csv --logfile=sp_itu.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_jaboticabal ------------------------------------------------"
scrapy crawl sp_jaboticabal -a start=2025-04-28 -o sp_jaboticabal.csv --logfile=sp_jaboticabal.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_jandira ------------------------------------------------"
scrapy crawl sp_jandira -a start=2025-04-28 -o sp_jandira.csv --logfile=sp_jandira.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_jau ------------------------------------------------"
scrapy crawl sp_jau -a start=2025-04-28 -o sp_jau.csv --logfile=sp_jau.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_jau_2023 ------------------------------------------------"
scrapy crawl sp_jau_2023 -a start=2025-04-28 -o sp_jau_2023.csv --logfile=sp_jau_2023.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_joanopolis ------------------------------------------------"
scrapy crawl sp_joanopolis -a start=2025-04-28 -o sp_joanopolis.csv --logfile=sp_joanopolis.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_joao_ramalho ------------------------------------------------"
scrapy crawl sp_joao_ramalho -a start=2025-04-28 -o sp_joao_ramalho.csv --logfile=sp_joao_ramalho.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_jundiai ------------------------------------------------"
scrapy crawl sp_jundiai -a start=2025-04-28 -o sp_jundiai.csv --logfile=sp_jundiai.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_junqueiropolis ------------------------------------------------"
scrapy crawl sp_junqueiropolis -a start=2025-04-28 -o sp_junqueiropolis.csv --logfile=sp_junqueiropolis.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_lagoinha ------------------------------------------------"
scrapy crawl sp_lagoinha -a start=2025-04-28 -o sp_lagoinha.csv --logfile=sp_lagoinha.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_lavinia ------------------------------------------------"
scrapy crawl sp_lavinia -a start=2025-04-28 -o sp_lavinia.csv --logfile=sp_lavinia.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_luiziania ------------------------------------------------"
scrapy crawl sp_luiziania -a start=2025-04-28 -o sp_luiziania.csv --logfile=sp_luiziania.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_macatuba ------------------------------------------------"
scrapy crawl sp_macatuba -a start=2025-04-28 -o sp_macatuba.csv --logfile=sp_macatuba.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_macaubal ------------------------------------------------"
scrapy crawl sp_macaubal -a start=2025-04-28 -o sp_macaubal.csv --logfile=sp_macaubal.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_marilia ------------------------------------------------"
scrapy crawl sp_marilia -a start=2025-04-28 -o sp_marilia.csv --logfile=sp_marilia.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_mira_estrela ------------------------------------------------"
scrapy crawl sp_mira_estrela -a start=2025-04-28 -o sp_mira_estrela.csv --logfile=sp_mira_estrela.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_mirante_do_paranapanema ------------------------------------------------"
scrapy crawl sp_mirante_do_paranapanema -a start=2025-04-28 -o sp_mirante_do_paranapanema.csv --logfile=sp_mirante_do_paranapanema.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_mogi_guacu ------------------------------------------------"
scrapy crawl sp_mogi_guacu -a start=2025-04-28 -o sp_mogi_guacu.csv --logfile=sp_mogi_guacu.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_monte_alto_2017 ------------------------------------------------"
scrapy crawl sp_monte_alto_2017 -a start=2025-04-28 -o sp_monte_alto_2017.csv --logfile=sp_monte_alto_2017.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_monte_alto_sigpub ------------------------------------------------"
scrapy crawl sp_monte_alto_sigpub -a start=2025-04-28 -o sp_monte_alto_sigpub.csv --logfile=sp_monte_alto_sigpub.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_monte_mor ------------------------------------------------"
scrapy crawl sp_monte_mor -a start=2025-04-28 -o sp_monte_mor.csv --logfile=sp_monte_mor.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_monteiro_lobato ------------------------------------------------"
scrapy crawl sp_monteiro_lobato -a start=2025-04-28 -o sp_monteiro_lobato.csv --logfile=sp_monteiro_lobato.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_nhandeara ------------------------------------------------"
scrapy crawl sp_nhandeara -a start=2025-04-28 -o sp_nhandeara.csv --logfile=sp_nhandeara.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_nova_castilho ------------------------------------------------"
scrapy crawl sp_nova_castilho -a start=2025-04-28 -o sp_nova_castilho.csv --logfile=sp_nova_castilho.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_nova_luzitania ------------------------------------------------"
scrapy crawl sp_nova_luzitania -a start=2025-04-28 -o sp_nova_luzitania.csv --logfile=sp_nova_luzitania.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_osasco ------------------------------------------------"
scrapy crawl sp_osasco -a start=2025-04-28 -o sp_osasco.csv --logfile=sp_osasco.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_ourinhos ------------------------------------------------"
scrapy crawl sp_ourinhos -a start=2025-04-28 -o sp_ourinhos.csv --logfile=sp_ourinhos.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_palmital ------------------------------------------------"
scrapy crawl sp_palmital -a start=2025-04-28 -o sp_palmital.csv --logfile=sp_palmital.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_parisi ------------------------------------------------"
scrapy crawl sp_parisi -a start=2025-04-28 -o sp_parisi.csv --logfile=sp_parisi.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_patrocinio_paulista ------------------------------------------------"
scrapy crawl sp_patrocinio_paulista -a start=2025-04-28 -o sp_patrocinio_paulista.csv --logfile=sp_patrocinio_paulista.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_paulinia ------------------------------------------------"
scrapy crawl sp_paulinia -a start=2025-04-28 -o sp_paulinia.csv --logfile=sp_paulinia.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_penapolis ------------------------------------------------"
scrapy crawl sp_penapolis -a start=2025-04-28 -o sp_penapolis.csv --logfile=sp_penapolis.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_piedade ------------------------------------------------"
scrapy crawl sp_piedade -a start=2025-04-28 -o sp_piedade.csv --logfile=sp_piedade.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_pindorama ------------------------------------------------"
scrapy crawl sp_pindorama -a start=2025-04-28 -o sp_pindorama.csv --logfile=sp_pindorama.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_piracicaba ------------------------------------------------"
scrapy crawl sp_piracicaba -a start=2025-04-28 -o sp_piracicaba.csv --logfile=sp_piracicaba.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_planalto ------------------------------------------------"
scrapy crawl sp_planalto -a start=2025-04-28 -o sp_planalto.csv --logfile=sp_planalto.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_poloni ------------------------------------------------"
scrapy crawl sp_poloni -a start=2025-04-28 -o sp_poloni.csv --logfile=sp_poloni.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_pontes_gestal ------------------------------------------------"
scrapy crawl sp_pontes_gestal -a start=2025-04-28 -o sp_pontes_gestal.csv --logfile=sp_pontes_gestal.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_porangaba ------------------------------------------------"
scrapy crawl sp_porangaba -a start=2025-04-28 -o sp_porangaba.csv --logfile=sp_porangaba.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_potirendaba ------------------------------------------------"
scrapy crawl sp_potirendaba -a start=2025-04-28 -o sp_potirendaba.csv --logfile=sp_potirendaba.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_pratania ------------------------------------------------"
scrapy crawl sp_pratania -a start=2025-04-28 -o sp_pratania.csv --logfile=sp_pratania.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_presidente_epitacio ------------------------------------------------"
scrapy crawl sp_presidente_epitacio -a start=2025-04-28 -o sp_presidente_epitacio.csv --logfile=sp_presidente_epitacio.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_presidente_prudente ------------------------------------------------"
scrapy crawl sp_presidente_prudente -a start=2025-04-28 -o sp_presidente_prudente.csv --logfile=sp_presidente_prudente.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_rio_claro ------------------------------------------------"
scrapy crawl sp_rio_claro -a start=2025-04-28 -o sp_rio_claro.csv --logfile=sp_rio_claro.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_salto ------------------------------------------------"
scrapy crawl sp_salto -a start=2025-04-28 -o sp_salto.csv --logfile=sp_salto.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_santa_ernestina ------------------------------------------------"
scrapy crawl sp_santa_ernestina -a start=2025-04-28 -o sp_santa_ernestina.csv --logfile=sp_santa_ernestina.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_santa_maria_da_serra ------------------------------------------------"
scrapy crawl sp_santa_maria_da_serra -a start=2025-04-28 -o sp_santa_maria_da_serra.csv --logfile=sp_santa_maria_da_serra.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_santo_andre ------------------------------------------------"
scrapy crawl sp_santo_andre -a start=2025-04-28 -o sp_santo_andre.csv --logfile=sp_santo_andre.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_santos ------------------------------------------------"
scrapy crawl sp_santos -a start=2025-04-28 -o sp_santos.csv --logfile=sp_santos.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_sao_bernardo_do_campo ------------------------------------------------"
scrapy crawl sp_sao_bernardo_do_campo -a start=2025-04-28 -o sp_sao_bernardo_do_campo.csv --logfile=sp_sao_bernardo_do_campo.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_sao_jose_dos_campos ------------------------------------------------"
scrapy crawl sp_sao_jose_dos_campos -a start=2025-04-28 -o sp_sao_jose_dos_campos.csv --logfile=sp_sao_jose_dos_campos.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_sao_manuel ------------------------------------------------"
scrapy crawl sp_sao_manuel -a start=2025-04-28 -o sp_sao_manuel.csv --logfile=sp_sao_manuel.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_sao_paulo ------------------------------------------------"
scrapy crawl sp_sao_paulo -a start=2025-04-28 -o sp_sao_paulo.csv --logfile=sp_sao_paulo.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_sao_pedro ------------------------------------------------"
scrapy crawl sp_sao_pedro -a start=2025-04-28 -o sp_sao_pedro.csv --logfile=sp_sao_pedro.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_sao_roque ------------------------------------------------"
scrapy crawl sp_sao_roque -a start=2025-04-28 -o sp_sao_roque.csv --logfile=sp_sao_roque.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_sarutaia ------------------------------------------------"
scrapy crawl sp_sarutaia -a start=2025-04-28 -o sp_sarutaia.csv --logfile=sp_sarutaia.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_sebastianopolis_do_sul ------------------------------------------------"
scrapy crawl sp_sebastianopolis_do_sul -a start=2025-04-28 -o sp_sebastianopolis_do_sul.csv --logfile=sp_sebastianopolis_do_sul.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_sertaozinho ------------------------------------------------"
scrapy crawl sp_sertaozinho -a start=2025-04-28 -o sp_sertaozinho.csv --logfile=sp_sertaozinho.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_sumare ------------------------------------------------"
scrapy crawl sp_sumare -a start=2025-04-28 -o sp_sumare.csv --logfile=sp_sumare.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_tapirai ------------------------------------------------"
scrapy crawl sp_tapirai -a start=2025-04-28 -o sp_tapirai.csv --logfile=sp_tapirai.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_taquaral ------------------------------------------------"
scrapy crawl sp_taquaral -a start=2025-04-28 -o sp_taquaral.csv --logfile=sp_taquaral.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_taubate ------------------------------------------------"
scrapy crawl sp_taubate -a start=2025-04-28 -o sp_taubate.csv --logfile=sp_taubate.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_terra_roxa ------------------------------------------------"
scrapy crawl sp_terra_roxa -a start=2025-04-28 -o sp_terra_roxa.csv --logfile=sp_terra_roxa.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_tremembe ------------------------------------------------"
scrapy crawl sp_tremembe -a start=2025-04-28 -o sp_tremembe.csv --logfile=sp_tremembe.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_turiuba ------------------------------------------------"
scrapy crawl sp_turiuba -a start=2025-04-28 -o sp_turiuba.csv --logfile=sp_turiuba.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_uniao_paulista ------------------------------------------------"
scrapy crawl sp_uniao_paulista -a start=2025-04-28 -o sp_uniao_paulista.csv --logfile=sp_uniao_paulista.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_valinhos ------------------------------------------------"
scrapy crawl sp_valinhos -a start=2025-04-28 -o sp_valinhos.csv --logfile=sp_valinhos.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_valparaiso ------------------------------------------------"
scrapy crawl sp_valparaiso -a start=2025-04-28 -o sp_valparaiso.csv --logfile=sp_valparaiso.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_vera_cruz ------------------------------------------------"
scrapy crawl sp_vera_cruz -a start=2025-04-28 -o sp_vera_cruz.csv --logfile=sp_vera_cruz.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_vinhedo ------------------------------------------------"
scrapy crawl sp_vinhedo -a start=2025-04-28 -o sp_vinhedo.csv --logfile=sp_vinhedo.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_votorantim ------------------------------------------------"
scrapy crawl sp_votorantim -a start=2025-04-28 -o sp_votorantim.csv --logfile=sp_votorantim.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR sp_votuporanga ------------------------------------------------"
scrapy crawl sp_votuporanga -a start=2025-04-28 -o sp_votuporanga.csv --logfile=sp_votuporanga.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR to_aguiarnopolis ------------------------------------------------"
scrapy crawl to_aguiarnopolis -a start=2025-04-28 -o to_aguiarnopolis.csv --logfile=to_aguiarnopolis.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR to_aparecida_do_rio_negro ------------------------------------------------"
scrapy crawl to_aparecida_do_rio_negro -a start=2025-04-28 -o to_aparecida_do_rio_negro.csv --logfile=to_aparecida_do_rio_negro.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR to_araguaina ------------------------------------------------"
scrapy crawl to_araguaina -a start=2025-04-28 -o to_araguaina.csv --logfile=to_araguaina.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR to_axixa_do_tocantins ------------------------------------------------"
scrapy crawl to_axixa_do_tocantins -a start=2025-04-28 -o to_axixa_do_tocantins.csv --logfile=to_axixa_do_tocantins.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR to_campos_lindos ------------------------------------------------"
scrapy crawl to_campos_lindos -a start=2025-04-28 -o to_campos_lindos.csv --logfile=to_campos_lindos.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR to_caseara ------------------------------------------------"
scrapy crawl to_caseara -a start=2025-04-28 -o to_caseara.csv --logfile=to_caseara.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR to_centenario ------------------------------------------------"
scrapy crawl to_centenario -a start=2025-04-28 -o to_centenario.csv --logfile=to_centenario.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR to_divinopolis_do_tocantins ------------------------------------------------"
scrapy crawl to_divinopolis_do_tocantins -a start=2025-04-28 -o to_divinopolis_do_tocantins.csv --logfile=to_divinopolis_do_tocantins.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR to_goiatins ------------------------------------------------"
scrapy crawl to_goiatins -a start=2025-04-28 -o to_goiatins.csv --logfile=to_goiatins.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR to_gurupi ------------------------------------------------"
scrapy crawl to_gurupi -a start=2025-04-28 -o to_gurupi.csv --logfile=to_gurupi.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR to_itapiratins_2017 ------------------------------------------------"
scrapy crawl to_itapiratins_2017 -a start=2025-04-28 -o to_itapiratins_2017.csv --logfile=to_itapiratins_2017.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR to_lagoa_da_confusao ------------------------------------------------"
scrapy crawl to_lagoa_da_confusao -a start=2025-04-28 -o to_lagoa_da_confusao.csv --logfile=to_lagoa_da_confusao.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR to_lagoa_de_tocantins ------------------------------------------------"
scrapy crawl to_lagoa_de_tocantins -a start=2025-04-28 -o to_lagoa_de_tocantins.csv --logfile=to_lagoa_de_tocantins.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR to_miracema ------------------------------------------------"
scrapy crawl to_miracema -a start=2025-04-28 -o to_miracema.csv --logfile=to_miracema.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR to_muricilandia ------------------------------------------------"
scrapy crawl to_muricilandia -a start=2025-04-28 -o to_muricilandia.csv --logfile=to_muricilandia.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR to_nazare ------------------------------------------------"
scrapy crawl to_nazare -a start=2025-04-28 -o to_nazare.csv --logfile=to_nazare.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR to_palmas ------------------------------------------------"
scrapy crawl to_palmas -a start=2025-04-28 -o to_palmas.csv --logfile=to_palmas.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR to_peixe ------------------------------------------------"
scrapy crawl to_peixe -a start=2025-04-28 -o to_peixe.csv --logfile=to_peixe.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR to_ponte_alta_do_tocantins ------------------------------------------------"
scrapy crawl to_ponte_alta_do_tocantins -a start=2025-04-28 -o to_ponte_alta_do_tocantins.csv --logfile=to_ponte_alta_do_tocantins.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR to_pugmil ------------------------------------------------"
scrapy crawl to_pugmil -a start=2025-04-28 -o to_pugmil.csv --logfile=to_pugmil.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR to_recursolandia ------------------------------------------------"
scrapy crawl to_recursolandia -a start=2025-04-28 -o to_recursolandia.csv --logfile=to_recursolandia.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR to_sampaio ------------------------------------------------"
scrapy crawl to_sampaio -a start=2025-04-28 -o to_sampaio.csv --logfile=to_sampaio.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR to_santa_fe_do_araguaia ------------------------------------------------"
scrapy crawl to_santa_fe_do_araguaia -a start=2025-04-28 -o to_santa_fe_do_araguaia.csv --logfile=to_santa_fe_do_araguaia.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR to_talisma ------------------------------------------------"
scrapy crawl to_talisma -a start=2025-04-28 -o to_talisma.csv --logfile=to_talisma.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR to_tocantinia ------------------------------------------------"
scrapy crawl to_tocantinia -a start=2025-04-28 -o to_tocantinia.csv --logfile=to_tocantinia.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR to_tocantinopolis ------------------------------------------------"
scrapy crawl to_tocantinopolis -a start=2025-04-28 -o to_tocantinopolis.csv --logfile=to_tocantinopolis.log
rm -rf data/
echo "------------------------------------------------ TESTANDO RASPADOR to_tupirama ------------------------------------------------"
scrapy crawl to_tupirama -a start=2025-04-28 -o to_tupirama.csv --logfile=to_tupirama.log
rm -rf data/
