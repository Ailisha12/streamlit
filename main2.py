import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt



uploaded_file = st.file_uploader("Загрузите файл CSV", type="csv")
if uploaded_file is not None:

    data = pd.read_csv(uploaded_file)
else:
    st.warning("Загрузите файл CSV")

if 'data' in locals():
    months = data['month'].str.split('-').str[-1].drop_duplicates().tolist()

    year = [int(month.split('-')[0]) for month in data['month']]
    selected_year = st.selectbox("Выберите год",  options=range(min(year), max(year)+1), index=0)
    selected_state = st.selectbox("Выберите штат", data['state'].unique())

    filtered_data = data[(data['state'] == selected_state) &
                       (pd.to_datetime(data['month']).dt.year == selected_year)]

    filtered_data  = data[pd.to_datetime(data['month']).dt.year == selected_year]
    top_states = filtered_data.groupby('state')['totals'].sum().nlargest(10)


    fig, ax = plt.subplots(figsize=(10, 8))
    top_states.plot.pie(autopct='%1.1f%%', ax=ax)
    ax.set_ylabel('')
    st.pyplot(fig)

    csv = data.to_csv(index=False)
    st.download_button(
        label="Скачать CSV",
        data=csv,
        file_name='csv_data.csv',
        mime='text/csv',
    )