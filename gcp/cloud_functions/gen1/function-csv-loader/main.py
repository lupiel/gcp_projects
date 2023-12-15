from google.cloud import bigquery
from google.cloud import storage
from pathlib import Path
import os

def load_csv(event, context):
    """Triggered by a change to a Cloud Storage bucket.
    Args:
        event (dict): Event payload.
        context (google.cloud.functions.Context): Metadata for the event.
    """

    bucket_name = event["bucket"]
    file_name = event["name"]
    # uri = "gs://cloud-samples-data/bigquery/us-states/us-states.csv"
    uri =  f"gs://{bucket_name}/{file_name}"

    project_name = os.environ.get("project", "project env var not set")
    dataset_name = os.environ.get("dataset", "dataset env var not set")
    table_name = Path(file_name).stem
    # table_id = "your-project.your_dataset.your_table_name"
    table_id = f"{project_name}.{dataset_name}.{table_name}"

    print(f"Processing uri: {uri}.")
    print(f"Processing table_id: {table_id}.")
    print(f"Processing event: {event}.")
    print(f"Processing context: {context}.")
    
    bq_client = bigquery.Client()

    job_config = bigquery.LoadJobConfig(
        schema=[
            bigquery.SchemaField("name", "STRING"),
            bigquery.SchemaField("post_abbr", "STRING"),
        ],
        skip_leading_rows=1,
        # The source format defaults to CSV, so the line below is optional.
        source_format=bigquery.SourceFormat.CSV,
    )

    load_job = bq_client.load_table_from_uri(
        uri, table_id, job_config=job_config
    )  # Make an API request.

    load_job.result()  # Waits for the job to complete.

    destination_table = bq_client.get_table(table_id)  # Make an API request.
    print("Loaded {} rows.".format(destination_table.num_rows))

    # Delete the loaded file
    gs_client = storage.Client()

    bucket = gs_client.get_bucket(bucket_name)

    try:
        bucket.delete_blob(file_name)
    except NotFound:
        print(f"{file_name} NotFound.")
