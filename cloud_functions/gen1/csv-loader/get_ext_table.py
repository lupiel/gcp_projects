"""
    python get_archive_ext_table.py
"""
import json

def get_archive_ext_table(table_name: str, dataset: str, project: str, bucket: str, directory: str):
    columns_lst = []
    with open("tables.json", "r") as f:
        for field in json.load(f)[table_name]["columns"]:
            if field["name"] != "load_timestamp":
                field_type = field['field_type'].replace("FLOAT", "FLOAT64")
                columns_lst.append(f"{field['name']} {field_type},")

    columns_ddl = "\n\t".join(columns_lst)

    table_ddl = f"""
DROP TABLE IF EXISTS `{project}.{dataset}.ext_{table_name}`
;

CREATE EXTERNAL TABLE `{project}.{dataset}.ext_{table_name}`
(
\t{columns_ddl}
)
OPTIONS(
  skip_leading_rows=1,
  format="CSV",
  uris=["gs://{bucket}/{directory}/*"]
)
;

SELECT *, _FILE_NAME FROM `{project}.{dataset}.ext_{table_name}` LIMIT 1000
;
"""
    print(table_ddl)

get_archive_ext_table("product_dim", "dataset_csv_loader", "natural-nebula-377015", "bucket-csv-loader", "cloud_functions/csv-loader/archive/product_dim")