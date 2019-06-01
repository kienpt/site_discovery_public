import matplotlib.pyplot as plt
import argparse
import numpy as np

def get_precision_values(input_file):
    prec_values = []
    means = []
    medians = []
    methods = []
    with open(input_file) as lines:
        for line in lines:
            if "RESULTS_AGGREGATION" in line:
                tokens = line.strip().split(',')
                methods.append(tokens[1])
                mean, median, prec = float(tokens[2]), float(tokens[3]), float(tokens[4])
                prec_values.append(prec)
                means.append(mean)
                medians.append(median)

    return methods, prec_values, means, medians

def plot_precision_at_k(input_file, output_file, domain):
    methods, values, means, medians = get_precision_values(input_file)

    y_pos = np.arange(len(values)) # the y positions 
    dist = 2.0
    y_pos = [y/dist for y in y_pos]
    heights = [0.3]*len(values)

    fig, ax = plt.subplots()
    ax.barh(y_pos, values, heights, align='center', ecolor='black', color="#2b83ba")

    ax.set_xlabel('Precision at k')
    ax.set_title(domain)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(methods)
    for i, v in enumerate(values):
        ax.text(v+0.02, i/dist-0.05, str(v), color='black', fontsize=10)
    plt.xlim(0, 1)
    plt.tight_layout()
    plt.savefig(output_file)
    
def plot_median(input_file, output_file, domain):
    methods, values, means, medians = get_precision_values(input_file)

    y_pos = np.arange(len(values)) # the y positions 
    dist = 2.0
    y_pos = [y/dist for y in y_pos]
    heights = [0.3]*len(values)

    fig, ax = plt.subplots()
    ax.barh(y_pos, medians, heights, align='center', ecolor='black', color="#2b83ba")

    ax.set_xlabel('Median')
    ax.set_title(domain)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(methods)
    for i, v in enumerate(medians):
        ax.text(v+0.02, i/dist-0.05, str(v), color='black', fontsize=10)
    plt.xlim(0, max(medians)+10)
    plt.tight_layout()
    plt.savefig(output_file)

def plot_mean(input_file, output_file, domain):
    methods, values, means, medians = get_precision_values(input_file)

    y_pos = np.arange(len(values)) # the y positions 
    dist = 2.0
    y_pos = [y/dist for y in y_pos]
    heights = [0.3]*len(values)

    fig, ax = plt.subplots()
    ax.barh(y_pos, means, heights, align='center', ecolor='black', color="#2b83ba")

    ax.set_xlabel('Mean')
    ax.set_title(domain)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(methods)
    for i, v in enumerate(means):
        ax.text(v+0.02, i/dist-0.05, str(v), color='black', fontsize=10)
    plt.xlim(0, max(means)+10)
    plt.tight_layout()
    plt.savefig(output_file)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--inputfile", help="input file with data to plot", type=str)
    parser.add_argument("-o", "--outputfile", help="plot file", type=str)
    parser.add_argument("-t", "--plottype", help="plot type: ['prec', 'median', 'mean']", type=str)
    
    parser.add_argument("-d", "--domain", help="domain name", type=str)
    args = parser.parse_args()

    if args.plottype=='prec':
        plot_precision_at_k(args.inputfile, args.outputfile, args.domain)
    elif args.plottype=='median':
        plot_median(args.inputfile, args.outputfile, args.domain)
    elif args.plottype=='mean':
        plot_mean(args.inputfile, args.outputfile, args.domain)
    else:
        print 'Wrong arg'

if __name__=='__main__':
    main()
