import os
import sys
import json
import argparse
import traceback
sys.path.append("extraction")
from urlutility import URLUtility
from link_extractor import Link_Extractor


def sample(datadir, outputfile):
    link_extractor = Link_Extractor()
    files = os.listdir(datadir)
    out = open(outputfile, 'w')
    for f in files:
        if 'json' not in f:
            print 'Skip ', f
            continue
        filepath = datadir + '/' + f
        with open(filepath) as lines:
            for line in lines:  
                try:
                    jsobj = json.loads(line)
                    jsobj = jsobj['value']
                    url, html = jsobj['url'], jsobj['html']
                    insite_urls = list(set(link_extractor.extract_insite_links(url, html)))
                    for u in insite_urls:
                        out.write(u + '\n')
                except:
                    traceback.print_exc()
    out.close()

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--datadir", help="path to directory containing crawled data", type=str)
    parser.add_argument("-o", "--outputfile", help="file to store sampled urls", type=str)
    args = parser.parse_args()
    parser.print_help()

    sample(args.datadir, args.outputfile)
