import argparse
import sys

def get_precision_values(input_file):
    seednumbs = []
    precs = []
    with open(input_file) as lines:
        for line in lines:
            if "RESULTS_SEEDNUMB" in line:
                values = line.strip().split()
                seednumbs.append(str(values[1]))
            if "RESULTS_AGGREGATION" in line:
                tokens = line.strip().split(',')
                mean, median, prec = float(tokens[2]), float(tokens[3]), float(tokens[4])
                precs.append(prec)

    seednumbs.reverse()
    precs.reverse()
    return seednumbs, precs 

def prepare_data(infile, domain, outputdir):
    seednumbs, precs = get_precision_values(infile)

    # P@K
    fname = outputdir + "/prec_" + domain + ".csv"
    with open(fname, 'w') as f:
        f.write(','.join(seednumbs) + '\n')
        f.write(','.join([str(p) for p in precs]) + '\n')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--inputfile", help="input file with data to plot", type=str)
    parser.add_argument("-o", "--outputdir", help="output directory", type=str)
    #parser.add_argument("-t", "--plottype", help="plot type: ['prec', 'median', 'mean']", type=str)
    
    parser.add_argument("-d", "--domain", help="domain name", type=str)
    args = parser.parse_args()

    prepare_data(args.inputfile, args.domain, args.outputdir)

if __name__=='__main__':
    main()
