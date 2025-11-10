
# Streamlit dashboard for University Student Data
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

st.set_page_config(page_title='University Dashboard', layout='wide')

@st.cache_data
def load_data():
    df = pd.read_csv('/mnt/data/university_student_data.csv')
    df['Year'] = df['Year'].astype(int)
    return df

df = load_data()

st.title('University — Student Admission, Retention & Satisfaction Dashboard')

# Filters
cols = st.columns([1,1,1])
with cols[0]:
    years = sorted(df['Year'].unique())
    year = st.selectbox('Year', options=['All'] + years, index=0)
with cols[1]:
    terms = sorted(df['Term'].unique())
    term = st.selectbox('Term', options=['All'] + terms, index=0)
with cols[2]:
    dept = st.selectbox('Department (for enrollment)', options=['All', 'Engineering', 'Business', 'Arts', 'Science'])

# Filter data
d = df.copy()
if year != 'All':
    d = d[d['Year'] == int(year)]
if term != 'All':
    d = d[d['Term'] == term]

# KPIs
col1, col2, col3, col4 = st.columns(4)
col1.metric('Avg Retention (%)', f"{d['Retention Rate (%)'].mean():.2f}")
col2.metric('Avg Satisfaction (%)', f"{d['Student Satisfaction (%)'].mean():.2f}")
col3.metric('Avg Applications', f"{d['Applications'].mean():.0f}")
col4.metric('Avg Enrolled', f"{d['Enrolled'].mean():.0f}")

st.markdown('---')

# Plots
st.header('Trends')

# Retention over time
fig1, ax1 = plt.subplots(figsize=(8,4))
ydata = d.groupby('Year')['Retention Rate (%)'].mean().reset_index()
ax1.plot(ydata['Year'], ydata['Retention Rate (%)'], marker='o')
ax1.set_xlabel('Year')
ax1.set_ylabel('Retention Rate (%)')
ax1.xaxis.set_major_locator(MaxNLocator(integer=True))
ax1.grid(True, linestyle='--', linewidth=0.4)
st.pyplot(fig1)

# Satisfaction over time
fig2, ax2 = plt.subplots(figsize=(8,4))
y2 = d.groupby('Year')['Student Satisfaction (%)'].mean().reset_index()
ax2.plot(y2['Year'], y2['Student Satisfaction (%)'], marker='o')
ax2.set_xlabel('Year')
ax2.set_ylabel('Student Satisfaction (%)')
ax2.xaxis.set_major_locator(MaxNLocator(integer=True))
ax2.grid(True, linestyle='--', linewidth=0.4)
st.pyplot(fig2)

st.header('Term comparison (Spring vs Fall)')
# Comparison plot for retention by term per year (show current filters)
fig3, ax3 = plt.subplots(figsize=(10,5))
pivot = d.pivot_table(index='Year', columns='Term', values='Retention Rate (%)', aggfunc='mean').fillna(0)
years = pivot.index.values
x = range(len(years))
width = 0.35
spring = pivot.get('Spring', pd.Series([0]*len(years), index=pivot.index)).values
fall = pivot.get('Fall', pd.Series([0]*len(years), index=pivot.index)).values
ax3.bar([i - width/2 for i in x], spring, width, label='Spring')
ax3.bar([i + width/2 for i in x], fall, width, label='Fall')
ax3.set_xticks(x)
ax3.set_xticklabels(years)
ax3.set_xlabel('Year')
ax3.set_ylabel('Retention Rate (%)')
ax3.legend()
ax3.grid(axis='y', linestyle='--', linewidth=0.4)
st.pyplot(fig3)

# Department enrollment table (if requested)
if dept != 'All':
    col_name = "{} Enrolled".format(dept)
    if col_name in d.columns:
        st.header('Enrollment — {}'.format(dept))
        st.table(d[['Year','Term', col_name]].groupby(['Year','Term']).sum().reset_index())
    else:
        st.info('No department-specific enrollment column found in dataset.')

st.markdown('---')
st.write('Files included: app.py, requirements.txt, README.md, Summary_Findings_Aldair_Escobar.docx. Follow the README to deploy to Streamlit Cloud.')
