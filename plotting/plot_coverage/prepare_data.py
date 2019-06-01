"""
Transform crawled data to plot-ready format:
Method,coverage
"""

import sys
sys.path.append("../../utils/")
sys.path.append("../")
from urlutility import URLUtility
from file_names import get_filenames
import traceback

def _read_result_file(result_file, max_pages):
    """
    Load all sites from the result file of wdt tool
    """
    sites = set()
    count = 0
    with open(result_file) as lines:
        for line in lines:
            count += 1
            values = line.strip().split(",")
            url = values[0]
            url = URLUtility.normalize(url)
            site = URLUtility.get_host(url)
            sites.add(site)
            if count == max_pages:
                break
    return sites

def _read_sf_result_file(result_file, max_pages):
    """
    Load all sites from the result file of SEEDFINDER 
    """
    sites = set()
    count = 0
    with open(result_file) as lines:
        for line in lines:
            count += 1
            values = line.strip().split(', ') 
            url = values[-1]
            url = URLUtility.normalize(url)
            site = URLUtility.get_host(url)
            sites.add(site)
            if count == max_pages:
                break
    return sites

def _read_ac_result_file(result_file, max_pages):
    """
    Load all sites from the result file of ACHE 
    """
    count = 0
    sites = set()
    with open(result_file) as lines:
        for line in lines:  
            count += 1
            url = line.split()[0]
            url = URLUtility.normalize(url)
            site = URLUtility.get_host(url)
            sites.add(site)
            if count == max_pages:
                break
    return sites

def _read_relev_file(clf_file):
    """
    Load all sites from the classification file
    Note that all classification files from different discovery tools have the same format
    """
    sites = set()
    with open(clf_file) as lines:
        for line in lines:
            try:
                values = line.strip().split(",")
                url = ''.join(values[:-1])
                label = int(values[-1])
                url = URLUtility.normalize(url)
                site = URLUtility.get_host(url)
                if label != -1 and label != 1:
                    print "Parsed label is incorrect"
                if label==1:
                    sites.add(site)
            except:
                traceback.print_exc()
    return sites

def read(kw_files, bl_files, rl_files, fw_files, bandit_files, sf_files, ac_files, bi_files):
    max_pages = 50000
    print "Maximum number of pages: ", max_pages
    kw_res_file, kw_clf_file = kw_files
    bl_res_file, bl_clf_file = bl_files
    rl_res_file, rl_clf_file = rl_files
    fw_res_file, fw_clf_file = fw_files
    bandit_res_file, bandit_clf_file = bandit_files
    sf_res_file, sf_clf_file = sf_files
    ac_res_file, ac_clf_file = ac_files
    bi_res_file, bi_clf_file = bi_files

    # Load sites classification files
    kw_relev = _read_relev_file(kw_clf_file)
    bl_relev = _read_relev_file(bl_clf_file)
    rl_relev = _read_relev_file(rl_clf_file)
    fw_relev = _read_relev_file(fw_clf_file)
    bandit_relev = _read_relev_file(bandit_clf_file)
    sf_relev = _read_relev_file(sf_clf_file)
    ac_relev = _read_relev_file(ac_clf_file)
    bi_relev = _read_relev_file(bi_clf_file)

    # Load sites from result files
    kw_sites = _read_result_file(kw_res_file, max_pages) 
    bl_sites = _read_result_file(bl_res_file, max_pages) 
    rl_sites = _read_result_file(rl_res_file, max_pages) 
    fw_sites = _read_result_file(fw_res_file, max_pages) 
    bandit_sites = _read_result_file(bandit_res_file, max_pages) 
    sf_sites = _read_sf_result_file(sf_res_file, max_pages)
    ac_sites = _read_ac_result_file(ac_res_file, max_pages)
    bi_sites = _read_ac_result_file(bi_res_file, max_pages) # bipartite and ache results have the same format

    kw_sites = set([s for s in kw_sites if s in kw_relev])
    bl_sites = set([s for s in bl_sites if s in bl_relev])
    rl_sites = set([s for s in rl_sites if s in rl_relev])
    fw_sites = set([s for s in fw_sites if s in fw_relev])
    bandit_sites = set([s for s in bandit_sites if s in bandit_relev])
    sf_sites = set([s for s in sf_sites if s in sf_relev])
    ac_sites = set([s for s in ac_sites if s in ac_relev])
    bi_sites = set([s for s in bi_sites if s in bi_relev])

    # Compute intersection and complement
    sites = set() # union of all results
    sites.update(kw_sites)
    sites.update(bl_sites)
    sites.update(rl_sites)
    sites.update(fw_sites)
    sites.update(bandit_sites)
    sites.update(sf_sites)
    sites.update(ac_sites)
    sites.update(bi_sites)

    print "keyword sites:", len(kw_sites)
    print "backlink sites:", len(bl_sites)
    print "related sites:", len(rl_sites)
    print "forward sites:", len(fw_sites)
    print "bandit sites:", len(bandit_sites)
    print "seedfinder sites:", len(sf_sites)
    print "ache sites:", len(ac_sites)
    print "bipartite sites:", len(bi_sites)
    print "total sites:", len(sites)
    return kw_sites, bl_sites, rl_sites, fw_sites, bandit_sites, sf_sites, ac_sites, bi_sites, sites

def prepare_heatmap_data(kw_files, bl_files, rl_files, fw_files, bandit_files, sf_files, ac_files, bi_files, outfile):
    kw_sites, bl_sites, rl_sites, fw_sites, bandit_sites, sf_sites, ac_sites, bi_sites, sites = read(kw_files, bl_files, rl_files, fw_files, bandit_files, sf_files, ac_files, bi_files)
    n = float(len(sites))
    #methods = ['KEYWORD','BACKWARD','RELATED','FORWARD','BANDIT','SEEDFINDER','ACHE','BIPARTITE']
    methods = ['KEYWORD','BACKWARD','RELATED','FORWARD','SEEDFINDER','ACHE','BIPARTITE']
    method2site = {'KEYWORD':kw_sites,
                'BACKWARD':bl_sites,
                'RELATED':rl_sites,
                'FORWARD':fw_sites,
                'SEEDFINDER':sf_sites,
                'ACHE':ac_sites,
                'BIPARTITE':bi_sites}
    
    out = open(outfile, 'w')
    header = ','.join(methods)
    out.write(header + '\n')
    for m1 in methods:
        line = ''
        for m2 in methods:
            #inter_value = round(len(method2site[m1].intersection(method2site[m2]))*100/float(len(method2site[m1])), 2)
            inter_value = round(len(method2site[m1].intersection(method2site[m2]))*100/float(n), 2)
            line += str(inter_value) + ','
        line = line.strip(',') + '\n'
        out.write(line)
    out.close()

def prepare_data(kw_files, bl_files, rl_files, fw_files, bandit_files, sf_files, ac_files, bi_files, outfile):
    kw_sites, bl_sites, rl_sites, fw_sites, bandit_sites, sf_sites, ac_sites, bi_sites, sites = read(kw_files, bl_files, rl_files, fw_files, bandit_files, sf_files, ac_files, bi_files)
    n = float(len(sites))/100

    exc_kw_percent = round(len(kw_sites - fw_sites - bandit_sites - bl_sites - rl_sites - sf_sites - ac_sites - bi_sites)/n, 2)
    exc_bl_percent = round(len(bl_sites - fw_sites - bandit_sites - kw_sites - rl_sites - sf_sites - ac_sites - bi_sites)/n, 2)
    exc_rl_percent = round(len(rl_sites - fw_sites - bandit_sites - bl_sites - kw_sites - sf_sites - ac_sites - bi_sites)/n, 2)
    exc_fw_percent = round(len(fw_sites - kw_sites - bandit_sites - bl_sites - rl_sites - sf_sites - ac_sites - bi_sites)/n, 2)
    exc_bandit_percent = round(len(bandit_sites - rl_sites - bl_sites - kw_sites - sf_sites - ac_sites - bi_sites - fw_sites)/n, 2)
    exc_sf_percent = round(len(sf_sites - fw_sites - bandit_sites - bl_sites - rl_sites - kw_sites - ac_sites - bi_sites)/n, 2)
    exc_ac_percent = round(len(ac_sites - fw_sites - bandit_sites - bl_sites - rl_sites - sf_sites - kw_sites - bi_sites)/n, 2)
    exc_bi_percent = round(len(bi_sites - fw_sites - bandit_sites - bl_sites - rl_sites - sf_sites - ac_sites - kw_sites)/n, 2)

    kw_percent = round(len(kw_sites)/n, 2)
    bl_percent = round(len(bl_sites)/n, 2)
    rl_percent = round(len(rl_sites)/n, 2)
    fw_percent = round(len(fw_sites)/n, 2)
    bandit_percent = round(len(bandit_sites)/n, 2)
    sf_percent = round(len(sf_sites)/n, 2)
    ac_percent = round(len(ac_sites)/n, 2)
    bi_percent = round(len(bi_sites)/n, 2)
    print kw_percent + bl_percent + rl_percent + sf_percent + ac_percent + bi_percent + bandit_percent + fw_percent

    out = open(outfile, 'w')
    out.write('KEYWORD,BACKWARD,RELATED,FORWARD,BANDIT,SEEDFINDER,ACHE,BIPARTITE\n')
    out.write(str(exc_kw_percent) + ',' + \
              str(exc_bl_percent) + ',' + \
              str(exc_rl_percent) + ',' + \
              str(exc_fw_percent) + ',' + \
              str(exc_bandit_percent) + ',' + \
              str(exc_sf_percent) + ',' + \
              str(exc_ac_percent) + ',' + \
              str(exc_bi_percent) + '\n')

    out.write(str(kw_percent-exc_kw_percent) + ',' + \
              str(bl_percent-exc_bl_percent) + ',' + \
              str(rl_percent-exc_rl_percent) + ',' + \
              str(fw_percent-exc_fw_percent) + ',' + \
              str(bandit_percent-exc_bandit_percent) + ',' + \
              str(sf_percent-exc_sf_percent) + ',' + \
              str(ac_percent-exc_ac_percent) + ',' + \
              str(bi_percent-exc_bi_percent) + '\n')
    """
    out.write('keyword,' + str(exc_kw_percent) + ',' + str(kw_percent-exc_kw_percent) + '\n') # percentage
    out.write('BACKWARD,' + str(exc_bl_percent) + ',' + str(bl_percent-exc_bl_percent) + '\n')
    out.write('related,' + str(exc_rl_percent) + ',' + str(rl_percent-exc_rl_percent) + '\n')
    out.write('seedfinder,' + str(exc_sf_percent) + ',' + str(sf_percent-exc_sf_percent) + '\n')
    out.write('ache,' + str(exc_ac_percent) + ',' + str(ac_percent-exc_ac_percent) + '\n')
    """

    out.close()

def main(domain):
    kw_files, bl_files, rl_files, fw_files, bandit_files, sf_files, ac_files, bi_files, outfile = get_filenames(domain)
    prepare_data(kw_files, bl_files, rl_files, fw_files, bandit_files, sf_files, ac_files, bi_files, outfile)
    #prepare_heatmap_data(kw_files, bl_files, rl_files, fw_files, bandit_files, sf_files, ac_files, bi_files, outfile)


main(sys.argv[1])
