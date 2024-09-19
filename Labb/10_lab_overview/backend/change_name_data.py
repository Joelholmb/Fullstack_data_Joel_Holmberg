from pathlib import Path
from shutil import copytree, rmtree

# Definierar sökvägen till mappen där rådata ligger
raw_data_path = Path(__file__).parent / "raw_data"

# Definierar sökvägen till mappen där de förkortade mappnamnen kommer sparas
cleaned_data_path = Path(__file__).parent / "cleaned_data"

# Om mappen "cleaned_data" redan existerar, ta bort den för att kunna skapa en ny från grunden
if cleaned_data_path.is_dir():
    rmtree(cleaned_data_path)

# Skapa en ny tom "cleaned_data"-mapp (inklusive alla underkataloger om de inte finns)
cleaned_data_path.mkdir(parents=True, exist_ok=True)

# Itererar genom alla mappar i "raw_data" för att förkorta mappnamnen och kopiera dem
for folder in raw_data_path.iterdir():
    # Förkortar mappens namn till bara den första delen (före första mellanslaget)
    new_name = folder.name.split()[0]
    
    # Kopierar mappen och dess innehåll till "cleaned_data" med det nya namnet
    copytree(folder, cleaned_data_path / new_name)

