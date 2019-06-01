'''
This class manages past search results.
This helps to avoid sending the same queries to Search APIs
'''
import json
import traceback
import os

class Cache:
    def __init__(self, data_file):
        self.data_file = data_file
        self.data = self._load_data()

    def contains(self, key):
        if key in self.data:
            return True
        else:
            return False

    def get(self, key):
        if self.contains(key):
            return self.data[key]
        else:
            return None

    def keys(self):
        return self.data.keys()

    def add(self, key, data):
        self.data[key] = data
        try:
            with open(self.data_file, "a+") as fd:
                json_obj = {'key':key, 'value':data}
                json.dump(json_obj, fd)
                fd.write("\n")
        except:
            traceback.print_exc()

    def length(self):
        return len(self.data)

    def _load_data(self):
        data = {}
        if not os.path.exists(self.data_file):
            return data

        with open(self.data_file) as lines:
            for line in lines:
                obj = json.loads(line)
                key = obj['key']
                value = obj['value']    
                data[key] = value 

        return data

def test():
    cache = Cache("cache_test_file.txt")
    assert(cache.contains("key1")==False)
    cache.add("key1", "value1")
    cache.add("key2", "value2")
    assert(cache.contains("key1")==True)
    assert(cache.get("key1")=="value1")

if __name__=="__main__":
    test()
