import streamlit as st
import numpy as np
from sklearn.metrics import davies_bouldin_score, silhouette_score

def evaluate_clustering(scaled_data, labels):
    """Evaluate clustering performance using Davies-Bouldin Index and Silhouette Score"""
    db_index = davies_bouldin_score(scaled_data, labels)
    silhouette_avg = silhouette_score(scaled_data, labels)
    return db_index, silhouette_avg

def dbi(scaled_data, labels):
    if len(np.unique(labels)) > 1:  # Pastikan terdapat lebih dari satu klaster
        db_index = davies_bouldin_score(scaled_data, labels)
        st.write(f"Davies-Bouldin Index: {db_index:.2f}")
        if db_index < 1:
            st.write("Davies-Bouldin Index indicates good clustering.")
        elif 1 <= db_index < 2:
            st.write("Davies-Bouldin Index indicates decent clustering.")
        elif 2 <= db_index < 5:
            st.write("Davies-Bouldin Index indicates acceptable clustering.")
        else:
            st.write("Davies-Bouldin Index indicates poor clustering.")
    else:
        st.write("Davies-Bouldin Index cannot be computed with only one cluster.")

def sil_score(scaled_data, labels):
    if len(np.unique(labels)) > 1:  # Pastikan terdapat lebih dari satu klaster
        silhouette_avg = silhouette_score(scaled_data, labels)
        st.write(f"Silhouette Score: {silhouette_avg:.2f}")
        if silhouette_avg > 0.5:
            st.write("Silhouette Score indicates good clustering.")
        elif 0.2 < silhouette_avg <= 0.5:
            st.write("Silhouette Score indicates that clustering can be improved.")
        else:
            st.write("Silhouette Score indicates poor clustering.")
    else:
        st.write("Silhouette Score cannot be computed with only one cluster.")
