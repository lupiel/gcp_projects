from datetime import datetime
from typing import List, Dict
from google.cloud import bigquery
from google.cloud import storage
from google.cloud.exceptions import NotFound

import pandas as pd
import json, os

PROJECT = os.environ.get("PROJECT", "PROJECT env var not set")
DATASET = os.environ.get("DATASET", "DATASET env var not set")
INBOX_DIR = os.environ.get("INBOX_DIR", "INBOX_DIR env var not set")

def get_archive_ext_table(table_name: str, dataset: str, project: str, bucket: str, directory: str):
    """
        python -c 'from main import get_archive_ext_table; print(get_archive_ext_table("ext_product_dim", "dataset_csv_loader", "natural-nebula-377015", "bucket-csv-loader", "cloud_functions/csv-loader/archive/product_dim"))'
    """
    columns_lst = []
    with open("tables.json", "r") as f:
        for field in json.load(f)[table_name]["columns"]:
            if field["name"] != "load_timestamp":
                columns_lst.append(f"{field['name']} {field['field_type']},")

    columns_ddl = "\n\t".join(columns_lst)

    table_ddl = f"""
CREATE EXTERNAL TABLE `{project}.{dataset}.{table_name}`
(
\t{columns_ddl}
)
OPTIONS(
  skip_leading_rows=1,
  format="CSV",
  uris=["gs://{bucket}/{directory}/*"]
)
;

SELECT *, _FILE_NAME FROM `{project}.{dataset}.{table_name}` LIMIT 1000
;
"""
    return table_ddl

def get_schema(table_name: str) -> List[bigquery.SchemaField]:
    """
        python -c 'from main import get_schema; print(get_schema("product_dim"))'
    """
    schema = []
    with open("tables.json", "r") as f:
        for field in json.load(f)[table_name]["columns"]:
            schema.append(bigquery.SchemaField(name=field["name"], field_type=field["field_type"]))
    return schema


def get_key(table_name: str) -> List[str]:
    """
        python -c 'from main import get_key; print(get_key("product_dim"))'
    """
    with open("tables.json", "r") as f:
        print(table_name)        
        return json.load(f)[table_name]["scope_key"]


def get_gcs_as_dataframe(uri: str):
    """
        python -c 'from main import get_gcs_as_dataframe; print(get_gcs_as_dataframe("gs://bucket-csv-loader/product_dim_1.csv").to_string())'
    """
    df = pd.read_csv(uri)
    return df

def delete_scope_from_bigquery(table_name: str, scope_col: List[str], scope_val: List[str]):
    table_id = f"{PROJECT}.{DATASET}.{table_name}"
    client = bigquery.Client()
    try:
        client.get_table(table_id)
    except NotFound:
        return

    delete_sql = (f"DELETE FROM `{table_id}`\n"
                   "WHERE 1=1")

    where_sql = ""
    for col, val in zip(scope_col, scope_val):
        where_sql = where_sql + "\n  AND " + (f"{col}='{val}'" if isinstance(val, str) else f"{col}={val}")

    delete_sql = delete_sql + where_sql
    print(f"delete_sql:\n{delete_sql}")
    client.query(delete_sql)
    print("Delete completed.")


def gcs_mv(src_bucket: str, src_file: str, dest_bucket: str, dest_file: str):
    client = storage.Client()

    source_bucket = client.get_bucket(src_bucket)
    source_blob = source_bucket.blob(src_file)
    destination_bucket = client.get_bucket(dest_bucket)

    source_bucket.copy_blob(source_blob, destination_bucket, dest_file)
    source_blob.delete()


def mv_archive(bucket_name: str, file_name: str, load_timestamp: datetime):
    """Moves file from INBOX_DIR/TABLE_NAME
    to INBOX_DIR/TABLE_NAME

    python -c 'from datetime import datetime; from main import mv_archive; mv_archive("bucket-csv-loader", "inbox/product_dim/product_dim_1.csv", datetime.now())'
    """
    dest_ts = load_timestamp.strftime("%Y%m%d_%H%M%S_%f")
    
    dest_lst = file_name.split("/")
    dest_lst[-3] = "archive" # instead of inbox
    #dest_lst[-2] is a table_name
    dest_lst[-1] = dest_lst[-1] + "_" + dest_ts # append timestamp
    dest_file = "/".join(dest_lst)

    print("Executing mv", f"gs://{bucket_name}/{file_name} gs://{bucket_name}/{dest_file}")
    gcs_mv(src_bucket=bucket_name, src_file=file_name, dest_bucket=bucket_name, dest_file=dest_file)


def insert_dataframe_to_bigquery(df: pd.DataFrame, table_name: str):
    client = bigquery.Client()

    job_config = bigquery.LoadJobConfig(
        schema=get_schema(table_name),
        write_disposition="WRITE_APPEND"
    )

    table_id = f"{PROJECT}.{DATASET}.{table_name}"

    client.load_table_from_dataframe(
        dataframe=df,
        destination=table_id,
        job_config=job_config,
    )

    print(f"Insert completed. Rows: {df.shape[0]} Table: {table_id}")

def reload_scope(table_name: str, uri: str, load_timestamp: datetime):
    """
        export PROJECT=natural-nebula-377015
        export DATASET=dataset_csv_loader
        gsutil cp -r data/product_dim* gs://bucket-csv-loader/inbox/product_dim/
        python -c 'from main import reload_scope; reload_scope("product_dim", "gs://bucket-csv-loader/inbox/product_dim/product_dim_1.csv")'
        python -c 'from main import reload_scope; reload_scope("product_dim", "gs://bucket-csv-loader/inbox/product_dim/product_dim_2.csv")'
        python -c 'from main import reload_scope; reload_scope("product_dim", "gs://bucket-csv-loader/inbox/product_dim/product_dim_3.csv")'
    """
    df = get_gcs_as_dataframe(uri=uri)
    key_columns = get_key(table_name=table_name)
    key_values = df.loc[0, key_columns].values.tolist()
    
    if len(df[key_columns].drop_duplicates(subset=key_columns)) > 1:
        raise ValueError(f"File key columns have multiple values.")
    
    df = df.assign(load_timestamp=load_timestamp)

    delete_scope_from_bigquery(table_name, scope_col=key_columns, scope_val=key_values)
    insert_dataframe_to_bigquery(df=df, table_name=table_name)

def main(event, context):
    """Triggered by a change to a Cloud Storage bucket.
    Args:
        event (dict): Event payload.
        context (google.cloud.functions.Context): Metadata for the event.

    export PROJECT=natural-nebula-377015
    export DATASET=dataset_csv_loader
    export INBOX_DIR=cloud_functions/csv-loader/inbox
    gsutil cp data/product_dim_1.csv gs://bucket-csv-loader/cloud_functions/csv-loader/inbox/product_dim/product_dim_1.csv
    python -c 'from main import main; main({"bucket": "bucket-csv-loader", "name": "cloud_functions/csv-loader/inbox/product_dim/product_dim_1.csv"}, {})'
    """
    LOAD_TIMESTAMP = datetime.now()
    BUCKET_NAME = event["bucket"]
    FILE_NAME = event["name"]

    if not FILE_NAME.startswith(INBOX_DIR):
        print(f"File {FILE_NAME} not tracked.")
        return

    # cloud_functions/csv-loader-v2/inbox/TABLE_NAME/data.csv
    TABLE_NAME = FILE_NAME[len(INBOX_DIR)+1:].split("/")[0]
    URI = f"gs://{BUCKET_NAME}/{FILE_NAME}"
    print("TABLE_NAME:", TABLE_NAME)
    print("URI:", URI)
    reload_scope(table_name=TABLE_NAME, uri=URI, load_timestamp=LOAD_TIMESTAMP)
    mv_archive(bucket_name=BUCKET_NAME, file_name=FILE_NAME, load_timestamp=LOAD_TIMESTAMP)
