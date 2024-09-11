import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split


def read_data():
    data_path = Path(__file__).parents[2] / "data"
    df = pd.read_csv(data_path / "IceCreamData.csv")
    return df


def train_model(data):
    X = data[['Temperature']]
    y = data['Revenue']
    
    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Initialize the model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    
    # Train the model
    model.fit(X_train, y_train)
    
    return model

# Predict revenue based on temperature
def predict_revenue(model, temperature):
    prediction = model.predict(np.array([[temperature]]))[0]
    return prediction

# Streamlit app
def main():
    st.title('Ice Cream Revenue Prediction')
    
    # Load data and train the model
    data = read_data()
    model = train_model(data)
    
    # User input
    temperature = st.number_input('Enter the temperature (in Celsius):', min_value=-30.0, max_value=50.0)
    
    # Predict button
    if st.button('Predict Revenue'):
        revenue = predict_revenue(model, temperature)
        st.success(f'Predicted revenue: ${revenue:.0f}')
        
if __name__ == '__main__':
    main()
