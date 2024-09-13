import streamlit as st
import pandas as pd
from pathlib import Path
import matplotlib as plt
import seaborn as sns

def read_data():
    data_path = Path(__file__).parents[2] / "data"
    df = pd.read_csv(data_path / "OECD PISA data.csv")
    return df

# df = read_data()
# print(df)
# st.write(df)


def plot_boxplot(data, column, by, title):
    plt.figure(figsize=(10, 6))
    sns.boxplot(x=by, y=column, data=data)
    plt.title(title)
    plt.xlabel('Score')
    plt.ylabel("Average PISA score by location")
    st.pyplot(plt)


def layout():
    
    df = read_data()
    
    total_records = df.shape[0]  # Number of rows (records)
    unique_locations = df['LOCATION'].nunique()  # Unique locations
    unique_subjects = df['SUBJECT'].nunique()  # Unique subjects
    unique_time_periods = df['TIME'].nunique()  # Unique time periods

    # Title and basic statistics
    st.markdown("# OECD PISA Dashboard")
    st.markdown("## Basic Statistics of the Data")
    
    # Display statistics in four columns
    cols = st.columns(4)
    cols[0].metric("Total Records", total_records)
    cols[1].metric("Unique Locations", unique_locations)
    cols[2].metric("Unique Subjects", unique_subjects)
    cols[3].metric("Unique Time Periods", unique_time_periods)

    st.markdown("## Sample Data")
    st.dataframe(df)

    st.header("Trends per country")
    location = st.selectbox("Choose country", df["LOCATION"].unique())

    filtered_data = df[df['LOCATION'] == location]

    country_stats = filtered_data["Value"].describe()
    cols = st.columns(4)
    stats = ["min", "50%", "max"]
    labels = ["min", "median", "max"]
    for col, stat, label in zip(cols, stats, labels):
        with col:
            st.metric(label=label, value=f"{country_stats[stat]:.0f}")


    st.markdown("## Average PISA score by location")
    if 'Value' in df.columns and 'LOCATION' in df.columns:
        average_pisa_score = df.groupby('LOCATION')["Value"].mean().sort_values(ascending=False)
        st.bar_chart(average_pisa_score)
    else:
        st.write("Error: The columns 'Value' and 'LOCATION' must exist in the dataset.")



if __name__ == "__main__":
    layout()