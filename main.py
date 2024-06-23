import os
import streamlit as st
import numpy as np
from conn import *
from preprocess import *
from visual import *
from accuracy import *
from export import *
from model import *

def main():
    st.title("Sistem Deteksi Transaksi Keuangan Mencurigakan")
    st.subheader("1. Data")
    with st.expander("Petunjuk Penggunaan") :
        st.write("1. Menggunakan File CSV/Excel"
                 "\n\n\t a. Pilih Sumber Data: Pastikan untuk memilih opsi file CSV atau Excel sebagai sumber data Anda."
                 "\n\n\t b. Unggah File: Masukkan file CSV atau Excel Anda ke dalam kolom yang tersedia."
                 "\n\n\t c. Mulai Training SOM: Centang checkbox “Train SOM”."
                 "\n\n\t d. Tunggu Proses: Tunggu hingga proses training selesai. \n\n"
                 "2. Menggunakan Database"
                 "\n\n\t a. Pilih opsi database sebagai sumber data Anda."
                 "\n\n\t b. Mulai Training SOM: Centang checkbox “Train SOM”."
                 "\n\n\t c. Tunggu Proses: Tunggu hingga proses training selesai.")
    data_source = st.radio("Pilih sumber data", ("CSV/Excel File", "Database"))
    upload_file = None
    transaction_data = None

    with st.expander("Dataset", expanded=True):
        if data_source == "CSV/Excel File":
            uploaded_file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])
            if uploaded_file is not None:
                transaction_data = load_data(uploaded_file)
            else:
                st.warning("Please upload a file.")
                return
    if data_source == "Database":
        transaction_data = load_data_transaction()

    if transaction_data is not None:
        scaled_data = preprocess_data(transaction_data)

        # Train SOM or load from saved model
        st.subheader("2. Train Model")
        som_filename = 'som_model.pkl'
        if st.checkbox('Train SOM'):
            som = train_som(scaled_data, verbose=False)
            save_som_model(som, som_filename)
            st.success("SOM model trained and saved successfully.")
        else:
            if os.path.exists(som_filename):
                som = load_som_model(som_filename)
            else:
                st.error("SOM model has not been trained. Please train the model first.")
                return

        plot_som_distance_map(som)
        plot_som_clustering(som, scaled_data)
        kmeans = train_kmeans(som, scaled_data)
        plot_kmeans_clustering(som, scaled_data)

        kmeans, labels = train_kmeans(som, scaled_data)
        fraud_labels = np.where(labels > 0.5, 1, 0)  # assign "fraud" label if kmeans.labels_ > 0.5, otherwise assign "non-fraud" label
        transaction_data['fraud_label'] = fraud_labels
        fraud_data = transaction_data[kmeans.labels_ == 1]
        nfraud_data = transaction_data[kmeans.labels_ == 0]

        st.subheader('3. Transaction Data with Fraud Labels')
        st.write(transaction_data)
        st.write('Total Data:', len(transaction_data))
        st.write('Total Fraud:', len(fraud_data))
        st.write('Total Non Fraud:', len(nfraud_data))

        # Evaluate clustering
        # dbi(scaled_data, labels)
        # sil_score(scaled_data, labels)

        st.subheader('4. Fraudulent Transaction Data')
        st.write(fraud_data[['tanggal', 'id_nasabah', 'jenis_mata_uang', 'nominal', 'kurs', 'jenis_transaksi', 'total', 'nama', 'fraud_label']])
        st.write('Total Fraud:', len(fraud_data))

        plot_fraud_percentage(transaction_data, kmeans, scaled_data)

        st.subheader('10. Export Data')
        file_format = st.selectbox('Select file format', ['CSV', 'Excel'])
        label = st.selectbox('Select label', ['Fraud', 'Non Fraud', 'All'])
        export_data(transaction_data, label, file_format, fraud_data, nfraud_data)
    else:
        st.warning("No data available or failed to fetch data.")
