import streamlit as st
import pandas as pd
import psycopg2
from psycopg2 import OperationalError

def create_connection():
    """Create a database connection."""
    try:
        conn = psycopg2.connect(
            dbname=st.secrets['database']['dbname'],
            user=st.secrets['database']['user'],
            password=st.secrets['database']['password'],
            host=st.secrets['database']['host'],
            port=st.secrets['database']['port']
        )
        return conn
    except OperationalError as e:
        st.error(f"Error connecting to the database: {e}")
        return None

def load_data_transaction():
    """Load transaction data from database."""
    conn = create_connection()
    if conn is not None:
        try:
            query = "SELECT * FROM transaksi"
            transaction_data = pd.read_sql(query, conn)
            transaction_data['tanggal'] = pd.to_datetime(transaction_data['tanggal'])
            return transaction_data
        except Exception as e:
            st.error(f"Error loading data: {e}")
            return None
        finally:
            conn.close()
    else:
        return None
