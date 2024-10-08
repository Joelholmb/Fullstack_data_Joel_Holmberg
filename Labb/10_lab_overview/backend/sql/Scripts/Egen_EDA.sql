-- Explore the data table to understand its structure and content
SELECT * FROM datum.tabelldata LIMIT 10;

-- Explore the "totalt" table to check for summary data
SELECT * FROM datum.totalt LIMIT 10;

-- Explore device type data to see how views are distributed across different device types
SELECT * FROM enhetstyp.diagramdata LIMIT 10;

-- Explore age data to understand the distribution of viewers by age group
SELECT * FROM tittare.tabelldata_alder LIMIT 10;

-- Explore gender data to understand the distribution of viewers by gender
SELECT * FROM tittare.tabelldata_kon LIMIT 10;

-- Retrieve the top 5 videos based on the number of exposures
SELECT 
    Videotitel,
    Exponeringar,
    "Klickfrekvens för exponeringar (%)" AS Klickfrekvens
FROM 
    innehall.tabelldata
ORDER BY 
    Exponeringar DESC  -- Order by impressions in descending order
LIMIT 5;  -- Limit to the top 5 videos

-- Retrieve traffic sources along with the average watch time per source
SELECT 
    "Trafikkälla",
    AVG("Visningstid (timmar)") AS Genomsnittlig_visningstid 
FROM 
    trafikkalla.tabelldata
GROUP BY 
    Trafikkälla
ORDER BY 
    Genomsnittlig_visningstid DESC;  -- Order by average watch time in descending order

-- Retrieve the top 5 videos that contributed most to subscriber growth
SELECT 
    Videotitel,
    Prenumeranter
FROM 
    innehall.tabelldata
WHERE 
    Prenumeranter IS NOT NULL  -- Filter out videos with no subscriber data
ORDER BY 
    Prenumeranter DESC  -- Order by subscriber growth in descending order
LIMIT 5;  -- Limit to the top 5 videos

-- Retrieve the average click-through rate (CTR) for impressions per traffic source
SELECT 
    "Trafikkälla",
    AVG("Klickfrekvens för exponeringar (%)") AS Genomsnittlig_klickfrekvens
    trafikkalla.tabelldata
WHERE 
    "Klickfrekvens för exponeringar (%)" IS NOT NULL
GROUP BY 
    Trafikkälla
ORDER BY 
    Genomsnittlig_klickfrekvens DESC;  -- Order by average CTR in descending order
