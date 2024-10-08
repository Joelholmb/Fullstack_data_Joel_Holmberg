-- Create schema for viewer demographics if it does not already exist
CREATE SCHEMA IF NOT EXISTS tittare_marts;

-- Creates table for age distribution of viewers
CREATE TABLE IF NOT EXISTS tittare_marts.age_distribution AS (
    SELECT
        t."Tittarnas ålder" AS Alder,  
        t."Visningar (%)" AS Visningar_procent,  
        t."Genomsnittlig visningslängd" AS Genomsnittlig_visningslängd,  
        t."Genomsnittlig procent som har visats (%)" AS Genomsnittlig_procent_visad,  
        t."Visningstid (timmar) (%)" AS Visningstid_timmar_procent  
        (
            -- Selects all rows from the source table but only include rows where age is not null or empty
            SELECT *
            FROM tittare.tabelldata_alder
            WHERE "Tittarnas ålder" IS NOT NULL AND "Tittarnas ålder" != ''
        ) t
);

-- Creates table for gender distribution of viewers
CREATE TABLE IF NOT EXISTS tittare_marts.gender_distribution AS (
    SELECT
        t."Tittarnas kön" AS Kon,  
        t."Visningar (%)" AS Visningar_procent, 
        t."Genomsnittlig visningslängd" AS Genomsnittlig_visningslängd,  
        t."Genomsnittlig procent som har visats (%)" AS Genomsnittlig_procent_visad,  
        t."Visningstid (timmar) (%)" AS Visningstid_timmar_procent  
    FROM
        (
            -- Selects all rows from the source table but only include rows where gender is not null or empty
            SELECT *
            FROM tittare.tabelldata_kon
            WHERE "Tittarnas kön" IS NOT NULL AND "Tittarnas kön" != ''
        ) t
);

-- Verifys the created age distribution table
SELECT * FROM tittare_marts.age_distribution;

-- Verifys the created gender distribution table
SELECT * FROM tittare_marts.gender_distribution;
