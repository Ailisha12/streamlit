import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
import plotly.express as px


data = pd.read_csv("nics-firearm-background-checks.csv")


st.title('Первый график')
st.title('По каждому штату за все месяцы')
data['month'] = pd.to_datetime(data['month'])
data['year'] = data['month'].dt.year
grouped_data = data.groupby(['year', 'state'])['totals'].sum().reset_index()
max_year = grouped_data['year'].max()
filtered_data = grouped_data[grouped_data['year'] == max_year]
filtered_data = filtered_data[filtered_data['totals'] >  100000]

fig = px.bar(filtered_data, x='state', y='totals', color='state')
fig.update_layout(width=600, height=400)
st.write(fig)



st.title('Второй график')
st.title('Возврат пистолетов продавцу по штатам (в процентах более трех)')
chart_data = data.groupby('state')['return_to_seller_handgun'].sum()
filtered_data = chart_data[chart_data > chart_data.sum() * 0.03] 
fig, ax = plt.subplots()
ax.pie(filtered_data, labels=filtered_data.index, autopct='%1.1f%%')
st.pyplot(fig)

st.title('Третий график')
st.title('Выданные разрешения по штатам')
chart_data = data.groupby(['state'])['permit'].sum()
st.line_chart(chart_data)


st.title('Четвертый график')
st.title('Выкуп оружия по штатам')
data['total_redemption'] = data['redemption_handgun'] + data['redemption_long_gun'] + data['redemption_other']
grouped_data = data.groupby('state')['total_redemption'].sum().reset_index()
top_states = grouped_data.nlargest(10, 'total_redemption')
fig = px.pie(top_states, values='total_redemption', names='state')
st.plotly_chart(fig)


st.title('Пятый график')
st.title('Во всех штатах')
chart_data = data.groupby('state')['totals'].sum().reset_index()
chart = alt.Chart(chart_data).mark_bar().encode(
    x='state',
    y='totals',
    tooltip=['state', 'totals']
).properties(
    width=600,
    height=400
)
st.write(chart)
