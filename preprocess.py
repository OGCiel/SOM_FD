import streamlit as st
import pandas as pd
from sklearn import preprocessing
from sklearn.cluster import KMeans
from minisom import MiniSom

def load_data(uploaded_file):
    """Load transaction data from uploaded file"""
    try:
        transaction_data = pd.read_csv(uploaded_file)
        transaction_data['tanggal'] = pd.to_datetime(transaction_data['tanggal'])
        return transaction_data
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

def preprocess_data(transaction_data):
    """Preprocess data by dropping columns and normalizing"""
    preprocessed_data = transaction_data.copy()
    to_drop = ['tanggal', 'id_nasabah', 'jenis_mata_uang', 'jenis_transaksi', 'nama']
    preprocessed_data = transaction_data.drop(to_drop, axis=1)
    scaler = preprocessing.MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(preprocessed_data)
    return scaled_data

def train_som(scaled_data, num_iteration=1000, init_sigma=1.0, init_learning_rate=0.1, verbose=True):
    """Train Self-Organizing Map (SOM)"""
    som = MiniSom(10, 10, input_len=scaled_data.shape[1], sigma=init_sigma, learning_rate=init_learning_rate)
    som.random_weights_init(scaled_data)
    for i in range(num_iteration):
        # Update sigma and learning rate
        sigma = init_sigma * (1 - i / num_iteration)
        learning_rate = init_learning_rate * (1 - i / num_iteration)
        som.sigma = sigma
        som.learning_rate = learning_rate
        som.train_random(scaled_data, 1)
        if verbose and (i % (num_iteration // 10) == 0):
            st.write(f"Iteration {i+1}/{num_iteration}", flush=True)  # Use st.write with flush=True
            st.write(init_sigma)
            st.write(init_learning_rate)
            st.write(sigma)
            st.write(learning_rate)
    return som

def train_kmeans(som, scaled_data):
    """Train K-Means clustering using SOM results"""
    # Get the winning neurons for each data point
    winners = [som.winner(x) for x in scaled_data]

    # Initialize KMeans with the initial centroids
    kmeans = KMeans(n_clusters=2)
    kmeans.fit(winners)

    # Get the labels
    labels = kmeans.labels_
    return kmeans, labels

def print_som_training_process(scaled_data, num_iteration=1000, init_sigma=1.0, init_learning_rate=0.1):
    """Print SOM training process in a detailed table form"""
    som = MiniSom(10, 10, input_len=scaled_data.shape[1], sigma=init_sigma, learning_rate=init_learning_rate)
    som.random_weights_init(scaled_data)

    # Create a table to store the training process
    table_data = []

    for i in range(num_iteration):
        # Update sigma and learning rate
        sigma = init_sigma * (1 - i / num_iteration)
        learning_rate = init_learning_rate * (1 - i / num_iteration)
        som.sigma = sigma
        som.learning_rate = learning_rate

        # Train the SOM for one iteration
        som.train_random(scaled_data, 1)

        # Get the winning neurons and new weights
        winners = [som.winner(x) for x in scaled_data]
        new_weights = som.get_weights()

        # Create a table row for this iteration
        row_data = {
            'Iteration': i+1,
            'Data': scaled_data.tolist(),
            'Winning Neurons': winners,
            'Sigma': sigma,
            'Learning Rate': learning_rate,
            'New Weights': new_weights.tolist()
        }
        table_data.append(row_data)

    # Create a Pandas DataFrame from the table data
    df = pd.DataFrame(table_data)

    # Print the table
    st.write(df)
