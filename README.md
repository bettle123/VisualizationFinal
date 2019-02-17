# VisualizationFinal
@Author: Su Ming Yi <br />
@Date: 02/06/2019 <br />
@Library: Python, vtk <br />
@Data Source: https://sciviscontest2018.org <br />

In this project, we will introduce the data information we use and focus on answering four tasks:
1. When does the airburst happen? 
2. When does the size of the region with abnormal temperature caused by the asteroid reach its maximum and start to shrink?
3. When does the asteroid hit the water surface? 
4. When is the tsunami (wave rim) generated and start to propagate?

Due to huge size of data, we accomplish four tasks by the following steps.
First, we plot the time series plots of attributes for summary statistics ["median", "mean", std", "size", "max", "min", "range"].
According to these plots, we determine which timesteps we visualize.
Second, we answer the time range of four tasks by plotting Volume Rendering and iso-surface.

There are some screenshots for demonstration.

## ScreenShot1 - Time Series plot of "tev" mean
!["ScreenShot1"](https://github.com/bettle123/VisualizationFinal/blob/master/plots/yC31/series/tev/tev_mean.png)

## ScreenShot2 - Volume Rendering
!["ScreenShot2"](https://github.com/bettle123/VisualizationFinal/blob/master/plots/yA31/v_r/v02/v02_t_40654.png)

## DemoVideo1 - Volume Rendering
!["DemoVideo1"](https://github.com/bettle123/VisualizationFinal/blob/master/plots/yA31/v_r/v02/v_r_gif.gif)

## ScreenShot3 - Iso-surface
!["ScreenShot3"](https://github.com/bettle123/VisualizationFinal/blob/master/plots/yA31/ios/v02/v02_t_37765.png)

## DemoVideo2 - Iso-surface
!["DemoVideo2"](https://github.com/bettle123/VisualizationFinal/blob/master/plots/yA31/ios/v02/iso_gif.gif)
