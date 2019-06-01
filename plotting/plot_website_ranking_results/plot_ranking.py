import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import sys
import argparse
import numpy as np
import time

def plot_ranking_evaluation_linechart(score_file):
    '''
    Plot the ranking results using line chart
    '''
    mpl.rcParams['xtick.labelsize'] = 17
    mpl.rcParams['ytick.labelsize'] = 17
    #all_markers = ['+', 'o', "*", "s", "x", "h", "d", "<", ">"]
    ranks = []
    methods = []
    ids = []
    with open(score_file) as lines:
        for line in lines:
            values = line.strip().split(",")
            if values[1]=="random":
                continue
            methods.append(values[1])
            ranklist = [float(c) for c in values[2:]]
            ranks.append(ranklist)
            ids.append([i for i in xrange(len(ranklist))])

    plt.xlabel('ID', fontsize=17)
    plt.ylabel('Ranking Score', fontsize=17)
    #plt.ylim(ymin=0)
    for i, ranklist in enumerate(ranks):
        print ranklist
        #plt.plot(ids[i], ranklist, marker=all_markers[i])
        plt.plot(ids[i], ranklist)
    #plt.legend(names, loc='upper center', bbox_to_anchor=(0.5, 1.1), ncol=4, fancybox=True)
    leg = plt.legend(methods, loc='upper right', ncol=3, fancybox=True, fontsize=12)
    #leg.get_frame().set_alpha(0.1)
    #plt.xticks(ids)
    #plt.tight_layout()
    outfile = score_file.split("/")[-1].split(".")[0] 
    plt.savefig("plotting/ranking_comparision/" + outfile)
 
def plot_ranking_evaluation_barchart(score_file):
    """
    Plot the ranking results using bar chart
    """
    data = pd.read_csv(score_file)

def plot_site_representation_comparision(score_dir, domain):
    def load_data(score_file):
        print score_file
        data = pd.read_csv(score_file, header=None)
        methods = data[1]
        data = data.iloc[:, 2:] # 2 is the position of the rank of the first url 
        mean = data.mean(axis=1).tolist()   
        std = data.std(axis=1).tolist()
        return mean, std, methods

    body, body_std, methods = load_data(score_dir + "/" + domain + "_body.csv")
    meta, meta_std, methods = load_data(score_dir + "/" + domain + "_meta.csv")
    #title, title_std, methods = load_data(score_dir + "/" + domain + "_title.csv")

    x_pos = np.arange(len(body)) # the x positions of the 'body' bar
    width = 0.35 # width of the bars

    fig, ax = plt.subplots()
    bar_body = ax.bar(x_pos, body, width/2, color='r', yerr=body_std)
    bar_meta = ax.bar(x_pos + 0.5*width, meta, width/2, color='y', yerr=meta_std)
    #bar_title = ax.bar(x_pos + width, title, width/2, color='b', yerr=title_std)

    ax.set_ylabel('Rank')
    ax.set_title('Ranks by different site representations')
    ax.set_xticks(x_pos + 0.5*width)
    methods = [name.replace("bayesian", "bayes") for name in methods]
    ax.set_xticklabels(methods)
    plt.gca().set_ylim(bottom=0)
    if domain == "atf_ads":
        plt.ylim((0, 600)) # this range only applies for atf_ads domain
    leg = plt.legend(["body", "meta"], loc="upper center", ncol=3, fancybox=True, fontsize=12)
    output_file = "plotting/representation_comparision/" + domain + "_body_meta.png"
    print "output: ", output_file
    plt.savefig(output_file)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--chart", help="line or bar (line chart or bar chart)", type=str)
    parser.add_argument("-s", "--scorefile", help="score file", type=str)
    parser.add_argument("-dir", "--scoredir", help="score directory", type=str)
    parser.add_argument("-dom", "--domain", help="ads/market/forum", type=str)
    args = parser.parse_args()

    if args.chart=='line':
        #plot_ranking_evaluation_barchart()
        plot_ranking_evaluation_linechart(args.scorefile)
    elif args.chart=='bar':
        plot_site_representation_comparision(args.scoredir, args.domain)

if __name__=="__main__":
    main()
