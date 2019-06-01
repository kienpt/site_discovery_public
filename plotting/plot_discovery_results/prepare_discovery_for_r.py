import sys
import argparse

def count(fname):
    pos, neg = 0, 0
    with open(fname) as lines:
        for line in lines:
            values = line.strip().split(',')
            if values[1]=='1':
                pos += 1
            else:
                neg += 1
    return pos, neg

def prepare(domain, outputdir):
    related_file = '../../data/discovery/' + domain + '_related_classification.csv'
    backlink_file = '../../data/discovery/' + domain + '_backlink_classification.csv'
    kw_file = '../../data/discovery/' + domain + '_keyword_classification.csv'
    seedfinder_file = '../../data/discovery/seedfinder/' + domain + '_classification.csv'

    related_pos, related_neg = count(related_file)
    related_ratio = round(related_pos*100/float(related_pos + related_neg), 2)
    print "Related: ", related_pos, related_neg, related_ratio 
    bl_pos, bl_neg = count(backlink_file)
    bl_ratio =  round(bl_pos*100/float(bl_pos + bl_neg), 2)
    print "Backlink: ", bl_pos, bl_neg, bl_ratio 
    kw_pos, kw_neg = count(kw_file)
    kw_ratio =  round(kw_pos*100/float(kw_pos + kw_neg), 2)
    print "Keyword: ", kw_pos, kw_neg, kw_ratio 
    sf_pos, sf_neg = count(seedfinder_file)
    sf_ratio = round(sf_pos*100/float(sf_pos + sf_neg), 2)
    print "Seedfinder: ", sf_pos, sf_neg, sf_ratio 

    outfile = outputdir + '/' + domain + '_harvestrate.csv'
    with open(outfile, 'w') as f:
        f.write("Related Search,Backlink Search,Keyword Search,Seedfinder\n")
        f.write(str(related_ratio) + ',' + str(bl_ratio) + ',' + str(kw_ratio) + ',' + str(sf_ratio) + '\n')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--outputdir", help="output directory", type=str)
    parser.add_argument("-d", "--domain", help="domain name", type=str)
    args = parser.parse_args()

    prepare(args.domain, args.outputdir)

if __name__=='__main__':
    main()
