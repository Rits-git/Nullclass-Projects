import pandas as pd
import plotly.express as px
from datetime import datetime
import pytz

# Sample DataFrame loading (replace with actual data source)
df = pd.read_csv('D:/nullclass/job_preference_dataset.csv')

# Filter data
filtered_df = df[
    (df['WorkType'] == 'Intern') &
    (df['Latitude'] < 10) &
    (df['County'].str[0].isin(['A', 'B', 'C', 'D'])) &
    (df['JobTitle'].str.len() <= 10) &
    (df['CompanySize'] < 50000)
]

# Get current time in IST
ist = pytz.timezone('Asia/Kolkata')
current_time = datetime.now(ist).time()

# Define time window
start_time = datetime.strptime('15:00', '%H:%M').time()
end_time = datetime.strptime('17:00', '%H:%M').time()

# Check if current time is within the window
if start_time <= current_time <= end_time:
    fig = px.bar(filtered_df, x='Preference', y='work_type', title='Preference vs Work Type for Interns')
    fig.show()
else:
    print("Chart is only available between 3 PM and 5 PM IST.")
