import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import pytz  # For IST timezone
import folium  # For interactive map
from folium.plugins import MarkerCluster  # Optional: cluster markers if many

# Step 1: Time Check (3 PM to 6 PM IST)
def is_time_allowed():
    ist = pytz.timezone('Asia/Kolkata')
    current_time = datetime.now(ist)
    hour = current_time.hour
    return 15 <= hour < 18  # 3 PM (15) to 6 PM (18) IST

if not is_time_allowed():
    print("Dashboard unavailable. This graph is only visible between 3 PM and 6 PM IST.")
    exit()

print("Time check passed. Generating dashboard...")

# Step 2: Generate Sample Data (Replace with your real data loading, e.g., pd.read_csv('jobs.csv'))
data = {
    'Job_Title': ['Data Analyst', 'Developer', 'Director of Engineering', 'Data Scientist'],
    'Qualification': ['B.tech,M.tech,PhD', 'B.tech,M.tech,PhD', 'B.tech,M.tech,PhD', 'B.tech,M.tech,PhD'],
    'Work_Type': ['Full time', 'Full time', 'Full time', 'Full time'],
    'Country': ['Nigeria', 'South Africa', 'Kenya', 'Egypt'],  # African countries only
    'Preference': ['Male', 'Male', 'Male', 'Male'],
    'Company_Size': [85000, 120000, 95000, 110000],  # All > 80000
    'Contact_Person': ['Ahmed', 'Alice', 'Aisha', 'Alex'],
    'Job_Portal': ['indeed', 'indeed', 'indeed', 'indeed'],
    'Latitude': [9.0579, -25.7479, 1.2921, 30.0444],  # Sample lat for African locations
    'Longitude': [8.6753, 28.2361, 36.8219, 31.2357]   # Sample lon
}
df = pd.DataFrame(data)

# Step 3: Apply Filters
african_countries = ['Nigeria', 'South Africa', 'Kenya', 'Egypt', 'Ghana', 'Morocco', 'Algeria', 'Ethiopia']  # Expand as needed
filtered_df = df[
    (df['Qualification'] == 'B.tech,M.tech,PhD') &
    (df['Work_Type'] == 'Full time') &
    (df['Country'].isin(african_countries)) &
    (df['Job_Title'].str.startswith('D')) &
    (df['Preference'] == 'Male') &
    (df['Company_Size'] > 80000) &
    (df['Contact_Person'].str.startswith('A')) &
    (df['Job_Portal'] == 'indeed')
]

print(f"Filtered data shape: {filtered_df.shape}")
if filtered_df.empty:
    print("No data matches the criteria.")
    exit()

# Step 4: Create Bar Chart (Job Counts by Country)
plt.figure(figsize=(10, 6))
sns.countplot(data=filtered_df, x='Country', palette='viridis')
plt.title('Job Opportunities in African Countries\n(Qualification: B.Tech/M.Tech/PhD, Full Time, Male Preference, etc.)')
plt.xlabel('Country')
plt.ylabel('Number of Jobs')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('job_chart.png')  # Save as image
plt.show()  # Display chart

# Step 5: Create Interactive Map with Clickable Lat/Lon
map_center = [filtered_df['Latitude'].mean(), filtered_df['Longitude'].mean()]  # Center on average location
m = folium.Map(location=map_center, zoom_start=4)  # Africa-wide view

# Add markers for each job (click to open popup with details)
marker_cluster = MarkerCluster().add_to(m)
for idx, row in filtered_df.iterrows():
    folium.Marker(
        location=[row['Latitude'], row['Longitude']],
        popup=f"""
        <b>Job Title:</b> {row['Job_Title']}<br>
        <b>Country:</b> {row['Country']}<br>
        <b>Contact:</b> {row['Contact_Person']}<br>
        <b>Company Size:</b> {row['Company_Size']}<br>
        <b>Portal:</b> {row['Job_Portal']}
        """,
        tooltip=f"Click for details: {row['Job_Title']}",
        icon=folium.Icon(color='blue', icon='info-sign')  # Custom icon
    ).add_to(marker_cluster)

# Save and open map
m.save('job_map.html')
print("Map saved as 'job_map.html'. Open in browser to interact (click markers for location/details).")

# Optional: If integrating into a dashboard (e.g., Streamlit or Dash), you can embed this.
