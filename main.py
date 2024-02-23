import streamlit as st  
import pandas as pd
import matplotlib.pyplot as plt

st.title('Дашборд')

data = pd.read_csv('nics-firearm-background-checks.csv')
data['month1'] = data['month'].str.split('-').str[-1]
data['year'] = data['month'].str.split('-').str[0]
year_selectbox = st.selectbox('Выберите год', data['year'].unique())
st.title('Выберите месяц(ы)')
select_all_months = st.checkbox("Выбрать все месяцы")

month_checkboxes = {month: st.checkbox(month, value=(select_all_months and month in data['month1'].unique())) for month in data['month1'].unique()}
state_selectbox = st.selectbox('Выберите штат', data['state'].unique())

selected_months = [month for month, selected in month_checkboxes.items() if selected]
df = data[(data['month1'].isin(selected_months)) & (data['year'] == year_selectbox) & (data['state'] == state_selectbox)]

st.write(df)

csv = df.to_csv(index=False)
st.download_button(
    label="Скачать CSV",
    data=csv,
    file_name='csv_data.csv',
    mime='text/csv',
)

chart_data = df.groupby('month1')['totals'].sum()
# filtered_data = chart_data[chart_data > chart_data.sum() * 0.01] 
fig, ax = plt.subplots()
ax.pie(chart_data, labels=chart_data.index, autopct='%1.1f%%')
st.pyplot(fig)
