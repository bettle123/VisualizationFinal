'''
Author: Su Ming Yi
Date: 11/18/2018
Goal: 5544 final project
Variable: v03
    use VTK to do volume rendering

How to run it:
C:\python\Lib\site-packages\VTK\bin\vtkpython.exe task4_volume_rendering.py

'''
import vtk
import vtk.util.numpy_support as VN
import numpy as np
import sys,os
# This template is going to show a slice of the data
# The data used in this example can be downloaded from 
# http://oceans11.lanl.gov/deepwaterimpact/yA31/300x300x300-FourScalars_resolution/pv_insitu_300x300x300_49275.vti 

def main():
    # setup the dataset filepath
    #all_filename = np.genfromtxt('stats/yA31/filenames.csv', dtype=None)
    path = "D:/data/"
    files = os.listdir(path);
    time_index = [];
    for i in range(180, len(files)):
        if(i%5==0):
            time_index.append(i);
    #print(files);
    daryName = "v02";
    #'v03' 'prs' 'tev'
    #for i in range(236, 237):
    #for i in range(0, 1):
    for i in range(0, len(time_index)):
        filename = path+files[time_index[i]];
        #filename = path+ files[i];
        print(filename);
        # for accessomg build-in color access
        colors = vtk.vtkNamedColors();

        # Create the renderer, the render window, and the interactor.
        # The renderer draws into the render window.
        # The interactor enables mouse and keyboard-based interaction 
        # with the data within the render windows.


        aRenderer = vtk.vtkRenderer();
        renWin = vtk.vtkRenderWindow();
        renWin.AddRenderer(aRenderer);
        iren = vtk.vtkRenderWindowInteractor();
        iren.SetRenderWindow(renWin);

        # Set a background color for the renderer
        # and set the size of the render window.
        aRenderer.SetBackground(colors.GetColor3d("Silver"));
        renWin.SetSize(600, 600);

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
        #dary = dary[dary>dMax/2]
        dMin = np.amin(dary);
        dRange = dMax - dMin;
        dMean = np.mean(dary);
        dMedian = np.median(dary);
        #dary = dary[dary>dMax/2]
        
        print("Data array max: ", dMax);
        print("Data array min: ", dMin);
        print("Data array range: ", dRange);
        print("Data array mean: ", dMean);
        print("Data array median: ", dMedian);
        
        ############ setup color map #########


        hueLut = vtk.vtkLookupTable();
        # This creates a red ,white, blue lut.
        hueLut.SetHueRange(0.67, 0.0)
        hueLut.Build();



        # An outline provides context around the data.
        outlineData = vtk.vtkOutlineFilter();
        outlineData.SetInputConnection(reader.GetOutputPort());
        outlineData.Update()

        mapOutline = vtk.vtkPolyDataMapper();
        mapOutline.SetInputConnection(outlineData.GetOutputPort());

        outline = vtk.vtkActor();
        outline.SetMapper(mapOutline);
        outline.GetProperty().SetColor(colors.GetColor3d("Black"));

        ################## create volume rendering ################################

        # Create transfer mapping scalar value to opacity
        opacityTransferFunction = vtk.vtkPiecewiseFunction();
        opacityTransferFunction.AddPoint(0.0, 0.0001);
        opacityTransferFunction.AddPoint(0.5, 0.0001);
        opacityTransferFunction.AddPoint(1.0, 0.005);

        # int AddRGBPoint (double x, double r, double g, double b)
        # int AddHSVPoint (double x, double h, double s, double v)
        # Create transfer mapping scalar value to color.
        colorTransferFunction = vtk.vtkColorTransferFunction()

        colorTransferFunction.AddRGBPoint(dMin, 0.0, 0.0, 1.0);
        colorTransferFunction.AddRGBPoint(0.5, 0.0, 1.0, 0.0);
        colorTransferFunction.AddRGBPoint(dMax, 1.0, 0.0, 0.0);

        # The property describes how the data will look.
        volumeProperty = vtk.vtkVolumeProperty()
        volumeProperty.SetColor(colorTransferFunction)
        volumeProperty.SetScalarOpacity(opacityTransferFunction)
        volumeProperty.SetScalarOpacityUnitDistance(100);
        volumeProperty.SetInterpolationTypeToLinear()

        # The mapper / ray cast function know how to render the data.
        volumeMapper = vtk.vtkGPUVolumeRayCastMapper();
        volumeMapper.SetInputConnection(reader.GetOutputPort())

        # The volume holds the mapper and the property and
        # can be used to position/orient the volume.
        volume = vtk.vtkVolume()
        volume.SetMapper(volumeMapper)
        volume.SetProperty(volumeProperty)

        ######################## create a text #####################
        # create a text actor
        txt = vtk.vtkTextActor()
        txt.SetInput("Color map")
        txtprop=txt.GetTextProperty()
        txtprop.SetFontFamilyToArial()
        txtprop.SetFontSize(24)
        txtprop.SetColor(0.0, 0.0, 0.0)
        txt.SetDisplayPosition(450,550)

        ############################################################
        txt2 = vtk.vtkTextActor()
        txt_str2 = "timestep = "+filename[30:35]+", Scalar Value (v02)"
        txt2.SetInput(txt_str2)
        txtprop2=txt2.GetTextProperty()
        txtprop2.SetFontFamilyToArial()
        txtprop2.SetFontSize(24)
        txtprop2.SetColor(0,0,0)
        txt2.SetDisplayPosition(20,550)
        ############################ create a color bar ###########################
        
        
        # create the scalar_bar
        scalar_bar = vtk.vtkScalarBarActor()
        scalar_bar.SetOrientationToHorizontal()
        scalar_bar.SetLookupTable(hueLut)
 

        # create the scalar_bar_widget
        scalar_bar_widget = vtk.vtkScalarBarWidget()
        scalar_bar_widget.SetInteractor(iren)
        scalar_bar_widget.SetScalarBarActor(scalar_bar)
        scalar_bar_widget.On()
        

        aCamera = vtk.vtkCamera();
        aCamera.SetViewUp(0, 1, 0);
        aCamera.SetPosition(-0.2, 0.2, 0.5);
        aCamera.SetFocalPoint(0, 0, 0);
        aCamera.ComputeViewPlaneNormal();
        #aCamera.Azimuth(45.0);
        #aCamera.Elevation(45.0);
        #aCamera.Zoom(0.01);
        #aCamera.Dolly(10.0);

        # Actors are added to the renderer.
        aRenderer.AddActor(outline);
        aRenderer.AddVolume(volume);
        aRenderer.AddActor(txt);
        aRenderer.AddActor(txt2);
        # An initial camera view is created. The Dolly() method moves
        # the camera towards the FocalPoint, thereby enlarging the image.
        aRenderer.SetActiveCamera(aCamera);

        # Calling Render() directly on a vtkRenderer is strictly forbidden.
        # Only calling Render() on the vtkRenderWindow is a valid call.
        renWin.Render();
        aRenderer.ResetCamera();
        #aCamera.Dolly(-2.0);
        ####################################################################
        # screenshot code:
        w2if = vtk.vtkWindowToImageFilter()
        w2if.SetInput(renWin)
        w2if.Update()

        writer = vtk.vtkPNGWriter()
        saveName = "plots/yA31/v_r/v02/"+daryName+"_t_"+filename[30:35]+".png";
        writer.SetFileName(saveName)
        writer.SetInputData(w2if.GetOutput())
        writer.Write()
        
        #####################################################################
        # Note that when camera movement occurs (as it does in the Dolly() method),
        # the clipping planes often need adjusting.
        # Clipping planes consist of two planes:
        # near and far along the view direction.
        # The near plane clips out objects in front of the plane;
        # the far plane clips out objects behind the plane.
        # This way only what is drawn between the planes is actually rendered.

        aRenderer.ResetCameraClippingRange();

        # Interact with the data.
        renWin.Render();
        #iren.Initialize();
        #iren.Start();


if __name__ == '__main__':
    main(); 
