#!/bin/bash

# fill in below parameters
SOURCE_PROJECT="src-project-name"
SOURCE_DATASET="f_dataset"
DESTINATION_PROJECT="dest-project_name"
DESTINATION_DATASET="f_dataset"
BUCKET="bucket-name/hackathon"

# List of table names to copy
TABLES_FILE="tables.txt"
TABLE_NAMES=($(cat ${TABLES_FILE}))
# TABLE_NAMES=("ACE_historical_subbrand_calc_ACE_JP")

for TABLE_NAME in "${TABLE_NAMES[@]}"
do
  # Set the location for the export files in Cloud Storage
  EXPORT_PATH="gs://${BUCKET}/${TABLE_NAME}.csv"

  echo "${EXPORT_PATH}"

  # Export BigQuery table to Cloud Storage in the source project
  bq extract --project_id=${SOURCE_PROJECT} --destination_format=CSV \
      ${SOURCE_PROJECT}:${SOURCE_DATASET}.${TABLE_NAME} \
      ${EXPORT_PATH}

  # Auto-generate schema based on the source table
  SCHEMA=$(bq show --project_id=${SOURCE_PROJECT} --format=prettyjson ${SOURCE_PROJECT}:${SOURCE_DATASET}.${TABLE_NAME} | jq -c '.schema.fields')

  # Load the exported data into a new BigQuery table in the destination project
  echo ${SCHEMA} > schema.json
  bq load --project_id=${DESTINATION_PROJECT} --source_format=CSV \
      --skip_leading_rows=1 \
      ${DESTINATION_PROJECT}:${DESTINATION_DATASET}.${TABLE_NAME} \
      ${EXPORT_PATH} \
      schema.json

  # Clean up: Optionally, delete the exported files in Cloud Storage
  # gsutil -m rm -r ${EXPORT_PATH}

  # Remove the temporary schema file
  # rm schema.json

  echo "Table ${TABLE_NAME} copied from ${SOURCE_PROJECT}:${SOURCE_DATASET} to ${DESTINATION_PROJECT}:${DESTINATION_DATASET}"
done
