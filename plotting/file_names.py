def get_filenames(domain):
    if domain == 'forum':
        fname = 'result_atf_stacking_search-kw_count-50_1530573706.79.csv' #50k
        kw_files = ['../../data/discovery/forum/keyword/' + fname,
                    '../../data/discovery/forum/keyword/' + fname + '.classification']
        fname = 'result_atf_stacking_search-bl_count-50_1530738010.2.csv' #50K
        bl_files = ['../../data/discovery/forum/backlink/' + fname,
                    '../../data/discovery/forum/backlink/' + fname + '.classification']
        fname = 'result_atf_stacking_search-rl_count-50_1530732222.28.csv' #50k
        rl_files = ['../../data/discovery/forum/related/' + fname,
                    '../../data/discovery/forum/related/' + fname + '.classification']
        fname = 'result_atf_stacking_search-fw_count-50_1531369359.77.csv' #50k
        fw_files = ['../../data/discovery/forum/forward/' + fname,
                    '../../data/discovery/forum/forward/' + fname + '.classification']
        fname = 'result_atf_stacking_search-bandit_count-50_1531073652.78.csv' #50k
        bandit_files = ['/home/vgc/kienpham/memex_project/site_discovery/data/discovery/forum/bandit/'+fname,
                     '/home/vgc/kienpham/memex_project/site_discovery/data/discovery/forum/bandit/' + fname + '.classification']


        sf_files = ['../../baselines/ache/results/atf_forum_nocv_maxpages5/forum_nocv.csv',
                    '../../data/discovery/seedfinder/forum_classification.csv']
        ac_files = ['../../baselines/ache/results/forum_crawl_hard_10/default/data_monitor/crawledpages.csv', 
                    '../../data/discovery/ache/forum_hard_10_classification.csv'] # 10 hard
        bi_files = ['../../baselines/ache/results/forum_bipartite/default/data_monitor/crawledpages.csv',
                    '../../data/discovery/bipartite/forum_classification.csv'] 
        outfile = 'forum.csv'

    elif domain == 'ads':
        fname = 'result_atf_stacking_search-kw_count-50_1530664888.25.csv' # 50k
        kw_files = ['../../data/discovery/ads/keyword/' + fname,
                    '../../data/discovery/ads/keyword/' + fname + '.classification']
        fname = 'result_atf_stacking_search-bl_count-50_1531100629.87.csv' # 50k
        bl_files = ['../../data/discovery/ads/backlink/' + fname,
                    '../../data/discovery/ads/backlink/' + fname + '.classification']
        fname = 'result_atf_stacking_search-rl_count-50_1531631713.76.csv' # 50k
        rl_files = ['/home/vgc/kienpham/memex_project/site_discovery//data/discovery/ads/related/' + fname,
                    '/home/vgc/kienpham/memex_project/site_discovery//data/discovery/ads/related/' + fname + '.classification']
        fname = 'result_atf_stacking_search-fw_count-50_1531200713.74.csv' # 50k
        fw_files = ['../../data/discovery/ads/forward/' + fname,
                    '../../data/discovery/ads/forward/' + fname + '.classification']

        fname = 'result_atf_stacking_search-bandit_count-50_1531115744.04.csv' # 50k
        bandit_files = ['/home/vgc/kienpham/memex_project/site_discovery//data/discovery/ads/bandit/' + fname,
                     '/home/vgc/kienpham/memex_project/site_discovery/data/discovery/ads/bandit/' + fname + '.classification']

        sf_files = ['../../baselines/ache/results/atf_ads_nocv_maxpages5/ads_nocv.csv',
                    '../../data/discovery/seedfinder/ads_classification.csv']
        ac_files = ['../../baselines/ache/results/ads_crawl_hard_10/default/data_monitor/crawledpages.csv',
                    '../../data/discovery/ache/ads_hard_10_classification.csv'] # 10 hard
        bi_files = ['../../baselines/ache/results/ads_bipartite/default/data_monitor/crawledpages.csv',
                    '../../data/discovery/bipartite/ads_classification.csv']
        outfile = 'ads.csv'

    elif domain == 'ht':
        fname = 'result_ht_stacking_search-kw_count-50_1530635004.67.csv' # 10 hard
        kw_files = ['../../data/discovery/escort/keyword/' + fname,
                    '../../data/discovery/escort/keyword/' + fname + '.classification']
        fname = 'result_ht_stacking_search-bl_count-50_1531156079.24.csv'
        bl_files = ['../../data/discovery/escort/backlink/' + fname,
                    '../../data/discovery/escort/backlink/' + fname + '.classification'] # 50k
        fname = 'result_ht_stacking_search-rl_count-50_1531364504.0.csv' #50k
        rl_files = ['/home/vgc/kienpham/memex_project/site_discovery/data/discovery/escort/related/' + fname,
                    '/home/vgc/kienpham/memex_project/site_discovery/data/discovery/escort/related/' + fname + '.classification']
        fname = 'result_ht_stacking_search-fw_count-50_1530807787.68.csv' # 50k
        fw_files = ['../../data/discovery/escort/forward/' + fname,
                    '../../data/discovery/escort/forward/' + fname + '.classification']

        fname = 'result_ht_stacking_search-bandit_count-50_1531200883.78.csv' # 50k
        bandit_files = ['/home/vgc/kienpham/memex_project/site_discovery/data/discovery/escort/bandit/' + fname,
                     '/home/vgc/kienpham/memex_project/site_discovery/data/discovery/escort/bandit/' + fname +  '.classification']

        sf_files = ['../../baselines/ache/results/escort_nocv_maxpages5/escort_bing_api_200queries.csv',
                    '../../data/discovery/seedfinder/escort_classification.csv']
        ac_files = ['../../baselines/ache/results/escort_crawl_hard_10/default/data_monitor/crawledpages.csv',
                    '../../data/discovery/ache/escort_hard_10_classification.csv'] # 10 hard
        bi_files = ['../../baselines/ache/results/escort_bipartite/default/data_monitor/crawledpages.csv',
                    '../../data/discovery/bipartite/escort_classification.csv']

        outfile = 'ht.csv'
    return kw_files, bl_files, rl_files, fw_files, bandit_files, sf_files, ac_files, bi_files, outfile
