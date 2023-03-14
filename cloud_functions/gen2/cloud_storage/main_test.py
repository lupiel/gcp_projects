from cloudevents.http import CloudEvent

import main


def test_functions_eventsource_storage(capsys):
    attributes = {
        "id": "5e9f24a",
        "type": "google.cloud.storage.object.v1.finalized",
        "source": "sourceUrlHere",
    }

    data = {
        "bucket": "test_bucket_for_storage",
        "name": "new_blob_uploaded",
        "generation": 1,
        "metageneration": 1,
        "timeCreated": "2021-10-10 00:00:00.000000Z",
        "updated": "2021-11-11 00:00:00.000000Z",
    }

    event = CloudEvent(attributes, data)

    main.hello_gcs(event)

    out, _ = capsys.readouterr()
    assert "Event ID: 5e9f24a" in out
    assert "Event type: google.cloud.storage.object.v1.finalized" in out
    assert "Bucket: test_bucket_for_storage" in out
    assert "File: new_blob_uploaded" in out
    assert "Metageneration: 1" in out
    assert "Created: 2021-10-10 00:00:00.000000Z" in out
    assert "Updated: 2021-11-11 00:00:00.000000Z" in out
