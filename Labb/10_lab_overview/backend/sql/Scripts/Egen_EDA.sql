-- Utforska tabelldata
SELECT * FROM datum.tabelldata LIMIT 10;

-- Utforska totalt
SELECT * FROM datum.totalt LIMIT 10;

-- Utforska diagramdata
SELECT * FROM enhetstyp.diagramdata LIMIT 10;

-- Utforska åldersdata
SELECT * FROM tittare.tabelldata_alder LIMIT 10;

-- Utforska könsdata
SELECT * FROM tittare.tabelldata_kon LIMIT 10;

-- Topp 5 videor baserat på exponeringar
SELECT 
    Videotitel, 
    Exponeringar, 
    "Klickfrekvens för exponeringar (%)" AS Klickfrekvens
FROM 
    innehall.tabelldata
ORDER BY 
    Exponeringar DESC
LIMIT 5;


-- Trafikkällor och genomsnittlig visningstid
SELECT 
    "Trafikkälla", 
    AVG("Visningstid (timmar)") AS Genomsnittlig_visningstid
FROM 
    trafikkalla.tabelldata
GROUP BY 
    Trafikkälla
ORDER BY 
    Genomsnittlig_visningstid DESC;




-- Videor som bidragit mest till prenumerationstillväxt
SELECT 
    Videotitel, 
    Prenumeranter
FROM 
    innehall.tabelldata
WHERE 
    Prenumeranter IS NOT NULL
ORDER BY 
    Prenumeranter DESC
LIMIT 5;

-- Klickfrekvens för exponeringar per trafikkälla
SELECT 
    "Trafikkälla", 
    AVG("Klickfrekvens för exponeringar (%)") AS Genomsnittlig_klickfrekvens
FROM 
    trafikkalla.tabelldata
WHERE 
    "Klickfrekvens för exponeringar (%)" IS NOT NULL
GROUP BY 
    Trafikkälla
ORDER BY 
    Genomsnittlig_klickfrekvens DESC;
