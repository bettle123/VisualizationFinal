'''
@Author: Su Ming Yi
@Date: 12/04/2018
@Goal: 
    know when the airburst happen by analysis the statistics of each timestep vairable "tev"
    statistics: average, median, std
How to run it:
    C:\python\Lib\site-packages\VTK\bin\vtkpython.exe task2_abnormal_tev.py

'''


import vtk
import vtk.util.numpy_support as VN
import numpy as np
import sys,os
import csv

def main():
    path = "yC31/";
    # the variable name of data array which we used to analyze
    daryName = "tev";
    files = os.listdir(path);
    # declare empty list first, and for every timestep statistics inside.
    #for i in range(0, 10):
    #for i in range(0, len(files)):
    for i in range(74, 75):
        filename = path+files[i];
        print(filename);
        
        # data reader
        reader = vtk.vtkXMLImageDataReader();
        reader.SetFileName(filename);
        reader.Update();
        # specify the data array in the file to process
        reader.GetOutput().GetPointData().SetActiveAttribute(daryName, 0);
        # convert the data array to numpy array and get the min and maximum value
        dary = VN.vtk_to_numpy(reader.GetOutput().GetPointData().GetScalars(daryName));
        dMax = np.amax(dary);
        dMin = np.amin(dary);
        dstd = np.std(dary);
        dsize = np.size(dary);
        dRange = dMax - dMin;
        dMean = np.mean(dary);
        dMedian = np.median(dary);
        print("Data array median: ", dMedian);
        print("Data array mean: ", dMean);
        print("Data array std: ", dstd);
        print("Data array size: ", dsize);
        print("Data array max: ", dMax);
        print("Data array min: ", dMin);
        print("Data array range: ", dRange);
if __name__ == '__main__':
    main();    
