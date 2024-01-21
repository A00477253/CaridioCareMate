# home.py
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def show_home_page():
    # URL of the dataset
    url = 'C:\\Users\\91866\\health.csv'

    # Load the dataset
    df = pd.read_csv(url)

    # Round the age to whole digits
    df['age'] = (df['age'] / 365).round().astype(int)

    # Add a column for the sum of risk factors
    df['risk_factor_sum'] = df['cholesterol'] + df['gluc'] + df['smoke'] + df['alco']

    def plot_binned_bar(df, column, bins):
        df_copy = df.copy()
        if column != 'risk_factor_sum':
            df_copy['binned'], bin_edges = pd.cut(df_copy[column], bins=bins, retbins=True, right=False, labels=False)
            df_copy.dropna(subset=['binned'], inplace=True)
            df_copy['binned'] = df_copy['binned'].astype(int)
            bin_labels = [f"{int(bin_edges[i])} - {int(bin_edges[i+1])}" for i in range(len(bin_edges)-1)]
            df_copy['binned'] = df_copy['binned'].apply(lambda x: bin_labels[x])
            grouped = df_copy.groupby('binned')['Cardiac_Attack_Chances'].mean().reset_index()
            grouped['binned'] = pd.Categorical(grouped['binned'], categories=bin_labels, ordered=True)
            grouped = grouped.sort_values('binned')
        else:
            df_copy['binned'] = df_copy['risk_factor_sum']
            grouped = df_copy.groupby('binned')['Cardiac_Attack_Chances'].mean().reset_index()
            grouped = grouped.sort_values('binned')
        return grouped

    # Streamlit app
    st.title('Cardiac Attack Chances Analysis')

    # Dropdown to select the column
    option = st.selectbox(
        'Which column do you want to analyze?',
        ('age', 'weight', 'risk_factor_sum')
    )

    # Define bins based on selection
    if option == 'age':
        bins = [20, 40, 60, 80, 100]
    elif option == 'weight':
        bins = np.linspace(df[option].min(), df[option].max(), 10)
    else:
        bins = None

    grouped_data = plot_binned_bar(df, option, bins)

    # Bar Chart Visualization
    st.bar_chart(grouped_data.set_index('binned'))

    # Pie Chart Visualization
    if option in ['age', 'weight', 'risk_factor_sum']:
        pie_data = grouped_data.set_index('binned')['Cardiac_Attack_Chances']
        plt.figure(figsize=(8, 8))
        plt.pie(pie_data, labels=pie_data.index, autopct='%1.1f%%')
        plt.title(f'Distribution for {option}')
        st.pyplot(plt)

    # Explanation for risk factor sum
    if option == 'risk_factor_sum':
        st.write("The 'risk_factor_sum' is calculated as the sum of the following factors:")
        st.write("- Cholesterol (cholesterol)")
        st.write("- Glucose (gluc)")
        st.write("- Smoking (smoke)")
        st.write("- Alcohol consumption (alco)")
        st.write("Each factor is added to get the total risk factor sum.")
