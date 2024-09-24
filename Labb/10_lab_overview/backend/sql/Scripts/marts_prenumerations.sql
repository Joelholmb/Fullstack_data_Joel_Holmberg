CREATE SCHEMA IF NOT EXISTS prenumerations_marts;

CREATE TABLE IF NOT EXISTS prenumerations_marts.views_per_status_date AS (
    SELECT
        STRFTIME('%Y-%m-%d', d.Datum) AS Datum,
        d.Prenumerationsstatus,
        SUM(d.Visningar) AS Visningar
    FROM
        (
            SELECT *
            FROM prenumerationsstatus.diagramdata
            WHERE CAST(Datum AS TEXT) != 'Totalt'  -- Filtrera bort rader där Datum är 'Totalt'
        ) d
    GROUP BY
        Datum,
        d.Prenumerationsstatus
    ORDER BY
        Datum ASC,
        Visningar DESC
);

CREATE TABLE IF NOT EXISTS prenumerations_marts.subscribers_per_date AS (
    SELECT
        STRFTIME('%Y-%m-%d', t.Datum) AS Datum,
        SUM(t.Prenumeranter) AS Prenumeranter
    FROM
        (
            SELECT *
            FROM prenumerationskalla.totalt
            WHERE CAST(Datum AS TEXT) != 'Totalt'
        ) t
    GROUP BY
        Datum
);

-- Skapa schema för marts om det inte existerar
CREATE SCHEMA IF NOT EXISTS marts;

-- Skapa tabellen views_per_date i marts
CREATE TABLE IF NOT EXISTS marts.views_per_date AS (
    SELECT
        STRFTIME('%Y-%m-%d', v.Datum) AS Datum,
        SUM(v.Visningar) AS Visningar
    FROM
        (
            SELECT *
            FROM innehall.totalt
            WHERE CAST(Datum AS TEXT) != 'Totalt'
        ) v
    GROUP BY
        Datum
);

CREATE TABLE IF NOT EXISTS prenumerations_marts.views_and_subscribers_per_date AS (
    SELECT
        v.Datum,
        v.Visningar,
        s.Prenumeranter,
        ROUND((s.Prenumeranter * 1.0 / v.Visningar), 4) AS Prenumeranter_per_visning
    FROM
        marts.views_per_date v
    LEFT JOIN
        prenumerations_marts.subscribers_per_date s ON v.Datum = s.Datum
    ORDER BY
        v.Datum ASC
);

SELECT * FROM prenumerations_marts.views_per_status_date LIMIT 10;
SELECT * FROM prenumerations_marts.views_and_subscribers_per_date LIMIT 10;
