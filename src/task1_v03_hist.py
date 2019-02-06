'''
@Author: Su Ming Yi
@Date: 12/04/2018
@Goal: 
    Get the histogram of one timestep
How to run it:
    C:\python\Lib\site-packages\VTK\bin\vtkpython.exe task1_v03_hist.py

'''


import vtk
import vtk.util.numpy_support as VN
import numpy as np
import sys,os
import csv
import matplotlib.pyplot as plt

def main():
    path = "yC31/";
    # the variable name of data array which we used to analyze
    daryName = "v03";
    files = os.listdir(path);
    #for i in range(0, 10):
    for i in range(0, len(files)):
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
        
        plt.hist(dary, color = "blue", bins = 20)
        titlename = "Histogram of v03 timestep " +files[i][22:27]
        plt.title(titlename)
        savefilename = "plots/hists/v03_t_"+files[i][22:27]+".png";
        plt.savefig(savefilename);
    
    '''
    x = [];
    y = [];
    for i in range(0, 10):
        x.append(i);
        y.append(i*3);
        if(i>=5):
            y.append(i*3);
            
        
    plt.hist(y)  # arguments are passed to np.histogram
    plt.title("Histogram with 'auto' bins")
    plt.savefig("plots/example_hist.png");
    '''
    
    
if __name__ == '__main__':
    main();    
