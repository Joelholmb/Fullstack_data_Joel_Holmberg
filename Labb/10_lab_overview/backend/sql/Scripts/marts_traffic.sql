-- Create table to store views per date and traffic source if it doesn't already exist
CREATE TABLE IF NOT EXISTS trafikkalla.views_per_date AS (
    SELECT
        STRFTIME('%Y-%m-%d', d.Datum) AS Datum,  -- Format date as YYYY-MM-DD
        d.Trafikkälla,  -- Traffic source (e.g., external, search, direct, etc.)
        SUM(d.Visningar) AS Visningar  -- Total views for the traffic source on the given date
    FROM
        (
            -- Select from the traffic source diagram data, excluding summary rows
            SELECT *
            FROM trafikkalla.diagramdata
            WHERE CAST(Datum AS TEXT) != 'Totalt'  -- Exclude rows where the date is "Totalt" (summary row)
        ) d
    GROUP BY
        Datum,  -- Group by date
        d.Trafikkälla  -- Group by traffic source
    ORDER BY
        Datum ASC,  -- Order by date in ascending order
        Visningar DESC  -- Within each date, order by views in descending order
);

-- Create a summary table for traffic sources with additional metrics if it doesn't already exist
CREATE TABLE IF NOT EXISTS trafikkalla.summary AS (
    SELECT
        t.Trafikkälla, 
        t.Visningar,
        t."Visningstid (timmar)" AS Visningstid_timmar,
        t."Genomsnittlig visningslängd" AS Genomsnittlig_visningslängd,
        t.Exponeringar,
        t."Klickfrekvens för exponeringar (%)" AS Klickfrekvens_exponering_procent
    FROM
        trafikkalla.tabelldata t
    WHERE
        t.Trafikkälla != 'Totalt'  -- Exclude summary rows
);

-- Verify the views per date and traffic source table
SELECT * FROM trafikkalla.views_per_date LIMIT 10;

-- Verify the summary table for traffic sources
SELECT * FROM trafikkalla.summary;
