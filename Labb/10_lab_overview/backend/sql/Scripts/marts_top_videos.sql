
CREATE TABLE IF NOT EXISTS top_5_videos AS (
    SELECT
        t.Videotitel, 
        t."Publiceringstid för video" AS Publiceringstid,
        t.Visningar, 
        t."Visningstid (timmar)" AS Visningstid_timmar,
        t.Exponeringar,
        t.Prenumeranter,
        t."Klickfrekvens för exponeringar (%)" AS Klickfrekvens_exponering_procent
    FROM
        (
            -- Select from the main content table, excluding any invalid or summary rows
            SELECT *
            FROM innehall.tabelldata
            WHERE Innehåll IS NOT NULL AND Innehåll != 'Totalt' AND Innehåll != ''
        ) t
    ORDER BY
        t.Visningar DESC  -- Order by views in descending order to get the most viewed videos
    LIMIT 5  -- Limit the result to the top 5 videos
);

-- Verify that the top 5 videos were inserted into the table correctly
SELECT * FROM top_5_videos;

