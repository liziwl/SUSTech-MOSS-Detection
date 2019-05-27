# SUSTech-MOSS-Detection

## Modified mosspy
Forked code from https://github.com/soachishti/moss.py

My code is also in https://github.com/liziwl/moss.py

## Add your moss id in `moss_id.py`

like
```python
my_moss_id = 12345678
```

## Moss Detection Procedure

1. `extract_pack.py`
    
    recursively unpack compressed file which are downloaded from SAKAI
    
2. `moss_checker.py`
    
    In main function
    - set detect language
    - set file extension to check
    - set proxy if needed
    - set Base Files path
    - set student submission Files path

3. `result_html2csv.py`
    
    Already used in `moss_checker.py`, parse html report to csv report and remove duplicate item for the same student ID.