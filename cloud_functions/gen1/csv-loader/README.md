This cloud functions code is picking up csv file when uploaded to a $BUCKET and loads it into a BigQuery table. Tables and scope keys are defined in `tables.json`. Function will delete the scope before insert. 

```
BUCKET=bucket-csv-loader
REGION=us-central1
DATASET=dataset_csv_loader
PROJECT=natural-nebula-377015
FUNCTION_NAME=csv-loader

cd cloud_functions/gen1/csv-loader
```

## Environment Preparation
```
gcloud auth login
gcloud config set project $PROJECT

gcloud storage buckets create gs://$BUCKET
bq mk $DATASET
```


## Deployment

```

# first deployment
gcloud functions deploy $FUNCTION_NAME --env-vars-file .env.yaml --runtime python311 --trigger-bucket gs://$BUCKET --entry-point main --memory 512MB
# re-deployment
gcloud functions deploy $FUNCTION_NAME --env-vars-file .env.yaml

```

## Testing
```
gcloud functions describe $FUNCTION_NAME
...
```

```
gsutil cp data/product_dim_1.csv gs://$BUCKET/rand-dir/
...wait
gcloud beta functions logs read $FUNCTION_NAME --limit=10

............................................................
LOG: File rand-dir/product_dim_1.csv not tracked.
............................................................
```

```
gsutil cp data/product_dim_1.csv gs://$BUCKET/cloud_functions/csv-loader/inbox/product_dim/
...wait
gcloud beta functions logs read $FUNCTION_NAME --limit=20

............................................................
LOG: Function execution took 5 ms, finished with status: 'ok'
LOG: File cloud_functions/csv-loader/archive/product_dim/product_dim_1.csv_20230314_135042_484152 not tracked.
LOG: Function execution started

LOG: Function execution took 3502 ms, finished with status: 'ok'
LOG: Executing mv gs://bucket-csv-loader/cloud_functions/csv-loader/inbox/product_dim/product_dim_1.csv gs://bucket-csv-loader/cloud_functions/csv-loader/archive/product_dim/product_dim_1.csv_20230314_135042_484152
LOG: Insert completed. Rows: 2 Table: natural-nebula-377015.dataset_csv_loader.product_dim
LOG: Function execution started
............................................................


bq query --nouse_legacy_sql 'SELECT * FROM `natural-nebula-377015.dataset_csv_loader.product_dim`'
+------+------+------+---------------------+
| col1 | col2 | col3 |   load_timestamp    |
+------+------+------+---------------------+
| abc  |    1 |  2.0 | 2023-03-14 13:50:42 |
| abc  |    1 |  4.2 | 2023-03-14 13:50:42 |
+------+------+------+---------------------+

gsutil ls -r gs://$BUCKET/cloud_functions/csv-loader/**
gs://bucket-csv-loader/cloud_functions/csv-loader/archive/product_dim/product_dim_1.csv_20230314_135042_484152
```


```
gsutil cp data/product_dim_2.csv gs://$BUCKET/cloud_functions/csv-loader/inbox/product_dim/
...wait
gcloud beta functions logs read $FUNCTION_NAME --limit=20

............................................................
LOG: Function execution started
LOG: File cloud_functions/csv-loader/archive/product_dim/product_dim_2.csv_20230314_135042_484152 not tracked.
LOG: Function execution took 6 ms, finished with status: 'ok'

LOG: Function execution started
LOG: delete_sql:
LOG: DELETE FROM `natural-nebula-377015.dataset_csv_loader.product_dim`
LOG: WHERE 1=1
LOG:   AND col1='d'
LOG:   AND col2=2
LOG: Delete completed.
LOG: Insert completed. Rows: 2 Table: natural-nebula-377015.dataset_csv_loader.product_dim
LOG: Executing mv gs://bucket-csv-loader/cloud_functions/csv-loader/inbox/product_dim/product_dim_2.csv gs://bucket-csv-loader/cloud_functions/csv-loader/archive/product_dim/product_dim_2.csv_20230314_135042_484152
LOG: Function execution took 2997 ms, finished with status: 'ok'
............................................................


bq query --nouse_legacy_sql 'SELECT * FROM `natural-nebula-377015.dataset_csv_loader.product_dim`'
+------+------+------+---------------------+
| col1 | col2 | col3 |   load_timestamp    |
+------+------+------+---------------------+
| abc  |    1 |  2.0 | 2023-03-14 13:50:42 |
| abc  |    1 |  4.2 | 2023-03-14 13:50:42 |
| d    |    2 |  2.0 | 2023-03-14 14:39:26 |
| d    |    2 |  4.2 | 2023-03-14 14:39:26 |
+------+------+------+---------------------+

gsutil ls -r gs://$BUCKET/cloud_functions/csv-loader/**
gs://bucket-csv-loader/cloud_functions/csv-loader/archive/product_dim/product_dim_1.csv_20230314_135042_484152
gs://bucket-csv-loader/cloud_functions/csv-loader/archive/product_dim/product_dim_2.csv_20230314_143926_285578
```

```
gsutil cp data/product_dim_3.csv gs://$BUCKET/cloud_functions/csv-loader/inbox/product_dim/
...wait
gcloud beta functions logs read $FUNCTION_NAME --limit=20


bq query --nouse_legacy_sql 'SELECT * FROM `natural-nebula-377015.dataset_csv_loader.product_dim`'
+------+------+------+---------------------+
| col1 | col2 | col3 |   load_timestamp    |
+------+------+------+---------------------+
| d    |    2 |  2.0 | 2023-03-14 14:39:26 |
| d    |    2 |  4.2 | 2023-03-14 14:39:26 |
| abc  |    1 |  2.0 | 2023-03-14 14:40:48 |
| abc  |    1 |  4.2 | 2023-03-14 14:40:48 |
| abc  |    1 | 5.99 | 2023-03-14 14:40:48 |
+------+------+------+---------------------+

gsutil ls -r gs://$BUCKET/cloud_functions/csv-loader/**
gs://bucket-csv-loader/cloud_functions/csv-loader/archive/product_dim/product_dim_1.csv_20230314_135042_484152
gs://bucket-csv-loader/cloud_functions/csv-loader/archive/product_dim/product_dim_2.csv_20230314_143926_285578
gs://bucket-csv-loader/cloud_functions/csv-loader/archive/product_dim/product_dim_3.csv_20230314_144048_524480
```


```
gsutil cp data/product_dim_4.csv gs://$BUCKET/cloud_functions/csv-loader/inbox/product_dim/
...wait
gcloud beta functions logs read $FUNCTION_NAME --limit=5

............................................................
LOG: Error tracebak uploaded to gs://bucket-csv-loader/cloud_functions/csv-loader/log/product_dim/cloud_functions/csv-loader/inbox/product_dim/product_dim_4.csv_2023-03-14 15:57:06.984577.txt

LOG: File cloud_functions/csv-loader/log/product_dim/cloud_functions/csv-loader/inbox/product_dim/product_dim_4.csv_2023-03-14 15:57:06.984577.txt not tracked.
............................................................

gsutil ls -r gs://$BUCKET/cloud_functions/csv-loader/**
gs://bucket-csv-loader/cloud_functions/csv-loader/archive/product_dim/product_dim_1.csv_20230314_135042_484152
gs://bucket-csv-loader/cloud_functions/csv-loader/archive/product_dim/product_dim_2.csv_20230314_143926_285578
gs://bucket-csv-loader/cloud_functions/csv-loader/archive/product_dim/product_dim_3.csv_20230314_144048_524480
gs://bucket-csv-loader/cloud_functions/csv-loader/log/product_dim/product_dim_4.csv_20230314_144048_524480.txt


gsutil cp "gs://bucket-csv-loader/cloud_functions/csv-loader/log/product_dim/product_dim_4.csv_20230314_144048_524480" - | tail -1
google.api_core.exceptions.BadRequest: 400 POST https://bigquery.googleapis.com/upload/bigquery/v2/projects/natural-nebula-377015/jobs?uploadType=multipart: Invalid field name "Unnamed: 3". Fields must contain only letters, numbers, and underscores, start with a letter or underscore, and be at most 300 characters long.
```

## Cleanup
```
gcloud storage buckets delete gs://$BUCKET
bq rm $DATASET
gcloud functions delete $FUNCTION_NAME
```