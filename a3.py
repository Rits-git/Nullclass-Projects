import pandas as pd
import plotly.express as px
from datetime import datetime, time
import pytz

# Sample DataFrame 'df' with columns:
# ['Role', 'JobTitle', 'GenderPreference', 'Qualification', 'PostingDate', 'Company', 'Country', 'Latitude']

# Step 1: Filter data
def filter_data(df):
    # Convert PostingDate to datetime
    df['PostingDate'] = pd.to_datetime(df['PostingDate'], format='%d/%m/%Y')

    # Define date range
    start_date = pd.to_datetime('01/01/2023', format='%d/%m/%Y')
    end_date = pd.to_datetime('06/01/2023', format='%d/%m/%Y')

    # List of Asian countries (example subset)
    asian_countries = ['India', 'China', 'Japan', 'South Korea', 'Indonesia', 'Pakistan', 'Bangladesh', 'Philippines', 'Vietnam', 'Thailand', 'Malaysia', 'Singapore', 'Nepal', 'Sri Lanka', 'Myanmar', 'Cambodia', 'Laos', 'Mongolia', 'Taiwan', 'Hong Kong']

    # Apply filters
    filtered_df = df[
        (df['Role'] == 'Data Engineer') &
        (df['JobTitle'] == 'Data Scientist') &
        (df['GenderPreference'].str.lower() == 'female') &
        (df['Qualification'] == 'B.Tech') &
        (df['PostingDate'] >= start_date) &
        (df['PostingDate'] <= end_date) &
        (~df['Country'].isin(asian_countries)) &
        (~df['Country'].str.startswith('C')) &
        (df['Latitude'] >= 10)
    ]

    return filtered_df

# Step 2: Aggregate top 10 companies
def get_top_companies(filtered_df):
    company_counts = filtered_df.groupby('Company').size().reset_index(name='Count')
    top_companies = company_counts.sort_values(by='Count', ascending=False).head(10)
    return top_companies

# Step 3: Check current IST time
def is_time_between(start_time, end_time, check_time=None):
    check_time = check_time or datetime.now(pytz.timezone('Asia/Kolkata')).time()
    if start_time < end_time:
        return start_time <= check_time <= end_time
    else:  # Over midnight
        return check_time >= start_time or check_time <= end_time

# Step 4: Plot chart
def plot_chart(top_companies):
    fig = px.bar(top_companies, x='Company', y='Count',
                title='Top 10 Companies with Max Data Engineer Role & Data Scientist Job Title (Female, B.Tech)',
                labels={'Count': 'Number of Job Postings'})
    fig.show()

# Main function to run
def main(df):
    if is_time_between(time(15, 0), time(17, 0)):  # 3 PM to 5 PM IST
        filtered_df = filter_data(df)
        top_companies = get_top_companies(filtered_df)
        if not top_companies.empty:
            plot_chart(top_companies)
        else:
            print("No data available for the given filters.")
    else:
        print("Chart is only available between 3 PM and 5 PM IST.")

# Example usage:
df = pd.read_csv('D:/nullclass/top10_data_roles.csv') 
main(df)
