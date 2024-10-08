-- Create a new mart table for engagement KPIs if not already exist
CREATE TABLE IF NOT EXISTS marts.engagement_metrics AS (
    SELECT
        Videotitel,
        -- Calculates average view duration (in minutes)
        CASE
            WHEN Visningar > 0 THEN ("Visningstid (timmar)" * 60) / Visningar
            ELSE 0
        END AS Genomsnittlig_visningslängd_min,
        -- Calculates average percentage viewed (based on an assumed video length, e.g., 10 minutes)
        CASE
            WHEN Visningar > 0 THEN (("Visningstid (timmar)" * 60) / Visningar) / 10 -- Example: 10 minutes video length
            ELSE 0
        END AS Genomsnittlig_procent_visad
    FROM
        innehall.tabelldata
    WHERE
        Innehåll != 'Totalt'  -- Filter out aggregated rows (such as "Totalt")
);

-- Check that the data has been created correctly
SELECT * FROM marts.engagement_metrics LIMIT 10;


