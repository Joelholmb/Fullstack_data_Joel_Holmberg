CREATE SCHEMA IF NOT EXISTS prenumerations_marts;

-- Creates table to aggregate views by subscription status and date
CREATE TABLE IF NOT EXISTS prenumerations_marts.views_per_status_date AS (
    SELECT
        STRFTIME('%Y-%m-%d', d.Datum) AS Datum,  -- Format the date as YYYY-MM-DD
        d.Prenumerationsstatus,  -- Subscription status (e.g., subscribed, not subscribed)
        SUM(d.Visningar) AS Visningar  -- Sum views by subscription status
    FROM
        (
            SELECT *
            FROM prenumerationsstatus.diagramdata
            WHERE CAST(Datum AS TEXT) != 'Totalt'  -- Exclude rows where the date is "Totalt" (summary row)
        ) d
    GROUP BY
        Datum,
        d.Prenumerationsstatus  -- Group by date and subscription status
    ORDER BY
        Datum ASC,  -- Order by date in ascending order
        Visningar DESC  -- Order by views in descending order within each date
);

-- Creates table to aggregate subscriber counts per date
CREATE TABLE IF NOT EXISTS prenumerations_marts.subscribers_per_date AS (
    SELECT
        STRFTIME('%Y-%m-%d', t.Datum) AS Datum,  -- Format the date as YYYY-MM-DD
        SUM(t.Prenumeranter) AS Prenumeranter  -- Sum the number of subscribers per date
    FROM
        (
            SELECT *
            FROM prenumerationskalla.totalt
            WHERE CAST(Datum AS TEXT) != 'Totalt'  -- Exclude rows where the date is "Totalt" (summary row)
        ) t
    GROUP BY
        Datum
);

CREATE SCHEMA IF NOT EXISTS marts;

-- Creates table to aggregate views per date
CREATE TABLE IF NOT EXISTS marts.views_per_date AS (
    SELECT
        STRFTIME('%Y-%m-%d', v.Datum) AS Datum,  -- Format the date as YYYY-MM-DD
        SUM(v.Visningar) AS Visningar  -- Sum views per date
    FROM
        (
            SELECT *
            FROM innehall.totalt
            WHERE CAST(Datum AS TEXT) != 'Totalt'  -- Exclude rows where the date is "Totalt" (summary row)
        ) v
    GROUP BY
        Datum
);

-- Creates table to join views and subscribers per date, and calculate subscribers per view
CREATE TABLE IF NOT EXISTS prenumerations_marts.views_and_subscribers_per_date AS (
    SELECT
        v.Datum, 
        v.Visningar, 
        s.Prenumeranter,
        ROUND((s.Prenumeranter * 1.0 / v.Visningar), 4) AS Prenumeranter_per_visning  -- Calculate subscribers per view, rounded to 4 decimals
    FROM
        marts.views_per_date v
    LEFT JOIN
        prenumerations_marts.subscribers_per_date s ON v.Datum = s.Datum  -- Left join to match views and subscribers by date
    ORDER BY
        v.Datum ASC  -- Order by date in ascending order
);

-- Verify data in views_per_status_date table
SELECT * FROM prenumerations_marts.views_per_status_date LIMIT 10;

-- Verify data in views_and_subscribers_per_date table
SELECT * FROM prenumerations_marts.views_and_subscribers_per_date LIMIT 10;
