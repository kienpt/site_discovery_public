"""
Copy all key value pairs from a cache file to another cache file without duplication
"""
import sys
import json

def copycache(from_file, to_file):
    keys = set()
    with open(to_file) as lines:
        for line in lines:
            js = json.loads(line)
            key = js['key']
            keys.add(key)

    writer = open(to_file, 'a+')
    with open(from_file) as lines:
        for line in lines:
            js = json.loads(line)
            key = js['key']
            if key not in keys:
                writer.write(line)
    writer.close()

def copycache_emptyfiltered(from_file, to_file):
    """
    Only copy non-empty (key, value) pairs
    """
    keys = set()
    with open(to_file) as lines:
        for line in lines:
            js = json.loads(line)
            key = js['key']
            keys.add(key)

    writer = open(to_file, 'a+')
    with open(from_file) as lines:
        for line in lines:
            js = json.loads(line)
            key = js['key']
            if key not in keys:
                if len(js['value'])>2:
                    writer.write(line)
    writer.close()

def main():
    from_file = sys.argv[1]
    to_file = sys.argv[2]
    #copycache(from_file, to_file)
    copycache_emptyfiltered(from_file, to_file)

main()
