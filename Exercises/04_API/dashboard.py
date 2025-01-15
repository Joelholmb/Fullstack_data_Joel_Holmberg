import streamlit as st
import pandas as pd
from datetime import datetime
import time

# Anta att du redan har definierat get_timetable(stop_id, as_dataframe=True)
# och eventuellt show_departure_board_for_stop eller liknande funktioner i en modul resrobot_api.py
# men här klistrar vi in nyckel-delarna direkt för helhetens skull:

def get_timetable(stop_id, as_dataframe=False):
    """
    Hämtar tidtabellsinfo (DepartureBoard) för en viss hållplats (stop_id)
    från ResRobot-API och returnerar en DataFrame om as_dataframe=True annars dict.
    (Denna kod har du redan, men jag visar en förenklad variant.)
    """
    import requests
    import os
    from dotenv import load_dotenv

    load_dotenv()
    API_KEY = os.getenv("API_KEY")

    url = f"https://api.resrobot.se/v2.1/departureBoard?id={stop_id}&format=json&accessId={API_KEY}"
    try:
        resp = requests.get(url)
        resp.raise_for_status()
        data = resp.json()
        if as_dataframe:
            departures = data.get("Departure", [])
            df = pd.DataFrame(departures)
            if not df.empty:
                df_clean = df[["name", "direction", "date", "time"]].copy()
                return df_clean
            else:
                return pd.DataFrame()
        else:
            return data
    except requests.exceptions.RequestException as err:
        print(f"Nätverks-/HTTP-fel: {err}")
        return None


def load_departure_data(stop_id):
    """
    1) Hämtar DataFrame från get_timetable.
    2) Filtrerar spårvagnar/bussar.
    3) Räknar ut hur många minuter det är kvar tills avgång.
    4) Returnerar en DataFrame med kolumner ['Linje', 'Riktning', 'Avgång om (min)'].
    """
    df = get_timetable(stop_id, as_dataframe=True)
    if df.empty:
        return pd.DataFrame(columns=["Linje", "Riktning", "Avgång om (min)"])

    # Filtrera på spårväg och buss
    mask = df["name"].str.contains("Spårväg|Buss", case=False, na=False)
    df_filtered = df[mask].copy()

    # Bygg en kolumn 'departure_datetime' för att räkna väntetid
    df_filtered["departure_datetime"] = pd.to_datetime(df_filtered["date"] + " " + df_filtered["time"])
    
    now = datetime.now()
    df_filtered["wait_minutes"] = ((df_filtered["departure_datetime"] - now).dt.total_seconds() // 60).astype(int)
    df_filtered["wait_minutes"] = df_filtered["wait_minutes"].clip(lower=0)  # Negativa -> 0

    # Snygga till kolumnerna
    df_filtered["Linje"] = df_filtered["name"].str.replace("Länstrafik - ", "", case=False)
    df_filtered["Riktning"] = df_filtered["direction"]
    df_filtered["Avgång om (min)"] = df_filtered["wait_minutes"]

    # Sortera på kortast väntetid först
    df_filtered.sort_values("wait_minutes", inplace=True)

    return df_filtered[["Linje", "Riktning", "Avgång om (min)"]]


# ========== STREAMLIT APP ==========

def main():
    st.title("Avgångstabla i Streamlit")
    st.write("Exempel: spårvagnar och bussar för en vald hållplats.")

    # 1) Välj hållplats (extId)
    #    Här kan du hårdkoda för Göteborg Korsvägen, eller låta användaren välja i en selectbox
    #    Ex: 740015578 är Göteborg Korsvägen
    stop_id_dict = {
        "Göteborg Korsvägen": 740015578,
        "Göteborg Central": 740000002,
        "Malmö Central": 740000003
        # Lägg till fler om du vill
    }

    choice = st.selectbox("Välj hållplats", list(stop_id_dict.keys()))
    chosen_stop_id = stop_id_dict[choice]

    # 2) Button för att ladda/uppdatera data
    if st.button("Uppdatera nu"):
        st.session_state["data_load_trigger"] = True

    # 3) Auto-uppdatering: Du kan sätta en timer/sektion om du vill
    #   Just nu kör vi inte en loop, men du kan t.ex. st.set_page_config för autorefresh,
    #   eller en while True + st.experimental_rerun (men det är mindre vanligt).
    
    # Om antingen st.session_state["data_load_trigger"] är True, eller 
    # sidan laddats första gången, ladda data:
    if "data_load_trigger" not in st.session_state or st.session_state["data_load_trigger"]:
        df_result = load_departure_data(chosen_stop_id)
        
        if df_result.empty:
            st.warning("Inga avgångar eller problem med API.")
        else:
            # Visa tabell
            st.table(df_result)

        # Nollställ trigger
        st.session_state["data_load_trigger"] = False


if __name__ == "__main__":
    main()
