import streamlit as st
import openpyxl

def export_data(transaction_data, label, file_format, fraud_data, nfraud_data):
    """Export fraud data to Excel or CSV file"""
    if file_format.lower() == 'excel':
        if label.lower() == 'fraud':
            fraud_data.to_excel('fraud_data.xlsx', index=False)
            st.download_button(
                label="Download Fraud Data as Excel",
                data=open('fraud_data.xlsx', 'rb').read(),
                file_name='fraud_data.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
        elif label.lower() == 'non fraud':
            nfraud_data.to_excel('non_fraud_data.xlsx', index=False)
            st.download_button(
                label="Download Non Fraud Data as Excel",
                data=open('non_fraud_data.xlsx', 'rb').read(),
                file_name='non_fraud_data.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
        elif label.lower() == 'all':
            transaction_data.to_excel('transaction_data.xlsx', index=False)
            st.download_button(
                label="Download transaction_data as Excel",
                data=open('transaction_data.xlsx', 'rb').read(),
                file_name='transaction_data.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
    elif file_format.lower() == 'csv':
        if label.lower() == 'fraud':
            fraud_data.to_csv('fraud_data.csv', index=False)
            st.download_button(
                label="Download Fraud Data as CSV",
                data=open('fraud_data.csv', 'rb').read(),
                file_name='fraud_data.csv',
                mime='text/csv'
            )
        elif label.lower() == 'non fraud':
            nfraud_data.to_csv('non_fraud_data.csv', index=False)
            st.download_button(
                label="Download Non Fraud Data as CSV",
                data=open('non_fraud_data.csv', 'rb').read(),
                file_name='non_fraud_data.csv',
                mime='text/csv'
            )
        elif file_format.lower() == 'csv' and label.lower() == 'all':
            transaction_data.to_csv('transaction_data.csv', index=False)
            st.download_button(
                label="Download transaction_data as CSV",
                data=open('transaction_data.csv', 'rb').read(),
                file_name='transaction_data.csv',
                mime='text/csv'
            )
