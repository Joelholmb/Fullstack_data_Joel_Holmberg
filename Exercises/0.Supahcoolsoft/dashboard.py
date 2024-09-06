import streamlit as st
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns

def read_data():
    data_path = Path(__file__).parents[2] / "data"
    df = pd.read_csv(data_path / "supahcoolsoft.csv")
    return df

def plot_histogram(data, column, title):
    plt.figure(figsize=(10, 6))
    plt.hist(data[column], bins=30, edgecolor='k', alpha=0.7)
    plt.title(title)
    plt.xlabel(column)
    plt.ylabel('Frequency')
    st.pyplot(plt)

def plot_boxplot(data, column, by, title):
    plt.figure(figsize=(10, 6))
    sns.boxplot(x=by, y=column, data=data)
    plt.title(title)
    plt.xlabel('Department')
    plt.ylabel(column)
    st.pyplot(plt)

def layout():

    read_css()
    
    df = read_data()
    
    total_employees = df.shape[0]  # Number of rows in the dataframe = total number of employees
    average_age = df['Age'].mean()
    average_salary = df['Salary_SEK'].mean()

    st.markdown("# Executive Dashboard")

    st.markdown("## Basic Employee Statistics")
    cols = st.columns(3)  # Create three columns to display the statistics
    cols[0].metric("Total Number of Employees", total_employees)
    cols[1].metric("Average Age", round(average_age, 1))
    cols[2].metric("Average Salary", f"{round(average_salary):,} SEK")

    st.markdown("## Raw Employee Data")
    st.dataframe(df)

    st.markdown("## Employees by Department")
    department_counts = df['Department'].value_counts()
    st.bar_chart(department_counts)

    st.markdown("## Salary Distribution")
    plot_histogram(df, 'Salary_SEK', 'Histogram of Salary Distribution')

    st.markdown("## Salaries by Department")
    plot_boxplot(df, 'Salary_SEK', 'Department', 'Boxplot of Salaries by Department')

    st.markdown("## Age Distribution")
    plot_histogram(df, "Age", "Histogram of Age Distribution")

    st.markdown("## Age by Department")
    plot_boxplot(df, 'Age', 'Department', 'Boxplot of Age by Department')

def read_css():
    css_path = Path(__file__).parent / "style.css"  # Correct file name

    with open(css_path) as css:
        st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)


if __name__ == "__main__":
    layout()
