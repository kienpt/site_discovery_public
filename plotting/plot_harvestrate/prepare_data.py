"""
Input: chronological-ordered urls and classified urls.
- website discovery tool
- seed finder 
- ache 

Action:
Transform crawled data to plot-ready format:

Method1, #Relev / 1 crawled papes, #Relev / 2 crawled pages
"""
import sys
sys.path.append("../../utils/")
sys.path.append("../")
from urlutility import URLUtility
from file_names import get_filenames

def _read_clf_file(clf_file):
    url2label = {}
    site2label = {}

    with open(clf_file) as lines:
        for line in lines:
            try:
                values = line.strip().split(",")
                url = ''.join(values[:-1])
                label = int(values[-1])
                url = URLUtility.normalize(url)
                site = URLUtility.get_host(url)

                if label>0:
                    url2label[url] = True
                    site2label[site] = True
                else:
                    url2label[url] = False
                    if site not in site2label:
                        site2label[site] = False
            except:
                print line
    return url2label, site2label

def _read_result_file(result_file):
    urls = []
    with open(result_file) as lines:
        for line in lines:
            values = line.strip().split(",")
            url = values[0]
            url = URLUtility.normalize(url)
            urls.append(url)
    return urls

def _read_sf_result_file(result_file):
    urls = []
    with open(result_file) as lines:
        for line in lines:
            values = line.strip().split(', ') 
            url = values[-1]
            url = URLUtility.normalize(url)
            urls.append(url)
    return urls

def _read_ac_result_file(result_file):
    urls = []
    with open(result_file) as lines:
        for line in lines:  
            url = line.split()[0]
            url = URLUtility.normalize(url)
            urls.append(url)
    return urls

def _count_relev(url2label, site2label, urls):
    relev_pages = []
    relev_sites = []
    p = 0
    s = 0 
    counted_sites = set()
    for url in urls:
        site = URLUtility.get_host(url)
        if url in url2label:
            if url2label[url]:
                p += 1
            relev_pages.append(p)
            if site2label[site] and site not in counted_sites:
                s += 1
                counted_sites.add(site)
            relev_sites.append(s)
    return relev_pages, relev_sites

def prepare_wdt(result_file, clf_file):
    """
    Prepare data from website discovery tool

    Args:
    - result_file: output from wdt
    - clf_file: classification result
    """
    url2label, site2label = _read_clf_file(clf_file)
    urls = _read_result_file(result_file) # urls ordered by timestamp
    relev_pages, relev_sites = _count_relev(url2label, site2label, urls)
    return relev_pages, relev_sites

def prepare_seedfinder(result_file, clf_file):
    url2label, site2label = _read_clf_file(clf_file)
    urls = _read_sf_result_file(result_file) 
    relev_pages, relev_sites = _count_relev(url2label, site2label, urls)
    return relev_pages, relev_sites

def prepare_ache(result_file, clf_file):
    url2label, site2label = _read_clf_file(clf_file)
    urls = _read_ac_result_file(result_file) 
    relev_pages, relev_sites = _count_relev(url2label, site2label, urls)
    return relev_pages, relev_sites

def prepare_data(kw_files, bl_files, rl_files, fw_files, mix_files, sf_files, ac_files, bi_files, outfile):
    """
    output:
    #pages, #ache_relev_pages, #sf_relev_pages, #wdt_relev_pages
    #pages, #ache_relev_sites, #sf_relev_sites, #wdt_relev_sites
    """
    kw_res_file, kw_clf_file = kw_files
    bl_res_file, bl_clf_file = bl_files
    rl_res_file, rl_clf_file = rl_files
    fw_res_file, fw_clf_file = fw_files
    mix_res_file, mix_clf_file = mix_files
    sf_res_file, sf_clf_file = sf_files
    ac_res_file, ac_clf_file = ac_files
    bi_res_file, bi_clf_file = bi_files
    out = open(outfile, 'w')
    kw_pages, kw_sites = prepare_wdt(kw_res_file, kw_clf_file)
    bl_pages, bl_sites = prepare_wdt(bl_res_file, bl_clf_file)
    rl_pages, rl_sites = prepare_wdt(rl_res_file, rl_clf_file)
    fw_pages, fw_sites = prepare_wdt(fw_res_file, fw_clf_file)
    mix_pages, mix_sites = prepare_wdt(mix_res_file, mix_clf_file)
    sf_pages, sf_sites = prepare_seedfinder(sf_res_file, sf_clf_file)
    ac_pages, ac_sites = prepare_ache(ac_res_file, ac_clf_file)
    bi_pages, bi_sites = prepare_ache(bi_res_file, bi_clf_file)
    n = max(len(kw_pages), len(bl_pages), len(rl_pages), len(fw_pages), len(mix_pages), len(sf_pages), len(ac_pages), len(bi_pages))
    out.write('all,' + ','.join([str(i) for i in xrange(n)]) + '\n')
    out.write('KEYWORD,' + ','.join([str(i) for i in kw_pages])+ '\n')
    out.write('BACKWARD,' + ','.join([str(i) for i in bl_pages])+ '\n')
    out.write('RELATED,' + ','.join([str(i) for i in rl_pages])+ '\n')
    out.write('FORWARD,' + ','.join([str(i) for i in fw_pages])+ '\n')
    out.write('BANDIT,' + ','.join([str(i) for i in mix_pages])+ '\n')
    out.write('SEEDFINDER,' + ','.join([str(i) for i in sf_pages])+ '\n')
    out.write('ACHE,' + ','.join([str(i) for i in ac_pages])+ '\n')
    out.write('BIPARTITE,' + ','.join([str(i) for i in bi_pages])+ '\n')

    out.write('KEYWORD,' + ','.join([str(i) for i in kw_sites])+ '\n')
    out.write('BACKWARD,' + ','.join([str(i) for i in bl_sites])+ '\n')
    out.write('RELATED,' + ','.join([str(i) for i in rl_sites])+ '\n')
    out.write('FORWARD,' + ','.join([str(i) for i in fw_sites])+ '\n')
    out.write('BANDIT,' + ','.join([str(i) for i in mix_sites])+ '\n')
    out.write('SEEDFINDER,' + ','.join([str(i) for i in sf_sites])+ '\n')
    out.write('ACHE,' + ','.join([str(i) for i in ac_sites])+ '\n')
    out.write('BIPARTITE,' + ','.join([str(i) for i in bi_sites])+ '\n')
    out.close()

def main(domain):
    kw_files, bl_files, rl_files, fw_files, bandit_files, sf_files, ac_files, bi_files, outfile = get_filenames(domain)
    prepare_data(kw_files, bl_files, rl_files, fw_files, bandit_files, sf_files, ac_files, bi_files, outfile)

main(sys.argv[1])
