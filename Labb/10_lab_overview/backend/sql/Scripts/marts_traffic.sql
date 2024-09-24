CREATE TABLE IF NOT EXISTS trafikkalla.views_per_date AS (
    SELECT
        STRFTIME('%Y-%m-%d', d.Datum) AS Datum,
        d.Trafikkälla,
        SUM(d.Visningar) AS Visningar
    FROM
        (
            SELECT *
            FROM trafikkalla.diagramdata
            WHERE CAST(Datum AS TEXT) != 'Totalt'  -- Filtrera bort rader där Datum är 'Totalt'
        ) d
    GROUP BY
        Datum,
        d.Trafikkälla
    ORDER BY
        Datum ASC,
        Visningar DESC
);



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
        t.Trafikkälla != 'Totalt'
);

SELECT * FROM trafikkalla.views_per_date LIMIT 10;
SELECT * FROM trafikkalla.summary;
