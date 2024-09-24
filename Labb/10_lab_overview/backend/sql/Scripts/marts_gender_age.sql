CREATE SCHEMA IF NOT EXISTS tittare_marts;

-- Åldersfördelning
CREATE TABLE IF NOT EXISTS tittare_marts.age_distribution AS (
    SELECT
        t."Tittarnas ålder" AS Alder,
        t."Visningar (%)" AS Visningar_procent,
        t."Genomsnittlig visningslängd" AS Genomsnittlig_visningslängd,
        t."Genomsnittlig procent som har visats (%)" AS Genomsnittlig_procent_visad,
        t."Visningstid (timmar) (%)" AS Visningstid_timmar_procent
    FROM
        (
            SELECT *
            FROM tittare.tabelldata_alder
            WHERE "Tittarnas ålder" IS NOT NULL AND "Tittarnas ålder" != ''
        ) t
);

-- Könsfördelning
CREATE TABLE IF NOT EXISTS tittare_marts.gender_distribution AS (
    SELECT
        t."Tittarnas kön" AS Kon,
        t."Visningar (%)" AS Visningar_procent,
        t."Genomsnittlig visningslängd" AS Genomsnittlig_visningslängd,
        t."Genomsnittlig procent som har visats (%)" AS Genomsnittlig_procent_visad,
        t."Visningstid (timmar) (%)" AS Visningstid_timmar_procent
    FROM
        (
            SELECT *
            FROM tittare.tabelldata_kon
            WHERE "Tittarnas kön" IS NOT NULL AND "Tittarnas kön" != ''
        ) t
);

SELECT * FROM tittare_marts.age_distribution;
SELECT * FROM tittare_marts.gender_distribution;
