import streamlit as st
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from pylab import bone, pcolor, colorbar, plot, show

def plot_som_distance_map(som):
    """Plot SOM distance map"""
    plt.figure(figsize=(20, 10))
    bone()
    pcolor(som.distance_map().T)  # distance map as background
    colorbar()
    # st.subheader('Self-Organizing Map (SOM) Distance Map')
    # st.pyplot(plt)

def plot_som_clustering(som, scaled_data):
    """Plot SOM clustering"""
    plt.figure(figsize=(20, 10))
    bone()
    pcolor(som.distance_map().T)  # distance map as background
    colorbar()
    markers = ['o', 's']
    colors = ['r', 'g']
    for i, x in enumerate(scaled_data):
        w = som.winner(x)
        plt.plot(w[0] + 0.5, w[1] + 0.5, markers[0], markeredgecolor=colors[0], markerfacecolor='None', markersize=10, markeredgewidth=2)
    # st.subheader('SOM Clustering')
    # st.pyplot(plt)

def plot_kmeans_clustering(som, scaled_data):
    """Plot K-Means clustering using SOM results"""
    markers = ['o', 's']
    colors = ['r', 'g']
    winners = [som.winner(x) for x in scaled_data]
    for i, w in enumerate(winners):
        plt.plot(w[0] + 0.5, w[1] + 0.5, markers[i % len(markers)], markeredgecolor=colors[i % len(colors)], markerfacecolor='None', markersize=10, markeredgewidth=2)
    # st.subheader('K-Means Clustering using SOM results')
    # st.pyplot(plt)

def plot_fraud_percentage(transaction_data, kmeans, scaled_data):
    """Plot fraud percentage as a pie chart"""
    total_data = len(transaction_data)
    fraud_data = transaction_data[kmeans.labels_ == 1]
    nfraud_data = transaction_data[kmeans.labels_ == 0]

    fraud_percentage = len(fraud_data) / total_data * 100
    non_fraud_percentage = len(nfraud_data) / total_data * 100

    # Add pie chart for overall fraud percentage
    labels1 = ['Fraud', 'Non-Fraud']
    values1 = [fraud_percentage, non_fraud_percentage]
    fig = go.Figure(data=[go.Pie(labels=labels1, values=values1)])
    st.subheader('5. Overall Fraud Percentage')
    st.plotly_chart(fig, use_container_width=True)
    st.write('Total Data:', len(transaction_data))
    st.write('Total Non Fraud:', len(nfraud_data))
    st.write('Total Fraud:', len(fraud_data))

    # Add pie chart for jenis transaksi beli and jual
    beli_fraud_data = fraud_data[fraud_data['jenis_transaksi'] == 'Beli']
    jual_fraud_data = fraud_data[fraud_data['jenis_transaksi'] == 'Jual']

    beli_fraud_percentage = len(beli_fraud_data) / len(fraud_data) * 100
    jual_fraud_percentage = len(jual_fraud_data) / len(fraud_data) * 100

    labels2 = ['Beli', 'Jual']
    values2 = [beli_fraud_percentage, jual_fraud_percentage]
    fig = go.Figure(data=[go.Pie(labels=labels2, values=values2)])
    st.subheader('6. Fraud Percentage by Jenis Transaksi')
    st.plotly_chart(fig, use_container_width=True)
    st.write('Total Beli Fraud:', len(beli_fraud_data))
    st.write('Total Jual Fraud:', len(jual_fraud_data))

    # Add pie chart for jenis transaksi beli and jual
    beli_fraud_percentage = beli_fraud_data['jenis_mata_uang'].value_counts(normalize=True).mul(100).round(1)
    jual_fraud_percentage = jual_fraud_data['jenis_mata_uang'].value_counts(normalize=True).mul(100).round(1)

    # Add table for fraud amount by jenis mata uang for beli and jual
    beli_fraud_mata_uang = beli_fraud_data['jenis_mata_uang'].value_counts()
    jual_fraud_mata_uang = jual_fraud_data['jenis_mata_uang'].value_counts()

    fig = go.Figure(data=[go.Pie(labels=beli_fraud_percentage.index, values=beli_fraud_percentage.values)])
    st.subheader('7. Fraud Percentage by Jenis Mata Uang for Beli')
    st.plotly_chart(fig, use_container_width=True)

    fig = go.Figure(data=[go.Pie(labels=jual_fraud_percentage.index, values=jual_fraud_percentage.values)])
    st.subheader('8. Fraud Percentage by Jenis Mata Uang for Jual')
    st.plotly_chart(fig, use_container_width=True)

    fig = go.Figure(data=[go.Table(
        header=dict(values=['Jenis Mata Uang', 'Beli Fraud', 'Jual Fraud']),
        cells=dict(values=[beli_fraud_mata_uang.index, beli_fraud_mata_uang.values, jual_fraud_mata_uang.values])
    )])
    st.subheader('9. Fraud Amount by Jenis Mata Uang for Beli and Jual')
    st.plotly_chart(fig, use_container_width=True)
