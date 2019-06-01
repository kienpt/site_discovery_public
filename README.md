# Site Discovery
This repository contains the source code for the following paper:

Bootstrapping Domain-Specific Content Discovery on the Web, Kien Pham, Aecio Santos and Juliana Freire, The Web Conference 2019.

# How to start:
- Register account for Bing APIs, Google Custome Search API and MOZ API.
- Add the access keys associated with the account to set up the search apis in search_apis/search_apis.py 
- Install dependencies:
	- https://github.com/misja/python-boilerpipe.git
	- nltk
	- svmlight
	- google-api-python-client
- Run the main function in discovery/site_discovery.py
	- Show help: python discovery/site_discover.py -h
	- Search operators:
		- bl = backlink search
		- kw = keyword search
		- rl = related search 
		- fw = forward search
		- bandit = use UCB to select a search operator at each iteration -> best method.
		- mix = other strategy
	- Example
	```
	python discovery/site_discovery.py -seed data/seeds/atf/atf_ads.txt -out data/discovery/ads/bandit -rank stacking -re body -o -count 50 -search bandit -i 20 -skw "gun classified" -neg data/candidates/dmoz/negative_dmoz_sites.txt
	```.

## The code in this repository is available under Apache license 2.0
