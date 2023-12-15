This cloud functions code is picking up csv files when uploaded to a bucket and loads them into a BigQuery table.

## Environment Preparation
```
gcloud auth login
gcloud config set project natural-nebula-377015

gcloud storage buckets create gs://bucket-csv-loader
bq mk dataset_csv_loader
```


## Deployment

```

# first deployment
gcloud functions deploy function-csv-loader2 --env-vars-file .env.yaml --runtime python310 --trigger-bucket gs://bucket-csv-loader --entry-point load_csv --memory 128MB
# re-deployment
gcloud functions deploy function-csv-loader

```

## Testing
```
gcloud functions describe function-csv-loader
gsutil cp tabela.csv gs://bucket-csv-loader/
...wait
bq query --nouse_legacy_sql 'SELECT count(*) FROM `natural-nebula-377015.dataset_csv_loader.tabela`'
+-----+
| f0_ |
+-----+
|   2 |
+-----+
```

## Cleanup
```
gcloud storage buckets delete gs://bucket-csv-loader
bq rm dataset_csv_loader
gcloud functions delete function-csv-loader
```