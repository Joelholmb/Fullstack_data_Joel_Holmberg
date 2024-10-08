import streamlit as st
from utils.query_database import QueryDatabase

class ContentKPI:
    def __init__(self) -> None:
        self._content = QueryDatabase("SELECT * FROM marts.content_view_time;").df

    def display_content(self):
        df = self._content
        st.markdown("## KPIer för videor")
        st.markdown("Nedan visas KPIer för totalt antal")

        kpis = {
            "videor": len(df),
            "visade timmar": df["Visningstid_timmar"].sum(),
            "prenumeranter": df["Prenumeranter"].sum(),
            "exponeringar": df["Exponeringar"].sum(),
        }


        # adds alternative to show all kpis
        kpi_options = ["Visa alla KPI:er"] + list(kpis.keys())  # first choice is "Visa alla kpi:er"

        # creates a dropdown meny
        selected_kpi = st.selectbox(
            "Välj KPI att visa",
            options=kpi_options,  # shows all the names
            index=0  # "Visa alla kpi:er" is set as default
        )

        # checks the dropdown meny if "Visa alla kpi:er" is selected
        if selected_kpi == "Visa alla KPI:er":
            # show all kpis
            for col, kpi in zip(st.columns(len(kpis)), kpis):
                with col:
                    st.metric(kpi, round(kpis[kpi]))
        else:
            # show only selected kpi
            st.metric(selected_kpi, round(kpis[selected_kpi]))

        st.dataframe(df)

# create more KPIs here
class DeviceKPI:
    pass 

class TopVideos:
    def __init__(self):
        self.df = QueryDatabase("SELECT * FROM top_5_videos;").df

    def display_top_videos(self):
        df = self.df
        st.markdown("## Topp 5 per visningar")

        # Displays the top 5 videos in a table
        st.dataframe(df)

# Engagement Metrics, calculates and displays metrics like:
# Average View Duration
# Average Percentage Viewed
class EngagementKPI:
    def __init__(self):
        # get data feom marts.engagement_metrics
        self._content = QueryDatabase("SELECT * FROM marts.engagement_metrics;").df

    def display_engagement_kpi(self):
        df = self._content

        
        st.markdown("## KPI:er för engagemang")

        # Handle missing values with fillna to replace NaN with 0.
        df['Genomsnittlig_visningslängd_min'] = df['Genomsnittlig_visningslängd_min'].fillna(0)
        df['Genomsnittlig_procent_visad'] = df['Genomsnittlig_procent_visad'].fillna(0)

        # average data for the whole dataset
        genomsnittlig_visningslängd = df["Genomsnittlig_visningslängd_min"].mean()
        genomsnittlig_procent_visad = df["Genomsnittlig_procent_visad"].mean()

        kpi_data = {
            "Genomsnittlig visningslängd (min)": f"{genomsnittlig_visningslängd:.2f} minuter",
            "Genomsnittlig procent visad": f"{genomsnittlig_procent_visad:.2f} %"
        }

        # show kpis
        for kolumn, kpi in zip(st.columns(len(kpi_data)), kpi_data):
            with kolumn:
                st.metric(kpi, kpi_data[kpi])

        # show filtered table
        st.dataframe(df[['Videotitel', 'Genomsnittlig_visningslängd_min', 'Genomsnittlig_procent_visad']])

