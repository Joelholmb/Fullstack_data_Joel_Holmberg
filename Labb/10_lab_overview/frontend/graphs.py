from utils.query_database import QueryDatabase
import plotly.express as px
import streamlit as st
import pandas as pd

class ViewsTrend:
    def __init__(self) -> None:
        self.df = QueryDatabase("SELECT * FROM marts.views_per_date").df
        print(self.df)

    def display_plot(self):
        fig = px.line(self.df, x="Datum", y="Visningar")
        st.markdown("## Antal visningar under senaste månaden")
        st.plotly_chart(fig)

# create more graphs here

class Traffic:
    def __init__(self):
        self.df = QueryDatabase("SELECT * FROM trafikkalla.summary;").df

    def display_traffic(self):
        df = self.df
        st.markdown("## Topp 5 Trafikkällor")

        # Create a dropdown to select specific traffic source or view all
        traffic_options = ["Visa alla källor"] + df["Trafikkälla"].unique().tolist()

        # Create the dropdown menu (selectbox)
        selected_traffic_source = st.selectbox(
            "Markera källan du vill se",
            options=traffic_options,
            index=0  # Default option is to show all sources
        )

        # Filter based on user selection
        if selected_traffic_source == "Visa alla källor":
            filtered_df = df
        else:
            filtered_df = df[df["Trafikkälla"] == selected_traffic_source]

        # Display top 5 based on the filtered data
        top_sources = filtered_df.nlargest(5, 'Visningar')

        # Create and display the bar chart with the filtered traffic sources
        fig = px.bar(top_sources, x='Trafikkälla', y='Visningar', title=f'Trafikkällor: {selected_traffic_source}')
        st.plotly_chart(fig)


class SubscriberGrowth:
    def __init__(self):
        self.df = QueryDatabase("SELECT * FROM prenumerations_marts.subscribers_per_date;").df

    def display_subscriber_growth(self):
        df = self.df
        st.markdown("## Tillväxt av prenumationer över tid")
        fig = px.line(df, x='Datum', y='Prenumeranter', title='Prenumationstillväxt')
        st.plotly_chart(fig)


class ViewerDemographics:
    def __init__(self):
        self.age_df = QueryDatabase("SELECT * FROM tittare_marts.age_distribution;").df
        self.gender_df = QueryDatabase("SELECT * FROM tittare_marts.gender_distribution;").df

    def display_demographics(self):
        st.markdown("## Tittarnas Demografi")

        # Age Distribution
        st.markdown("### Fördelning utav ålder")
        fig_age = px.pie(self.age_df, names='Alder', values='Visningstid_timmar_procent', 
                         title='Tittarnas åldersfördelning')
        st.plotly_chart(fig_age)

        # Gender Distribution
        st.markdown("### Fördelning utav kön")
        fig_gender = px.pie(self.gender_df, names='Kon', values='Visningstid_timmar_procent', 
                            title='Tottarnas könsfördelning')
        st.plotly_chart(fig_gender)

# Add Filtering to Views Trend
class ViewsTrend:
    def __init__(self):
        self.df = QueryDatabase("SELECT * FROM marts.views_per_date").df

    def display_plot(self):
        df = self.df.copy()
        df['Datum'] = pd.to_datetime(df['Datum']).dt.date  # Converts to date format

        st.markdown("## Visningar över tid")

        # Date range slider
        min_date = df['Datum'].min()
        max_date = df['Datum'].max()
        start_date, end_date = st.slider('Select Date Range', min_value=min_date, max_value=max_date,
                                         value=(min_date, max_date))

        # Filtering dataframe
        mask = (df['Datum'] >= start_date) & (df['Datum'] <= end_date)
        filtered_df = df.loc[mask]

        fig = px.line(filtered_df, x="Datum", y="Visningar", title='Visningar över vald tidsram')
        st.plotly_chart(fig)
