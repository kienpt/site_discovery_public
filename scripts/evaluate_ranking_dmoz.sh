python evaluation/evaluate.py -re body -seed data/seeds/atf/atf_ads.txt -cand data/candidates/dmoz/dmoz_sites.txt -neg data/candidates/dmoz/negative_dmoz_sites.txt -out data/evaluation/dmoz -mc 1276 -rank all -o  -se search -mp 1  > log/ads_dmoz_1.txt
#python evaluation/evaluate.py -re body -seed data/seeds/atf/atf_ads.txt -cand data/candidates/dmoz/dmoz_sites.txt -neg data/candidates/dmoz/negative_dmoz_sites.txt -out data/evaluation/dmoz -mc 1276 -rank all -o  -se search -mp 2  > log/ads_dmoz_2.txt
#python evaluation/evaluate.py -re body -seed data/seeds/atf/atf_ads.txt -cand data/candidates/dmoz/dmoz_sites.txt -neg data/candidates/dmoz/negative_dmoz_sites.txt -out data/evaluation/dmoz -mc 1276 -rank all -o  -se search -mp 3  > log/ads_dmoz_3.txt
#python evaluation/evaluate.py -re body -seed data/seeds/atf/atf_ads.txt -cand data/candidates/dmoz/dmoz_sites.txt -neg data/candidates/dmoz/negative_dmoz_sites.txt -out data/evaluation/dmoz -mc 1276 -rank all -o  -se search -mp 4  > log/ads_dmoz_4.txt
#python evaluation/evaluate.py -re body -seed data/seeds/atf/atf_ads.txt -cand data/candidates/dmoz/dmoz_sites.txt -neg data/candidates/dmoz/negative_dmoz_sites.txt -out data/evaluation/dmoz -mc 1276 -rank all -o  -se search -mp 5  > log/ads_dmoz_5.txt

python evaluation/evaluate.py -re body -seed data/seeds/atf/atf_market.txt -cand data/candidates/dmoz/dmoz_sites.txt -neg data/candidates/dmoz/negative_dmoz_sites.txt -out data/evaluation/dmoz -mc 2160 -rank all -o  -se search -mp 1  > log/market_dmoz_1.txt
#python evaluation/evaluate.py -re body -seed data/seeds/atf/atf_market.txt -cand data/candidates/dmoz/dmoz_sites.txt -neg data/candidates/dmoz/negative_dmoz_sites.txt -out data/evaluation/dmoz -mc 2160 -rank all -o  -se search -mp 2  > log/market_dmoz_2.txt
#python evaluation/evaluate.py -re body -seed data/seeds/atf/atf_market.txt -cand data/candidates/dmoz/dmoz_sites.txt -neg data/candidates/dmoz/negative_dmoz_sites.txt -out data/evaluation/dmoz -mc 2160 -rank all -o  -se search -mp 3  > log/market_dmoz_3.txt
#python evaluation/evaluate.py -re body -seed data/seeds/atf/atf_market.txt -cand data/candidates/dmoz/dmoz_sites.txt -neg data/candidates/dmoz/negative_dmoz_sites.txt -out data/evaluation/dmoz -mc 2160 -rank all -o  -se search -mp 4  > log/market_dmoz_4.txt
#python evaluation/evaluate.py -re body -seed data/seeds/atf/atf_market.txt -cand data/candidates/dmoz/dmoz_sites.txt -neg data/candidates/dmoz/negative_dmoz_sites.txt -out data/evaluation/dmoz -mc 2160 -rank all -o  -se search -mp 5  > log/market_dmoz_5.txt

python evaluation/evaluate.py -re body -seed data/seeds/atf/atf_forums.txt -cand data/candidates/dmoz/dmoz_sites.txt -neg data/candidates/dmoz/negative_dmoz_sites.txt -out data/evaluation/dmoz -mc 7219 -rank all -o  -se search -mp 1  > log/forum_dmoz_1.txt
#python evaluation/evaluate.py -re body -seed data/seeds/atf/atf_forums.txt -cand data/candidates/dmoz/dmoz_sites.txt -neg data/candidates/dmoz/negative_dmoz_sites.txt -out data/evaluation/dmoz -mc 7219 -rank all -o  -se search -mp 2  > log/forum_dmoz_2.txt
#python evaluation/evaluate.py -re body -seed data/seeds/atf/atf_forums.txt -cand data/candidates/dmoz/dmoz_sites.txt -neg data/candidates/dmoz/negative_dmoz_sites.txt -out data/evaluation/dmoz -mc 7219 -rank all -o  -se search -mp 3  > log/forum_dmoz_3.txt
#python evaluation/evaluate.py -re body -seed data/seeds/atf/atf_forums.txt -cand data/candidates/dmoz/dmoz_sites.txt -neg data/candidates/dmoz/negative_dmoz_sites.txt -out data/evaluation/dmoz -mc 7219 -rank all -o  -se search -mp 4  > log/forum_dmoz_4.txt
#python evaluation/evaluate.py -re body -seed data/seeds/atf/atf_forums.txt -cand data/candidates/dmoz/dmoz_sites.txt -neg data/candidates/dmoz/negative_dmoz_sites.txt -out data/evaluation/dmoz -mc 7219 -rank all -o  -se search -mp 5  > log/forum_dmoz_5.txt

# SEC domain
python evaluation/evaluate.py -re body -seed data/seeds/sec/relevant_sites.txt -cand data/candidates/dmoz/dmoz_sites.txt -neg data/candidates/dmoz/negative_dmoz_sites.txt -out data/evaluation/dmoz -mc 5000 -rank all -o  -se search -mp 1  > log/sec_dmoz_1.txt

# Escort domain
python evaluation/evaluate.py -re body -seed data/seeds/ht/filter_escort.txt -cand data/candidates/dmoz/dmoz_sites.txt -neg data/candidates/dmoz/negative_dmoz_sites.txt -out data/evaluation/dmoz -mc 5000 -rank all -o  -se search -mp 1  > log/escort_dmoz_1.txt

# Politics domain
#python evaluation/evaluate.py -re body -seed data/seeds/politics/politics.txt -cand data/candidates/dmoz/dmoz_sites.txt -neg data/candidates/dmoz/negative_dmoz_sites.txt -out data/evaluation/dmoz -mc 5000 -rank all -o  -se search -mp 1  > log/politics_dmoz_1.txt
