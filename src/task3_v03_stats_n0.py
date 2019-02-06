'''
@Author: Su Ming Yi
@Date: 12/04/2018
@Goal: 
    know when the airburst happen by analysis the statistics of each timestep vairable "v03"
    statistics: average, median, std
    
    know when the tsunami (wave rim) generated and start to propagate by analysis the statistics of
    each timestep variable "v02"
    statistics: average, mean, median, std, range, 
   

How to run it:
    C:\python\Lib\site-packages\VTK\bin\vtkpython.exe task3_v03_stats_n0.py

'''


import vtk
import vtk.util.numpy_support as VN
import numpy as np
import sys,os
import csv

def main():
    path = "D:/data/";
    # the variable name of data array which we used to analyze
    daryName = "v03";
    files = os.listdir(path);
    # declare empty list first, and for every timestep statistics inside.\
    #print(files)
    t_median = [];
    t_mean = [];
    t_std = [];
    t_size = [];
    t_max = [];
    t_min = [];         
    t_range = [];
    t_median.append("median");
    t_mean.append("mean");
    t_std.append("std");
    t_size.append("size");
    t_max.append("max");
    t_min.append("min");
    t_range.append("range");
    #for i in range(0, 1):
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
        dary = dary[dary!= 0]
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
        t_median.append(dMedian);
        t_mean.append(dMean);
        t_std.append(dstd);
        t_size.append(dsize);
        t_max.append(dMax);
        t_min.append(dMin);
        t_range.append(dRange);
        
        median = np.array(t_median);
        mean = np.array(t_mean);
        std = np.array(t_std);
        size = np.array(t_size);
        max_ar = np.array(t_max);
        min_ar = np.array(t_min);
        range_ar = np.array(t_range);
        files_ar = np.array(files);
    
        #files_ar.tofile('stats/yA31/filenames.csv', sep='\n');
        median.tofile('stats/yA31/'+daryName+"/"+daryName+'_median_n0.csv',sep='\n');
        mean.tofile('stats/yA31/'+daryName+"/"+daryName+'_mean_n0.csv', sep='\n');
        std.tofile('stats/yA31/'+daryName+"/"+daryName+'_std_n0.csv', sep='\n');
        size.tofile('stats/yA31/'+daryName+"/"+daryName+'_size_n0.csv', sep='\n');
        max_ar.tofile('stats/yA31/'+daryName+'/'+daryName+'_max_n0.csv', sep='\n');
        min_ar.tofile('stats/yA31/'+daryName+'/'+daryName+'_min_n0.csv', sep='\n');
        range_ar.tofile('stats/yA31/'+daryName+'/'+daryName+'_range_n0.csv',sep='\n');
    
    print("Total median: ", t_median);
    print("Total mean: ", t_mean);
    print("Total std: ", t_std);
    print("Total size: ", t_size);
    print("Total Max: ", t_max);
    print("Total Min: ", t_min);
    print("Total Range: ", t_range);
    
    '''
    median = np.array(t_median);
    mean = np.array(t_mean);
    std = np.array(t_std);
    size = np.array(t_size);
    max_ar = np.array(t_max);
    min_ar = np.array(t_min);
    range_ar = np.array(t_range);
    files_ar = np.array(files);
    
    #files_ar.tofile('stats/yA31/filenames.csv', sep='\n');
    median.tofile('stats/yA31/v03/v03_median_n0.csv',sep='\n');
    mean.tofile('stats/yA31/v03/v03_mean_n0.csv', sep='\n');
    std.tofile('stats/yA31/v03/v03_std_n0.csv', sep='\n');
    size.tofile('stats/yA31/v03/v03_size_n0.csv', sep='\n');
    max_ar.tofile('stats/yA31/v03/v03_max_n0.csv', sep='\n');
    min_ar.tofile('stats/yA31/v03/v03_min_n0.csv', sep='\n');
    range_ar.tofile('stats/yA31/v03/v03_range_n0.csv',sep='\n');
    '''

if __name__ == '__main__':
    main();    
