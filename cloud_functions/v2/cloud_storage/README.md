[![Open in Cloud Shell](https://gstatic.com/cloudssh/images/open-btn.svg)](https://ssh.cloud.google.com/cloudshell/editor?cloudshell_git_repo=https://github.com/lupiel/gcp_snippets)

```
BUCKET=bucket-lp-us-central1
REGION=us-central1

cd cloud_functions/v2/cloud_storage
```
```
gsutil mb -l $REGION gs://$BUCKET
```
```
PROJECT_ID=$(gcloud config get-value project)
PROJECT_NUMBER=$(gcloud projects list --filter="project_id:$PROJECT_ID" --format='value(project_number)')

SERVICE_ACCOUNT=$(gsutil kms serviceaccount -p $PROJECT_NUMBER)

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member serviceAccount:$SERVICE_ACCOUNT \
  --role roles/pubsub.publisher
```

```
gcloud functions deploy python-finalize-function \
--gen2 \
--runtime=python311 \
--region=$REGION \
--source=. \
--entry-point=hello_gcs \
--trigger-event-filters="type=google.cloud.storage.object.v1.finalized" \
--trigger-event-filters="bucket=$BUCKET"
```

```
echo "Hello World" > test-finalize.txt
gsutil cp test-finalize.txt gs://$BUCKET/test-finalize.txt
```

```
gcloud beta functions logs read python-finalize-function --gen2 --limit=100
```
