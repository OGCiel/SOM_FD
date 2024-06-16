import streamlit as st
import pickle

def save_som_model(som, filename):
    try:
        with open(filename, 'wb') as f:
            pickle.dump(som, f)
        st.success("SOM model trained and saved successfully.")
    except Exception as e:
        st.error(f"Error saving SOM model: {e}")

def load_som_model(filename):
    try:
        with open(filename, 'rb') as f:
            som = pickle.load(f)
        return som
    except FileNotFoundError:
        st.error(f"File '{filename}' not found. Please train the SOM model first.")
        return None
