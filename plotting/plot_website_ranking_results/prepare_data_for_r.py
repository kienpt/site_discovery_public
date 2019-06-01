import argparse
import sys

def get_precision_values(input_file):
    prec_values = []
    all_precs = []
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
            if "RESULTS_PREC" in line:
                tokens = line.strip().split(',')
                all_precs.append([float(t) for t in tokens[1:]])
    print len(methods), len(prec_values), len(means), len(medians), len(all_precs)
    return methods, prec_values, means, medians, all_precs

def naming(methods):
    newnames = []
    for m in methods:
        if m=='jaccard':
            newnames.append('JACCARD')
        if m=='cosine':
            newnames.append('COSINE')
        if m=='stacking':
            newnames.append('COMBINATION')
        if m=='stacking_rrf':
            newnames.append('STACK-RRF')
        if m=='oneclass':
            newnames.append('ONECLASS')
        if m=='bayesian_tfidf':
            newnames.append('BAYESIANSETS')
        if m=='bayesian_bin':
            newnames.append('BS-BIN')
        if m=='pu_learning':
            newnames.append('PULEARNING')
        if m=='classifier':
            newnames.append('TWOCLASS')
    return newnames

def _filter(methods, precs, means, medians, all_precs):
    newmethods = []
    newprecs = []
    newmeans = []
    newmedians = []
    newall_precs = []
    for i in xrange(len(methods)):
        if (methods[i]!='STACK-RRF') and (methods[i]!='BS-BIN'):
            newmethods.append(methods[i])
            newprecs.append(precs[i]) 
            newmeans.append(means[i])
            newmedians.append(medians[i])
            newall_precs.append(all_precs[i])

    return newmethods, newprecs, newmeans, newmedians, newall_precs

def prepare_data(infile, domain, outputdir):
    methods, precs, means, medians, all_precs = get_precision_values(infile)
    # Filter some results
    methods = naming(methods)
    methods, precs, means, medians, all_precs = _filter(methods, precs, means, medians, all_precs)

    # P@K
    fname = outputdir + "/prec_" + domain + ".csv"
    with open(fname, 'w') as f:
        f.write(','.join(methods) + '\n')
        f.write(','.join([str(p) for p in precs]) + '\n')
        k = (len(all_precs[0])-1)/2
        diff_precs = [all_precs[i][k]-precs[i] for i in xrange(len(precs))]
        f.write(','.join([str(p) for p in diff_precs]) + '\n')

    # Variable K
    fname = outputdir + "/k_" + domain + ".csv"
    with open(fname, 'w') as f:
        for i in xrange(len(methods)):
            if methods[i]=='COMBINATION':
                stacking_precs = all_precs[i]
        interval = len(stacking_precs)/10+1
        k = interval
        line1 = "1"
        line2 = str(stacking_precs[0])
        while k<=len(stacking_precs):
            if k>1: 
                line1 += ',' + str(k) 
                line2 += ',' + str(stacking_precs[k-1]) 
            k += interval
        if (k-len(stacking_precs))<interval:
            line1 += ',' + str(len(stacking_precs))
            line2 += ',' + str(stacking_precs[-1])
        f.write(line1 + '\n')
        f.write(line2 + '\n')


    # mean@K
    fname = outputdir + "/mean_" + domain + ".csv"
    with open(fname, 'w') as f:
        f.write(','.join(methods) + '\n')
        f.write(','.join([str(p) for p in means]) + '\n')

    # P@K
    fname = outputdir + "/median_" + domain + ".csv"
    with open(fname, 'w') as f:
        f.write(','.join(methods) + '\n')
        f.write(','.join([str(p) for p in medians]) + '\n')

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
