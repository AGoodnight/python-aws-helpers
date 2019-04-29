import sys
import subprocess
import os
import json
import datetime
import argparse

from pydash import find


def main():

    parser = argparse.ArgumentParser(description='Some Arguments to merge the json')
    parser.add_argument('-t','--target',metavar='Target Json', type=argparse.FileType('r'), help='Supply a target JSON',required=True)
    parser.add_argument('-s','--source',metavar='Source Json', type=argparse.FileType('r'), help='Supply a source JSON',required=True)
    parser.add_argument('-f','--output',metavar='Resulting File Name', help='Give your output a name', required=True)
    parser.add_argument('-e','--exclude',metavar='Key Pairs to Strip', default=[], nargs='+', help='Supply a list of keys to strip from the target')
    parser.add_argument('-k','--catch-primary-key',metavar='Reassign Source Primary Key',dest='catch_primary_arg',help="If your source target json has a primary key that differs from 'id' but you want to assign it's value to id, provide the key name")

    mergeJsons([parser.parse_args().target,parser.parse_args().source],parser.parse_args().exclude)


def mergeJsons(files,exclude=[],catch_primary_key=None):

    _json1 = json.load(files[0])
    _json2 = json.load(files[1])
    _merged = []
    _exclude = exclude

    for obj in _json1:

        _obj = obj.copy()

        if catch_primary_key is not None:
            _obj['id'] = _obj.pop(catch_primary_key)
            print(_obj)

        _a = {k:v for k,v in _obj.items()}
        _b = find(_json2, {'id': _a['id']})

        if _b is not None:
            _a.update(_b)
        else:
            _a.update(addMissingFields(_a,_json2));

        # Remove excluded key:value pairs
        if _exclude is not None:
            _aclone = _a.copy()
            for key in _exclude:
                if key in _aclone:
                    del _a[key]

        # Replace Empty Strings ( for dynamo )
        _a = {k:replaceEmptyString(v) for k,v in _a.items()}
        _merged.append(_a)

    return _merged

def writeOutput(mergedJson,filename = 'output.json'):
    _output = open(filename,"w")
    json.dump(mergedJson,_output)
    _output.close()


def replaceEmptyString(value):
    if value is None:
        return "None"
    if len(value) < 1:
        return "None"
    else:
        return value

def addMissingFields(target,source):
    _target = {}
    for item in source[0]:
        if item not in target:
            _target[item] = "None"
    return _target

if __name__ == '__main__':
    main()
