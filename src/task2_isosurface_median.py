'''
Author: Su Ming Yi
Date: 12/05/2018
Goal: 5544 final project
Data: pv_insitu_300x300x300_*.vti
Variable: v03
    use VTK to do isosurface with variable v03


How to run it:
C:\python\Lib\site-packages\VTK\bin\vtkpython.exe task2_isosurface_mean.py

'''
import vtk
import vtk.util.numpy_support as VN
import numpy as np
import sys
# This template is going to show a slice of the data
# The data used in this example can be downloaded from 
# http://oceans11.lanl.gov/deepwaterimpact/yA31/300x300x300-FourScalars_resolution/pv_insitu_300x300x300_49275.vti 

def main():
    # setup the dataset filepath
    all_filename = ['pv_insitu_300x300x300_29072.vti','pv_insitu_300x300x300_29263.vti',
                'pv_insitu_300x300x300_29449.vti','pv_insitu_300x300x300_29638.vti',
                'pv_insitu_300x300x300_29827.vti','pv_insitu_300x300x300_30015.vti',
                'pv_insitu_300x300x300_30205.vti','pv_insitu_300x300x300_30395.vti',
                'pv_insitu_300x300x300_30587.vti','pv_insitu_300x300x300_30778.vti',
                'pv_insitu_300x300x300_30966.vti']
    # iso_value_1 = average mean + 3*std
    # ios_value_2 = average median + 3*std
    # we calculate it in other file "finalproject_T2"
    iso_value_1 = 0.3544;
    iso_value_2 = 0.3246;

    #for i in range(0, 2):
    for i in range(0, len(all_filename)):
        filename = "yC31/"+all_filename[i];
        print(filename);
        #filename = "yC31/pv_insitu_300x300x300_29072.vti"
        # the name of data array which is used in this example
        daryName = "tev";
        #'v03' 'prs' 'tev'
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
        dMin = np.amin(dary);
        dRange = dMax - dMin;
        dMean = np.mean(dary);
        dMedian = np.median(dary);
        dstd = np.std(dary);
        print("Data array max: ", dMax);
        print("Data array min: ", dMin);
        print("Data array range: ", dRange);
        print("Data array mean: ", dMean);
        print("Data array median: ", dMedian);
        print("Data array std: ", dstd);
        ############ setup color map #########
        # Now create a loopup table that consists of the full hue circle
        # (from HSV).
        hueLut = vtk.vtkLookupTable();
        hueLut.SetTableRange(dMin, dMax);
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



    
        #################### create isosurface tev = mean + 3*std ######################################
        # isosurface 
        iso = vtk.vtkContourFilter();
        iso.SetInputConnection(reader.GetOutputPort());
        iso.Update();
        #iso.SetValue(0, iso_value_1);
        iso.SetValue(0, iso_value_2);

        normals = vtk.vtkPolyDataNormals();
        normals.SetInputConnection(iso.GetOutputPort());
        normals.SetFeatureAngle(45);

        isoMapper = vtk.vtkPolyDataMapper();
        isoMapper.SetInputConnection(normals.GetOutputPort());
        isoMapper.ScalarVisibilityOff();

        isoActor = vtk.vtkActor();
        isoActor.SetMapper(isoMapper);
        isoActor.GetProperty().SetColor(colors.GetColor3d("bisque"));
        isoActor.GetProperty().SetOpacity(0.3);
        #################################################################################################
        aCamera = vtk.vtkCamera();
        aCamera.SetViewUp(0, 0, 1);
        aCamera.SetPosition(1, 1, 2);
        aCamera.SetFocalPoint(0, 0, 0);
        aCamera.ComputeViewPlaneNormal();
        aCamera.Azimuth(45.0);
        aCamera.Elevation(45.0);
    
        ######################## create a text #####################
        # create a text actor
    
        txt = vtk.vtkTextActor()
        txt_str = "isosurface value (median+3*std)(bisque) = "+ str(iso_value_2)[:5]
        #txt_str = "isosurface value (mean+3*std)(bisque) = "+ str(iso_value_1)[:5]
        txt.SetInput(txt_str)
        txtprop=txt.GetTextProperty()
        txtprop.SetFontFamilyToArial()
        txtprop.SetFontSize(24)
        txtprop.SetColor(colors.GetColor3d("bisque"))
        txt.SetDisplayPosition(50,550)
        ##########################################################
    
        txt3 = vtk.vtkTextActor()
        txt_str3 = "timestep = "+filename[27:32]
        txt3.SetInput(txt_str3)
        txtprop3=txt3.GetTextProperty()
        txtprop3.SetFontFamilyToArial()
        txtprop3.SetFontSize(24)
        txtprop3.SetColor(0,0,0)
        txt3.SetDisplayPosition(50,500)
    
    

        # Actors are added to the renderer.
        aRenderer.AddActor(outline);
        aRenderer.AddActor(isoActor);
        aRenderer.AddActor(txt);
        aRenderer.AddActor(txt3);
        # An initial camera view is created. The Dolly() method moves
        # the camera towards the FocalPoint, thereby enlarging the image.
        aRenderer.SetActiveCamera(aCamera);

        # Calling Render() directly on a vtkRenderer is strictly forbidden.
        # Only calling Render() on the vtkRenderWindow is a valid call.
        renWin.Render();
        aRenderer.ResetCamera();
        aCamera.Dolly(-2.0);
    
        ####################################################################
        # screenshot code:
        w2if = vtk.vtkWindowToImageFilter()
        w2if.SetInput(renWin)
        w2if.Update()

        writer = vtk.vtkPNGWriter()
        saveName = "plots/ios/tev/median/"+daryName+"_t_"+filename[27:32]+".png";
        #saveName = "plots/ios/tev/mean/"+daryName+"_t_"+filename[27:32]+".png";
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
