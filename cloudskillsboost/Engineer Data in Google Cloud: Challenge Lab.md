```
CREATE OR REPLACE TABLE `qwiklabs-gcp-03-5caf493613dd.taxirides.taxi_training_data_270`
AS
SELECT pickup_datetime, pickup_longitude as pickuplon, pickup_latitude as pickuplat, dropoff_longitude as dropofflon, dropoff_latitude as dropofflat, passenger_count as passengers, tolls_amount + fare_amount as fare_amount_556
FROM `qwiklabs-gcp-03-5caf493613dd.taxirides.historical_taxi_rides_raw` TABLESAMPLE SYSTEM (0.1 PERCENT)
WHERE trip_distance > 0
AND fare_amount >= 2.5
AND pickup_longitude between -90 and 90
AND pickup_latitude between -90 and 90
AND dropoff_longitude between -90 and 90
AND dropoff_latitude between -90 and 90
AND passenger_count > 0
;


CREATE OR REPLACE MODEL `taxirides.fare_model_713`
OPTIONS
(
model_type='linear_reg',
labels = ['fare_amount_556']
)
AS
#standardSQL
SELECT
  fare_amount_556, ST_Distance(ST_GeogPoint(pickuplon, pickuplat), ST_GeogPoint(dropofflon, dropofflat)) AS euclidean
FROM
  `qwiklabs-gcp-03-5caf493613dd.taxirides.taxi_training_data_270`
;

create or replace table `qwiklabs-gcp-03-5caf493613dd.taxirides.2015_fare_amount_predictions`
as 
SELECT * FROM ML.PREDICT(
  MODEL `qwiklabs-gcp-03-5caf493613dd.taxirides.fare_model_713`,
  (
    select 
      *, ST_Distance(ST_GeogPoint(pickuplon, pickuplat), ST_GeogPoint(dropofflon, dropofflat)) AS euclidean
    from `qwiklabs-gcp-03-5caf493613dd.taxirides.report_prediction_data`)
  )
;
```
