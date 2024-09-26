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
            SELECT *
            FROM innehall.tabelldata
            WHERE Innehåll IS NOT NULL AND Innehåll != 'Totalt' AND Innehåll != ''
        ) t
    ORDER BY
        t.Visningar DESC
    LIMIT 5
);

SELECT * FROM top_5_videos;

