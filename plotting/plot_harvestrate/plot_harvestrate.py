
# coding: utf-8

# In[5]:

import sys
import numpy as np
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
MARKERS = ['+', 'o', "*", "p", "s", "x", "h", "d", "<", ">", 'H', 'D', 'd', 'P', 'X']
plt.rc('text', usetex=True)
plt.rc('font', family='serif')

def _read_data(data_file):
    names = []
    rows = []
    with open(data_file) as lines:
        for line in lines:
            values = line.strip().split(',')
            names.append(values[0])
            rows.append(values[1:50000]) 
    return names, rows

def plot_harvestrate_page(data_file, outfile):
    plt.clf()
    names, rows = _read_data(data_file)
    global MARKERS
    plt.plot(rows[1], marker=MARKERS[0], markevery=5000)
    plt.plot(rows[2], marker=MARKERS[1], markevery=5000)
    plt.plot(rows[3], marker=MARKERS[2], markevery=5000)
    plt.plot(rows[4], marker=MARKERS[3], markevery=5000)
    plt.plot(rows[5], marker=MARKERS[4], markevery=5000)
    plt.plot(rows[6], marker=MARKERS[5], markevery=5000)
    plt.plot(rows[7], marker=MARKERS[6], markevery=5000)
    plt.plot(rows[8], marker=MARKERS[7], markevery=5000)
    plt.legend(names[1:9], loc=2, fontsize=11)
    plt.xlabel('Number of retrieved pages', fontsize=14)
    plt.ylabel('Number of relevant web pages', fontsize=14)
    plt.savefig(outfile)

def rename(a):
    """
    method_site -> method
    """
    return [s.split('_')[0] for s in a]

def plot_harvestrate_site(data_file, outfile, title=""):  
    plt.clf()
    names, rows = _read_data(data_file)
    global MARKERS
    plt.plot(rows[9], marker=MARKERS[0], markevery=5000)
    plt.plot(rows[10], marker=MARKERS[1], markevery=5000)
    plt.plot(rows[11], marker=MARKERS[2], markevery=5000)
    plt.plot(rows[12], marker=MARKERS[3], markevery=5000)
    plt.plot(rows[13], marker=MARKERS[4], markevery=5000)
    plt.plot(rows[14], marker=MARKERS[5], markevery=5000)
    plt.plot(rows[15], marker=MARKERS[6], markevery=5000)
    plt.plot(rows[16], marker=MARKERS[7], markevery=5000)
    #plt.legend(names[6:], fontsize=11, bbox_to_anchor=(1.05, 1), loc=2)
    plt.legend(rename(names[9:]), fontsize=11, loc=2)
    plt.xlabel('Number of retrieved pages', fontsize=14)
    plt.ylabel('Number of relevant websites', fontsize=14)
    plt.suptitle(title, fontsize=16)
    plt.savefig(outfile)

def main():
    data_file = 'ads.csv'
    domain = data_file.split(".")[0]
    plot_harvestrate_page(data_file, "figures/rate_page_" + domain + ".pdf")
    plot_harvestrate_site(data_file, "figures/rate_site_" + domain + ".pdf")

    # plot_harvestrate_site(data_file, "figures_png/rate_site_" + domain + ".png", "Weapon Marketplace Domain")

    data_file = 'forum.csv'
    domain = data_file.split(".")[0]
    plot_harvestrate_page(data_file, "figures/rate_page_" + domain + ".pdf")
    plot_harvestrate_site(data_file, "figures/rate_site_" + domain + ".pdf")

    # plot_harvestrate_site(data_file, "figures_png/rate_site_" + domain + ".png", "Weapon Forum Domain")

    data_file = 'ht.csv'
    domain = data_file.split(".")[0]
    plot_harvestrate_page(data_file, "figures/rate_page_" + domain + ".pdf")
    plot_harvestrate_site(data_file, "figures/rate_site_" + domain + ".pdf")

    # plot_harvestrate_site(data_file, "figures_png/rate_site_" + domain + ".png", "Human Trafficking (Escort) Domain")

main()
