# Build and Optimize Data Warehouses with BigQuery: Challenge Lab
```
1 hour 30 minutes
Free
GSP340
Google Cloud self-paced labs logo

Overview
In a challenge lab you’re given a scenario and a set of tasks. Instead of following step-by-step instructions, you will use the skills learned from the labs in the quest to figure out how to complete the tasks on your own! An automated scoring system (shown on this page) will provide feedback on whether you have completed your tasks correctly.

When you take a challenge lab, you will not be taught new Google Cloud concepts. You are expected to extend your learned skills, like changing default values and reading and researching error messages to fix your own mistakes.

To score 100% you must successfully complete all tasks within the time period!

This lab is recommended for students enrolled in the Build and Optimize Data Warehouses with BigQuery Quest.

Topics tested

Use BigQuery to access public COVID and other demographic datasets.
Create a new BigQuery dataset which will store your tables.
Add a new date partitioned table to your dataset.
Add new columns to this table with appropriate data types.
Run a series of JOINS to populate these new columns with data drawn from other tables.
Setup
Before you click the Start Lab button
Read these instructions. Labs are timed and you cannot pause them. The timer, which starts when you click Start Lab, shows how long Google Cloud resources will be made available to you.

This hands-on lab lets you do the lab activities yourself in a real cloud environment, not in a simulation or demo environment. It does so by giving you new, temporary credentials that you use to sign in and access Google Cloud for the duration of the lab.

To complete this lab, you need:

Access to a standard internet browser (Chrome browser recommended).
Note: Use an Incognito or private browser window to run this lab. This prevents any conflicts between your personal account and the Student account, which may cause extra charges incurred to your personal account.
Time to complete the lab---remember, once you start, you cannot pause a lab.
Note: If you already have your own personal Google Cloud account or project, do not use it for this lab to avoid extra charges to your account.
Challenge scenario
You are part of an international public health organization which is tasked with developing a machine learning model to predict the daily case count for countries during the Covid-19 pandemic. As a junior member of the Data Science team you've been assigned to use your data warehousing skills to develop a table containing the features for the machine learning model.

You are expected to have the skills and knowledge for these tasks, so don't expect step-by-step guides to be provided.

Your challenge
Your first step is to create a new dataset and table. The starting point for the machine learning model will be the oxford_policy_tracker table in the COVID 19 Government Response public dataset which contains details of different actions taken by governments to curb the spread of Covid-19 in their jurisdictions.

Given the fact that there will be models based on a range of time periods, you are instructed to create a new dataset and then create a date partitioned version of the oxford_policy_tracker table in your newly created dataset, with an expiry time set to 1080 days.

You have also been instructed to exclude the United Kingdom ( alpha_3_code='GBR'), Brazil ( alpha_3_code='BRA'), Canada ( alpha_3_code='CAN') & the United States of America (alpha_3_code='USA) as these will be subject to more in-depth analysis through nation and state specific analysis.

Then, in terms of additional information that is required, you have been told to add columns for population, country_area and a record column (named mobility) that will take six input fields representing average mobility data from the last six columns of the mobility_report table from the Google COVID 19 Mobility public dataset.

A colleague working on an ancillary task has provided you with the SQL they used for updating the daily new case data in a similar data partitioned table through a JOIN with the covid_19_geographic_distribution_worldwide table from the European Center for Disease Control COVID 19 public dataset.

This is a useful table that contains a range of data, including recent national population data, that you should use to populate the population column in your table:

UPDATE
    covid.oxford_policy_tracker t0
SET
    t0.population = t2.pop_data_2019
FROM
    (SELECT DISTINCT country_territory_code, pop_data_2019 FROM `bigquery-public-data.covid19_ecdc.covid_19_geographic_distribution_worldwide`) AS t2
WHERE t0.alpha_3_code = t2.country_territory_code;
Copied!
The above template updates a daily new case column so you must modify it before you can use it to populate the population data from the European Center for Disease Control COVID 19 public dataset but the final query will be very similar.

In addition to population date you must also add in country area data to your table. The data for geographic country areas can be found in the country_names_area table from the Census Bureau International public dataset.

The last data ingestion task requires you to extract average values for the six component fields that comprise the mobility record data from the mobility_report table from the Google COVID 19 Mobility public dataset .

You need to be aware that the mobility information might be broken down by sub-regions for some countries so there may be more than one daily record for each country. However the machine learning model you are working on will only operate on a country level so you must extract a daily average for these mobility fields that aggregates all daily records for each country into a single average for each mobility record element.

In order to ensure you are aligned with the rest of the team the following column names and data types have been specified that you must use when updating the schema for your table:

New Column Name          SQL Data Type
population               INTEGER
country_area             FLOAT
mobility                 RECORD
mobility.avg_retail      FLOAT
mobility.avg_grocery     FLOAT
mobility.avg_parks       FLOAT
mobility.avg_transit     FLOAT
mobility.avg_workplace   FLOAT
mobility.avg_residential FLOAT
Copied!
Your coworker has also given you a SQL snippet that is currently being used to analyze trends in the Google Mobility data daily mobility patterns. You should be able to use this as part of the query that will add the daily country data for the mobility record in your table.

 SELECT country_region, date,
      AVG(retail_and_recreation_percent_change_from_baseline) as avg_retail,
      AVG(grocery_and_pharmacy_percent_change_from_baseline)  as avg_grocery,
      AVG(parks_percent_change_from_baseline) as avg_parks,
      AVG(transit_stations_percent_change_from_baseline) as avg_transit,
      AVG( workplaces_percent_change_from_baseline ) as avg_workplace,
      AVG( residential_percent_change_from_baseline)  as avg_residential
      FROM `bigquery-public-data.covid19_google_mobility.mobility_report`
      GROUP BY country_region, date
Copied!
When performing the JOINs between these various tables, you will need to use either the alpha_3_code column which is the 3 letter country code, or the country_name column in your table which contains the full official country name. The corresponding column names in the secondary data tables may be different.

For your final task you must identify data issues that will need to be resolved by another member of your team. Once you have your columns populated, please run a query that returns a combined list of the DISTINCT countries that do not have any population data and countries that do not have country area information, ordered by country name. If a country has neither population nor country area it should appear twice. This will give you an idea of problematic countries.

Task 1. Create a table partitioned by date
Create a new dataset covid_154 and create a table oxford_policy_tracker_856 in that dataset partitioned by date, with an expiry of 1080 days. The table should initially use the schema defined for the oxford_policy_tracker table in the COVID 19 Government Response public dataset .

You must also populate the table with the data from the source table for all countries except the United Kingdom (GBR), Brazil (BRA), Canada (CAN) and the United States (USA).

Assessment Completed!
Check that a table partitioned by date based on the Oxford Policy Tracker table has been created.
Assessment Completed!
Task 2. Add new columns to your table
Update your table to add new columns to your table with the appropriate data types to ensure alignment with the specification provided to you:
New Column Name          SQL Data Type
population               INTEGER
country_area             FLOAT
mobility                 RECORD
mobility.avg_retail      FLOAT
mobility.avg_grocery     FLOAT
mobility.avg_parks       FLOAT
mobility.avg_transit     FLOAT
mobility.avg_workplace   FLOAT
mobility.avg_residential FLOAT
Copied!
Assessment Completed!
Check that all new columns have been correctly added.
Assessment Completed!
Task 3. Add country population data to the population column
Add the country population data to the population column in your table with covid_19_geographic_distribution_worldwide table data from the European Center for Disease Control COVID 19 public dataset table.

Assessment Completed!
Check that the population column has been correctly populated.
Assessment Completed!
Task 4. Add country area data to the country_area column
Add the country area data to the country_area column in your table with country_names_area table data from the Census Bureau International public dataset.

Assessment Completed!
Check that the country_area column has been correctly populated.
Assessment Completed!
Task 5. Populate the mobility record data
Populate the mobility record in your table with data from the Google COVID 19 Mobility public dataset .

Assessment Completed!
Check that the mobility record has been correctly populated.
Assessment Completed!
Task 6. Query missing data in population & country_area columns
Run a query to find the missing countries in the population and country_area data. The query should list countries that do not have any population data and countries that do not have country area information, ordered by country name. If a country has neither population or country area it must appear twice.
Assessment Completed!
Check query for missing data was correctly run.
Assessment Completed!
The Activity tracking section needs to be completed once the above scenario is approved.

Tips and tricks
Tip 1. Remember that you must exclude the United Kingdom (GBR), Brazil (BRA), Canada (CAN) and the United States (USA) data from your initial table.
Tip 2. When updating the schema for a BigQuery table you can use the console to add the columns and record elements or you can use the command line bqutility to update the schema by providing a JSON file with all of field definitions as explained in the BigQuery Standard SQL reference documentation.
Tip 3. The covid19_ecdc table in the European Center for Disease Control COVID 19 public dataset contains a population column that you can use to populate the populationcolumn in your dataset.
Tip 4. The country_names_area table from the Census Bureau International public dataset does not contain a three letter country code column, but you can join it to your table using the full text country_name column that exists in both tables.
Tip 5. When updating the mobility record remember that you must select (and average) a number of records for each country and date combination so that you get a single average of each child column in the mobility record. You must join the resulting data to your working table using the same combination of country name and date that you used to group the source mobility records to ensure there is a unique mapping between the averaged source mobility table results and the records in your table that have a single entry for each country and date combination.
TIP 6. The UNION option followed by the ALL keyword combines the results of two queries where each query lists distinct results without combining duplicate results that arise from the union into a single row.
```

# Solution  

```shell
bq show --schema --format=prettyjson bigquery-public-data:covid19_govt_response.oxford_policy_tracker > schema_old.json
bq mk covid_154
-- bq mk --table qwiklabs-gcp-02-301fccd4e4bb:covid_154.oxford_policy_tracker_856 schema_old.json

bq mk \
   -t \
   --schema schema_old.json \
   --time_partitioning_field date \
   --time_partitioning_type DAY \
   --time_partitioning_expiration 93312000  \
   qwiklabs-gcp-02-301fccd4e4bb:covid_154.oxford_policy_tracker_856

bq update --time_partitioning_expiration 93312000 qwiklabs-gcp-02-301fccd4e4bb:covid_154.oxford_policy_tracker_856

bq update qwiklabs-gcp-02-301fccd4e4bb:covid_154.oxford_policy_tracker_856 schema_new.json
```

```sql
insert into `qwiklabs-gcp-02-301fccd4e4bb.covid_154.oxford_policy_tracker_856`
SELECT * FROM `bigquery-public-data.covid19_govt_response.oxford_policy_tracker`
WHERE alpha_3_code not in ('GBR', 'BRA', 'CAN', 'USA')

UPDATE
    `qwiklabs-gcp-02-301fccd4e4bb.covid_154.oxford_policy_tracker_856` t0
SET
    t0.population = t2.pop_data_2019
FROM
    (SELECT DISTINCT country_territory_code, pop_data_2019 FROM `bigquery-public-data.covid19_ecdc.covid_19_geographic_distribution_worldwide`) AS t2
WHERE t0.alpha_3_code = t2.country_territory_code;

UPDATE
    `qwiklabs-gcp-02-301fccd4e4bb.covid_154.oxford_policy_tracker_856` t0
SET
    t0.country_area = t2.country_area
FROM
    (SELECT country_name, country_area FROM `bigquery-public-data.census_bureau_international.country_names_area`) AS t2
WHERE t0.country_name = t2.country_name;


UPDATE
    `qwiklabs-gcp-02-301fccd4e4bb.covid_154.oxford_policy_tracker_856` t0
SET
    t0.mobility = STRUCT<avg_retail FLOAT64,
avg_grocery FLOAT64,
avg_parks FLOAT64,
avg_transit FLOAT64,
avg_workplace FLOAT64,
avg_residential FLOAT64>(
        t2.avg_retail,
        t2.avg_grocery,
        t2.avg_parks,
        t2.avg_transit,
        t2.avg_workplace,
        t2.avg_residential
    )
FROM
    (
      SELECT country_region, date,
      AVG(retail_and_recreation_percent_change_from_baseline) as avg_retail,
      AVG(grocery_and_pharmacy_percent_change_from_baseline)  as avg_grocery,
      AVG(parks_percent_change_from_baseline) as avg_parks,
      AVG(transit_stations_percent_change_from_baseline) as avg_transit,
      AVG( workplaces_percent_change_from_baseline ) as avg_workplace,
      AVG( residential_percent_change_from_baseline)  as avg_residential
      FROM `bigquery-public-data.covid19_google_mobility.mobility_report`
      GROUP BY country_region, date
    ) AS t2
WHERE t0.country_name = t2.country_region
and t0.date=t2.date;


SELECT * FROM
(
    SELECT distinct country_name 
    FROM `qwiklabs-gcp-02-301fccd4e4bb.covid_154.oxford_policy_tracker_856`
    WHERE country_area is null
UNION ALL
    SELECT distinct country_name 
    FROM `qwiklabs-gcp-02-301fccd4e4bb.covid_154.oxford_policy_tracker_856`
    WHERE population is null
)
ORDER BY country_name;
```

schema_new.json
```
[
    {
        "description": "Name of the country",
        "mode": "NULLABLE",
        "name": "country_name",
        "type": "STRING"
    },
    {
        "description": "3-letter alpha code abbreviation of the country/region. See `bigquery-public-data.utility_us.country_code_iso` for more details",
        "mode": "NULLABLE",
        "name": "alpha_3_code",
        "type": "STRING"
    },
    {
        "description": "Name of the region within the country",
        "mode": "NULLABLE",
        "name": "region_name",
        "type": "STRING"
    },
    {
        "description": "Code of the region within the country",
        "mode": "NULLABLE",
        "name": "region_code",
        "type": "STRING"
    },
    {
        "description": "Date of the measured policy action status",
        "mode": "NULLABLE",
        "name": "date",
        "type": "DATE"
    },
    {
        "description": "C1 - Ordinal scale record closings of schools and universities; 0 - No measures 1 - recommend closing 2 - Require closing (only some levels or categories eg just high school or just public schools) 3 - Require closing all levels No data - blank",
        "mode": "NULLABLE",
        "name": "school_closing",
        "type": "STRING"
    },
    {
        "description": "Are C1 actions targeted at specific areas or general:0 - Targeted 1- General No data - blank",
        "mode": "NULLABLE",
        "name": "school_closing_flag",
        "type": "STRING"
    },
    {
        "description": "Additional details about C1 policy actions",
        "mode": "NULLABLE",
        "name": "school_closing_notes",
        "type": "STRING"
    },
    {
        "description": "C2 - Ordinal scale record closings of workplace; 0 - No measures 1 - recommend closing (or work from home) 2 - require closing (or work from home) for some sectors or categories of workers 3 - require closing (or work from home) all-but-essential workplaces (eg grocery stores doctors) No data - blank",
        "mode": "NULLABLE",
        "name": "workplace_closing",
        "type": "STRING"
    },
    {
        "description": "Are C2 actions targeted at specific areas or general:0 - Targeted 1- General No data - blank",
        "mode": "NULLABLE",
        "name": "workplace_closing_flag",
        "type": "STRING"
    },
    {
        "description": "Additional details about C2 policy actions",
        "mode": "NULLABLE",
        "name": "workplace_closing_notes",
        "type": "STRING"
    },
    {
        "description": "C3 - Ordinal scale record cancellations of public events;0- No measures 1 - Recommend cancelling 2 - Require cancelling No data - blank",
        "mode": "NULLABLE",
        "name": "cancel_public_events",
        "type": "STRING"
    },
    {
        "description": "Are C3 actions targeted at specific areas or general:0 - Targeted 1- General No data - blank",
        "mode": "NULLABLE",
        "name": "cancel_public_events_flag",
        "type": "STRING"
    },
    {
        "description": "Additional details about C3 policy actions",
        "mode": "NULLABLE",
        "name": "cancel_public_events_notes",
        "type": "STRING"
    },
    {
        "description": "C4 - Ordinal scale to record the cut-off size for bans on private gatherings;  0 - No restrictions 1 - Restrictions on very large gatherings (the limit is above 1000 people) 2 - Restrictions on gatherings between 100-1000 people 3 - Restrictions on gatherings between 10-100 people 4 - Restrictions on gatherings of less than 10 people No data - blank",
        "mode": "NULLABLE",
        "name": "restrictions_on_gatherings",
        "type": "STRING"
    },
    {
        "description": "Are C4 actions targeted at specific areas or general:0 - Targeted 1- General No data - blank",
        "mode": "NULLABLE",
        "name": "restrictions_on_gatherings_flag",
        "type": "STRING"
    },
    {
        "description": "Additional details about C4 policy actions",
        "mode": "NULLABLE",
        "name": "restrictions_on_gatherings_notes",
        "type": "STRING"
    },
    {
        "description": "C5 - Ordinal scale to record closing of public transportation; 0 - No measures 1 - Recommend closing (or significantly reduce volume/route/means of transport available) 2 - Require closing (or prohibit most citizens from using it)",
        "mode": "NULLABLE",
        "name": "close_public_transit",
        "type": "STRING"
    },
    {
        "description": "Are C5 actions targeted at specific areas or general:0 - Targeted 1- General No data - blank",
        "mode": "NULLABLE",
        "name": "close_public_transit_flag",
        "type": "STRING"
    },
    {
        "description": "Additional details about C5 policy actions",
        "mode": "NULLABLE",
        "name": "close_public_transit_notes",
        "type": "STRING"
    },
    {
        "description": "C6 - Ordinal scale record of orders to \u201cshelter-in- place\u201d and otherwise confine to home.",
        "mode": "NULLABLE",
        "name": "stay_at_home_requirements",
        "type": "STRING"
    },
    {
        "description": "Are C6 actions targeted at specific areas or general:0 - Targeted 1- General No data - blank\"\\",
        "mode": "NULLABLE",
        "name": "stay_at_home_requirements_flag",
        "type": "STRING"
    },
    {
        "description": "Additional details about C6 policy actions",
        "mode": "NULLABLE",
        "name": "stay_at_home_requirements_notes",
        "type": "STRING"
    },
    {
        "description": "C7 - Ordinal scale of restrictions on internal movement;  0 - No measures 1 - Recommend closing (or significantly reduce volume/route/means of transport) 2 - Require closing (or prohibit most people from using it)",
        "mode": "NULLABLE",
        "name": "restrictions_on_internal_movement",
        "type": "STRING"
    },
    {
        "description": "Are C7 actions targeted at specific areas or general:0 - Targeted 1- General No data - blank",
        "mode": "NULLABLE",
        "name": "restrictions_on_internal_movement_flag",
        "type": "STRING"
    },
    {
        "description": "Additional details about C7 policy actions",
        "mode": "NULLABLE",
        "name": "restrictions_on_internal_movement_notes",
        "type": "STRING"
    },
    {
        "description": "C8 - Ordinal scale record of restrictions on international travel; 0 - No measures 1 - Screening 2 - Quarantine arrivals from high-risk regions 3 - Ban on high-risk regions 4 - Total border closure No data - blank",
        "mode": "NULLABLE",
        "name": "international_travel_controls",
        "type": "STRING"
    },
    {
        "description": "Additional details about C8 policy actions",
        "mode": "NULLABLE",
        "name": "international_travel_controls_notes",
        "type": "STRING"
    },
    {
        "description": "E1 - Ordinal scale record if the government is covering the salaries or providing direct cash payments universal basic income or similar of people who lose their jobs or cannot work. (Includes payments to firms if explicitly linked to payroll/ salaries)",
        "mode": "NULLABLE",
        "name": "income_support",
        "type": "STRING"
    },
    {
        "description": "Sector scope of E1 actions;  0 - formal sector workers only 1 - transfers to informal sector workers too No data - blank",
        "mode": "NULLABLE",
        "name": "income_support_flag",
        "type": "STRING"
    },
    {
        "description": "Additional details about E1 policy actions",
        "mode": "NULLABLE",
        "name": "income_support_notes",
        "type": "STRING"
    },
    {
        "description": "E2 - Record if govt. is freezing financial obligations (eg stopping loan repayments preventing services like water from stopping or banning evictions)",
        "mode": "NULLABLE",
        "name": "debt_contract_relief",
        "type": "STRING"
    },
    {
        "description": "Additional details about E2 policy actions",
        "mode": "NULLABLE",
        "name": "debt_contract_relief_notes",
        "type": "STRING"
    },
    {
        "description": "E3 - What economic stimulus policies are adopted (in USD); Record monetary value USD of fiscal stimuli including spending or tax cuts NOT included in S10 (see below) -If none enter 0 No data - blank Please use the exchange rate of the date you are coding not the current date.",
        "mode": "NULLABLE",
        "name": "fiscal_measures",
        "type": "FLOAT"
    },
    {
        "description": "Additional details about E3 policy actions",
        "mode": "NULLABLE",
        "name": "fiscal_measures_notes",
        "type": "STRING"
    },
    {
        "description": "E4 - Announced offers of COVID-19 related aid spending to other countries (in USD);  Record monetary value announced if additional to previously announced spending -if none enter 0 No data - blank Please use the exchange rate of the date you are coding not the current date.",
        "mode": "NULLABLE",
        "name": "international_support",
        "type": "FLOAT"
    },
    {
        "description": "Additional details about E4 policy actions",
        "mode": "NULLABLE",
        "name": "international_support_notes",
        "type": "STRING"
    },
    {
        "description": "H1 - Ordinal scale record presence of public info campaigns;  0 -No COVID-19 public information campaign 1 - public officials urging caution about COVID-19 2 - coordinated public information campaign (e.g. across traditional and social media) No data - blank",
        "mode": "NULLABLE",
        "name": "public_information_campaigns",
        "type": "STRING"
    },
    {
        "description": "Sector scope of H1 actions;  0 - formal sector workers only 1 - transfers to informal sector workers too No data - blank",
        "mode": "NULLABLE",
        "name": "public_information_campaigns_flag",
        "type": "STRING"
    },
    {
        "description": "Additional details about H1 policy actions",
        "mode": "NULLABLE",
        "name": "public_information_campaigns_notes",
        "type": "STRING"
    },
    {
        "description": "H2 - Ordinal scale record of who can get tested;  0 \u2013 No testing policy 1 \u2013 Only those who both (a) have symptoms AND (b) meet specific criteria (eg key workers admitted to hospital came into contact with a known case returned from overseas) 2 \u2013 testing of anyone showing COVID-19 symptoms 3 \u2013 open public testing (eg \u201cdrive through\u201d testing available to asymptomatic people) No data Nb we are looking for policies about testing for having an infection (PCR tests) - not for policies about testing for immunity (antibody tests).",
        "mode": "NULLABLE",
        "name": "testing_policy",
        "type": "STRING"
    },
    {
        "description": "Additional details about H2 policy actions",
        "mode": "NULLABLE",
        "name": "testing_policy_notes",
        "type": "STRING"
    },
    {
        "description": "H3 - Ordinal scale record if governments doing contact tracing; 0 - No contact tracing 1 - Limited contact tracing - not done for all cases 2 - Comprehensive contact tracing - done for all cases No data",
        "mode": "NULLABLE",
        "name": "contact_tracing",
        "type": "STRING"
    },
    {
        "description": "Additional details about H3 policy actions",
        "mode": "NULLABLE",
        "name": "contact_tracing_notes",
        "type": "STRING"
    },
    {
        "description": "H4 - Short-term spending on e.g hospitals masks etc in USD; Record monetary value in USD of new short-term spending on health. If none enter 0. No data - blank Please use the exchange rate of the date you are coding not the current date.",
        "mode": "NULLABLE",
        "name": "emergency_healthcare_investment",
        "type": "FLOAT"
    },
    {
        "description": "Additional details about H4 policy actions",
        "mode": "NULLABLE",
        "name": "emergency_healthcare_investment_notes",
        "type": "STRING"
    },
    {
        "description": "H5 - Announced public spending on vaccine development in USD; Record monetary value in USD of new short-term spending on health. If none enter 0. No data - blank Please use the exchange rate of the date you are coding not the current date.",
        "mode": "NULLABLE",
        "name": "vaccine_investment",
        "type": "FLOAT"
    },
    {
        "description": "Additional details about H5 policy actions",
        "mode": "NULLABLE",
        "name": "vaccine_investment_notes",
        "type": "STRING"
    },
    {
        "description": "M1 - Record policy announcements that do not fit anywhere else",
        "mode": "NULLABLE",
        "name": "misc_wildcard",
        "type": "STRING"
    },
    {
        "description": "Additional details about M1 policy actions",
        "mode": "NULLABLE",
        "name": "misc_wildcard_notes",
        "type": "STRING"
    },
    {
        "description": "Number of confirmed COVID-19 cases",
        "mode": "NULLABLE",
        "name": "confirmed_cases",
        "type": "INTEGER"
    },
    {
        "description": "Number of confirmed COVID-19 deaths",
        "mode": "NULLABLE",
        "name": "deaths",
        "type": "INTEGER"
    },
    {
        "description": "Used after April 28 2020. Nine-point aggregation of the eight containment and closure indicators as well as H1 (public information campaigns). It reports a number between 0 to 100 that reflects the overall stringency of the governments response. This is a measure of how many of the these nine indicators (mostly around social isolation) a government has acted upon and to what degree.",
        "mode": "NULLABLE",
        "name": "stringency_index",
        "type": "FLOAT"
    },
    {
        "name": "population",
        "type": "INTEGER"
    },
    {
        "name": "country_area",
        "type": "FLOAT"
    },
    {
        "fields": [
            {
                "mode": "NULLABLE",
                "name": "avg_retail",
                "type": "FLOAT"
            },
            {
                "mode": "NULLABLE",
                "name": "avg_grocery",
                "type": "FLOAT"
            },
            {
                "mode": "NULLABLE",
                "name": "avg_parks",
                "type": "FLOAT"
            },
            {
                "mode": "NULLABLE",
                "name": "avg_transit",
                "type": "FLOAT"
            },
            {
                "mode": "NULLABLE",
                "name": "avg_workplace",
                "type": "FLOAT"
            },
            {
                "mode": "NULLABLE",
                "name": "avg_residential",
                "type": "FLOAT"
            }
        ],
        "mode": "NULLABLE",
        "name": "mobility",
        "type": "RECORD"
    }
]
```

```
