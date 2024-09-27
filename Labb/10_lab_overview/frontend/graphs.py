from utils.query_database import QueryDatabase
import plotly.express as px
import streamlit as st 

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
        st.markdown("## Topp 5 Traffikkällor")
        top_sources = df.nlargest(5, 'Visningar')

        fig = px.bar(top_sources, x='Trafikkälla', y='Visningar', title='Topp traffikkällor per tittare')
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
        st.markdown("## Viewer Demographics")

        # Age Distribution
        st.markdown("### Age Distribution")
        fig_age = px.pie(self.age_df, names='Alder', values='Visningstid_timmar_procent', 
                         title='Viewer Age Distribution')
        st.plotly_chart(fig_age)

        # Gender Distribution
        st.markdown("### Gender Distribution")
        fig_gender = px.pie(self.gender_df, names='Kon', values='Visningstid_timmar_procent', 
                            title='Viewer Gender Distribution')
        st.plotly_chart(fig_gender)