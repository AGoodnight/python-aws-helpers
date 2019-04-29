import sys
import subprocess
import os
import json
import datetime
import argparse

from pydash import find

from mergeJson import mergeJsons, writeOutput
from batchUpdateDynamoTable_fromJson import batchUpdate

def main():
    parser = argparse.ArgumentParser(description='Some Arguments to merge the json')

    parser.add_argument('files',metavar='Files to Merge', nargs='+', type=argparse.FileType('r'), help='Supply a target JSON')
    parser.add_argument('-t','--table',help='Supply a table in the account',required=True)
    parser.add_argument('-p','--profile', help='Select a AWS CLI profile to use',required=True)

    parser.add_argument('-e','--exclude',metavar='Key Pairs to Strip',default=[], nargs='+', help='Supply a list of keys to strip from the target')
    parser.add_argument('-k','--catch-primary-key',metavar='Reassign Source Primary Key',dest='catch_primary_key',help="If your source target json has a primary key that differs from 'id' but you want to assign it's value to id, provide the key name")

    jsons = parser.parse_args().files
    table_name = parser.parse_args().table
    cli_profile = parser.parse_args().profile
    exclude = parser.parse_args().exclude
    primary_key_to_remap = parser.parse_args().catch_primary_key

    _json = mergeJsons(jsons,exclude,primary_key_to_remap)
    batchUpdate(_json,table_name,cli_profile)

if __name__ == '__main__':
    main()
