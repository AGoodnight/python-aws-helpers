import sys
import subprocess
import os
import json
import datetime
import argparse

def main():

    parser = argparse.ArgumentParser(description='Some Arguments batch upload items to Dynamo')
    parser.add_argument('-s','--source', type=argparse.FileType('r'), help='Supply a source JSON',required=True)
    parser.add_argument('-t','--table', help='Supply a table in the account',required=True)
    parser.add_argument('-p','--profile', help='Supply a table in the account',required=True)

    _parsedJson = json.load(parser.parse_args().source_arg)

    batchUpdate(_parsedJson,parser.parse_args().table,parser.parse_args().profile)

def batchUpdate(source,table,profile):
    for item in source:
        _new_item = {}

        for node in item:
            _new_item[node] = { "S":str(item[node]) }

        _new_item['created'] = { "S":str(datetime.datetime.now()) }
        _new_item['modified'] = { "S":str(datetime.datetime.now()) }
        _newItem = json.dumps(_new_item)

        print('> Succesfully Uploaded to Table: ',_newItem)

        subprocess.call(['aws', '--profile', profile,'dynamodb', 'put-item','--item',str(_newItem),'--table-name', table])

if __name__ == '__main__':
    main()
