mkdir data
python prepare_data_for_r.py -i ../../experimental_results/seed_variation_05_09_2018/ads_dmoz_seednumb_1.txt -o data -d ATF-Ads-DMOZ
python prepare_data_for_r.py -i ../../experimental_results/seed_variation_05_09_2018/forum_dmoz_seednumb_1.txt -o data -d ATF-Forum-DMOZ
python prepare_data_for_r.py -i ../../experimental_results/seed_variation_05_09_2018/escort_dmoz_seednumb_1.txt -o data -d Escort-DMOZ
python prepare_data_for_r.py -i ../../experimental_results/seed_variation_05_09_2018/sec_dmoz_seednumb_1.txt -o data -d SEC-DMOZ
