# Importing the necessary library

import geopandas as gpd            # to read the point shapefile containing all the data from multiple stations
import os                          # to identify the individual rasters name while iterating over them
import rasterio                    # to read the rasters
import scipy.sparse as sparse      # to get the data into a coordinate matrix from the variable 'data_array'
import pandas as pd                # to create dataframe 
import numpy as np                 # to create array

stations = gpd.read_file(r'C:\Users\lenovo\Desktop\Stations.shp')

# Ascribing the geometry values (x, y) of the shapefile into newly created lat, lon columns of the existing dataframe

stations['Lat'] = stations['geometry'].x
stations['Lon'] = stations['geometry'].y  

# Creating a matrix (empty dataframe) to store the data from the following iterations for the variable 'data_array_sparse'

Matrix = pd.DataFrame()

# Creating a table (empty dataframe) to store the final dataset to be extracted

Table = pd.DataFrame(index = np.arange(0, 1))

# Iterate through the rasters and save the data as individual arrays of a matrix

for files in os.listdir(r'C:\Users\lenovo\Desktop\CHIRPS-Raster'):
    if files [-4: ] == '.tif':      # to identify only the .tif files from the destination folder
         dataset = rasterio.open(r'C:\Users\lenovo\Desktop\CHIRPS-Raster'+'\\'+files)
         data_array = dataset.read(1)      # to primarily store the data from each of the raster as an array
         data_array_sparse = sparse.coo_matrix(data_array, shape = (60, 60))     # shape will of the same as the shape of the variable 'data_array'
         date = files[ :-4]       # to keep track of the day/date which is passing 
         
         # Creating the column for the empty dataframe 'Matrix'
         Matrix[date] = data_array_sparse.toarray().tolist()
         print('Processing is done for the raster : ' + files[ :-4])      # just to visualize the processing of taking the actual date into the 'date' column in console
         
# Iterate through the stations and get the corresponding row and col for the related x, y coordinates       
         
for index, row in stations.iterrows():
    station_name = str(row['Name_of_the_station'])
    lat = float(row['Lat'])
    lon = float(row['Lon'])
    (x, y) = (lat, lon)
    row, col = dataset.index(x, y)
    print('Processing for : ' + station_name)
    
# Pick the rainfall value from each stored raster array and record it into the previously created dataframe 'Table'

    for records_date in Matrix.columns.tolist():
        a = Matrix[records_date]
        rainfall = a.loc[int(row)][int(col)]
    
        # Creating the column for the empty dataframe 'Table'
        Table['records_date'] = rainfall
        transpose_matx = Table.T 
    
        # Renaming the column of the previously created 'Table'
        transpose_matx.rename(columns = {0: 'Rainfall(mm)'}, inplace = True)
    
    transpose_matx.to_csv(r'C:\Users\lenovo\Desktop\Extracted-Time-Series'+ '\\'+ station_name+ '.csv')
    

    
    
    
    
    
    
    
    