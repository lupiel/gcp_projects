Use this script to copy tables between 2 projects whenever not possible to copy with `bq cp` or `CREATE TABLE AS SELECT...`

- Bucket name is used to store csv versions of tables.
- Not tested on high volumes of data.

### Run instruction
1. Fill in parameters in `copy_tables_bq_to_bq.sh` before running the script
```
SOURCE_PROJECT="src-project-name"
SOURCE_DATASET="f_dataset"
DESTINATION_PROJECT="dest-project_name"
DESTINATION_DATASET="f_dataset"
BUCKET="bucket-name/hackathon"
```
2. List tables to be moved in `tables.txt`
3. Run using command
`bash copy_bq_to_bq.sh`
