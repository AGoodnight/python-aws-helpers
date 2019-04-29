# Utility Scripts

## Merge jsons and Batch upload to DynamoDB Table

You need AWS CLI and a profile. The script assumes the target table is empty, 'updating' has not been tested.

If in Windows Powershell prepare your CSV files by converting them to JSON
```
import-csv "SampleInput.csv" | ConvertTo-Json -Compress | Add-Content -Path "output.json"
```

Once you have your JSONS, you will use the following script to perform the merge and upload.

```
py updateDashboardTable.py
```

### Arguments
The script takes some arguments.

1. Files <em>Required</em>
<br/>First include your files. The first file will be the base of the merge, so the preceding jsons are merged INTO the first file.
<b><em>Currently only 2 json files can be merged</em></b>
```
py updateDashboardTable.py file1.json file2.json
```

2. Tablename and AWS Profile <em>Required</em>
<br/>Second you will need to provide a table name and you profile for aws cli
```
-t "tableName" -p "profileName"
```

3. Exclude Key Pairs <em>Optional</em>
<br/>
Third you can specify which key pairs you want stripped from the final input
```
-e "key" "key2" "key3"
```

4. Remap Primary Keys <em>Optional</em> <br/>Finally the script assumes 'id' is the primary key of the table you are uploading the merged json to. If for some reason your preceding files have a different primary key you can provide that and it will remap the value to 'id'
```
-k "primarykey"
```


All together your command looks like:
```
py updateDashboardTable.py file1.json file2.json -t "tableName" -p "profileName" -e "key" "key2" "key3" -k "primarykey"
```
