# Import the necessary library

import rasterio
import os
import numpy as np
import pandas as pd

# Creating an empty dataframe to store the value 

table = pd.DataFrame(0, np.arange(1, 11689), columns = ['Date', 'Rainfall(mm)'])    # 0 is a dummy value to fill the columns primarily and the preset index number 1 to 1169 is equal the number of raster (or, you can say the number of row under both the columns, where the value from each raster will be input)

# Creating a 'for loop' to loop through, and read the information from all the rasters

i = 0     # Setting the counter to run the 'loop' from the very first raster to the 11688th

for files in os.listdir(r'C:\Users\lenovo\Desktop\CHIRPS-Data') :    # os library can read the files which are located in a folder
    
    if files [-4:] == '.tif' :     # This will avoid reading the file other than the ones with .tif format
    
        i = i+1
        
        dataset = rasterio.open(r'C:\Users\lenovo\Desktop\CHIRPS-Data' +'\\'+ files)
        
        # Putting the point on which to generate the time-series
        
        x, y = (23.616260, 90.521500)    # Let this lat long is for Station-01
        row, col = dataset.index(x, y)    # To retrieve the index of the provided lat long from the raster
        data_array = dataset.read(1)
        
        # Copying the date from the rasters to the 'date' column of the previously created 'table'
        
        table['Date'].loc[i] = files[:-4]
        
        # Fill the rainfall from the rasters to the 'Rainfall(mm)' column of the previously created 'table'
        
        table['Rainfall(mm)'].loc[i] = data_array[int(row), int(col)]
        
        # Export the 'table' into a .csv file
        
        table.to_csv(r'C:\Users\lenovo\Desktop\GEO-SPY\Station-01.csv')    # Put the name of the .csv file and the path to save
        