import pandas as pd
import plotly.express as px
from datetime import datetime
import pytz

# Load your dataset
df = pd.read_csv('D:/nullclass/sample_mechanical_engineers.csv')

# Define list of Asian countries (example subset)
asian_countries = [
    'India', 'China', 'Japan', 'South Korea', 'Indonesia', 'Thailand', 'Vietnam',
    'Malaysia', 'Singapore', 'Philippines', 'Bangladesh', 'Pakistan', 'Sri Lanka',
    'Nepal', 'Bhutan', 'Myanmar', 'Cambodia', 'Laos', 'Mongolia', 'Taiwan'
]

# Filter dataset
filtered_df = df[
    (df['Company Size'] < 50000) &
    (df['Job Title'].str.lower() == 'mechanical engineer') &
    (df['Experience (Years)'] > 5) &
    (df['Country'].isin(asian_countries)) &
    (df['AnnualSalary'] > 50000) &
    (df['Work Type'].isin(['Part Time', 'Full Time'])) &
    (df['Gender Preference'].str.lower() == 'male') &
    (df['Source'].str.lower() == 'idealist')
]

# Get current time in IST
ist = pytz.timezone('Asia/Kolkata')
current_time = datetime.now(ist).time()

# Define time window
start_time = datetime.strptime('15:00', '%H:%M').time()
end_time = datetime.strptime('17:00', '%H:%M').time()

# Show chart only if current time is between 3 PM and 5 PM IST
if start_time <= current_time <= end_time:
    fig = px.bar(filtered_df, x='company_name', y='company_size',
                title='Company Size vs Company Name for Mechanical Engineers',
                labels={'company_name': 'Company Name', 'company_size': 'Company Size'})
    fig.update_layout(xaxis_tickangle=-45)
    fig.show()
else:
    print("Chart is only available between 3 PM and 5 PM IST.")
