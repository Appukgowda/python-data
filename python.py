import pandas as pd
import geopandas as gpd
from shapely.geometry import box
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

# Reads the dataset into a DataFrame
file_path = 'Growlocations.csv' 
df = pd.read_csv(file_path)

# Interchange latitude and longitude columns
df['temp'] = df['Latitude']
df['Latitude'] = df['Longitude']
df['Longitude'] = df['temp']
df.drop(columns=['temp'], inplace=True)

# Save the updated DataFrame back to a new CSV file
output_file_path = 'updated_file.csv'  
df.to_csv(output_file_path, index=False)

# Remove bad values (outside the bounding box)
bounding_box = {'lon_min': -10.592, 'lon_max': 1.6848, 'lat_min': 50.681, 'lat_max': 57.985}

df = df[
    (bounding_box['lon_max'] >= df['Longitude']) & 
    (df['Longitude'] >= bounding_box['lon_min']) & 
    (bounding_box['lat_max'] >= df['Latitude']) & 
    (df['Latitude'] >= bounding_box['lat_min'])
]

# Create a GeoDataFrame from the DataFrame
geometry = gpd.points_from_xy(df['Longitude'], df['Latitude'])
gdf = gpd.GeoDataFrame(df, geometry=geometry, crs='EPSG:4326')

# Create a bounding box geometry
bbox_geometry = box(bounding_box['lon_min'], bounding_box['lat_min'], bounding_box['lon_max'], bounding_box['lat_max'])

# Create a GeoSeries containing the bounding box
clipped_map = gpd.GeoSeries(bbox_geometry)

# Plotting the data on the map
fig, ax = plt.subplots()

# Add map image
img = plt.imread('map7.png')
ax.imshow(img, extent=[bounding_box['lon_min'], bounding_box['lon_max'], bounding_box['lat_min'], bounding_box['lat_max']])

# Plot the sensor locations
gdf.plot(ax=ax, color='blue', marker='o')

# Set labels and title
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
ax.set_title('Plotting the Grow Data')

# Show the plot
plt.show()
