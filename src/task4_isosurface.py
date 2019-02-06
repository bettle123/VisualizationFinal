'''
Author: Su Ming Yi
Date: 12/05/2018
Goal: 5544 final project
Data: pv_insitu_300x300x300_*.vti
Variable: v03
    use VTK to do isosurface with variable v03


How to run it:
C:\python\Lib\site-packages\VTK\bin\vtkpython.exe task4_isosurface.py

'''
import vtk
import vtk.util.numpy_support as VN
import numpy as np
import sys, os
# This template is going to show a slice of the data
# The data used in this example can be downloaded from 
# http://oceans11.lanl.gov/deepwaterimpact/yA31/300x300x300-FourScalars_resolution/pv_insitu_300x300x300_49275.vti 

def main():
    # setup the dataset filepath
    path = "D:/data/"
    files = os.listdir(path);
    time_index = [];
    for i in range(266, 300):
        if(i%3==0):
            time_index.append(i);
    #print(files);
    daryName = "v02";          
    
    for i in range(0, len(time_index)):
    #for i in range(0, 1):
        filename = path+ files[time_index[i]];
        print(filename);
        #filename = "yC31/pv_insitu_300x300x300_29072.vti"
        # the name of data array which is used in this example
        daryName = "v02";
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



    
        #################### create isosurface v02 = mean ######################################
        # isosurface 
        iso = vtk.vtkContourFilter();
        iso.SetInputConnection(reader.GetOutputPort());
        iso.Update();
        iso.SetValue(0, dMean);

        normals = vtk.vtkPolyDataNormals();
        normals.SetInputConnection(iso.GetOutputPort());
        normals.SetFeatureAngle(45);

        isoMapper = vtk.vtkPolyDataMapper();
        isoMapper.SetInputConnection(normals.GetOutputPort());
        isoMapper.ScalarVisibilityOff();

        isoActor = vtk.vtkActor();
        isoActor.SetMapper(isoMapper);
        isoActor.GetProperty().SetColor(colors.GetColor3d("bisque"));
        isoActor.GetProperty().SetOpacity(0.5);
        ############################### create isosurface v02 = median######################################
        '''
        # isosurface 
        iso2 = vtk.vtkContourFilter();
        iso2.SetInputConnection(reader.GetOutputPort());
        iso2.Update();
        iso2.SetValue(0, dMedian);


        normals2 = vtk.vtkPolyDataNormals();
        normals2.SetInputConnection(iso2.GetOutputPort());
        normals2.SetFeatureAngle(45);

        isoMapper2 = vtk.vtkPolyDataMapper();
        isoMapper2.SetInputConnection(normals2.GetOutputPort());
        isoMapper2.ScalarVisibilityOff();

        isoActor2 = vtk.vtkActor();
        isoActor2.SetMapper(isoMapper2);
        isoActor2.GetProperty().SetColor(0.0, 0.9, 0.9);
        isoActor2.GetProperty().SetOpacity(0.2);
        '''
        ###############################################################################
        aCamera = vtk.vtkCamera();
        aCamera.SetViewUp(0, 0, 1);
        aCamera.SetPosition(1, 1, 2);
        aCamera.SetFocalPoint(0, 0, 0);
        aCamera.ComputeViewPlaneNormal();
        aCamera.Azimuth(45.0);
        aCamera.Elevation(-140.0);
    
        ######################## create a text #####################
        # create a text actor
    
        txt = vtk.vtkTextActor()
        txt_str = "isosurface value(bisque) (mean) = "+str(dMean)[:5]
        txt.SetInput(txt_str)
        txtprop=txt.GetTextProperty()
        txtprop.SetFontFamilyToArial()
        txtprop.SetFontSize(24)
        txtprop.SetColor(colors.GetColor3d("bisque"))
        txt.SetDisplayPosition(50,550)
        ############################################################
        txt2 = vtk.vtkTextActor()
        txt_str2 = "isosurface value (median)(blue) = "+ str(dMedian)[:5]
        txt2.SetInput(txt_str2)
        txtprop2=txt2.GetTextProperty()
        txtprop2.SetFontFamilyToArial()
        txtprop2.SetFontSize(24)
        txtprop2.SetColor(0,0.9,0.9)
        txt2.SetDisplayPosition(50,525)
        ##########################################################
    
        txt3 = vtk.vtkTextActor()
        txt_str3 = "timestep = "+filename[30:35]
        txt3.SetInput(txt_str3)
        txtprop3=txt3.GetTextProperty()
        txtprop3.SetFontFamilyToArial()
        txtprop3.SetFontSize(24)
        txtprop3.SetColor(0,0,0)
        txt3.SetDisplayPosition(50,500)
    
    

        # Actors are added to the renderer.
        aRenderer.AddActor(outline);
        aRenderer.AddActor(isoActor);
        #aRenderer.AddActor(isoActor2);
        aRenderer.AddActor(txt);
        #aRenderer.AddActor(txt2);
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
        saveName = "plots/yA31/ios/v02/"+daryName+"_t_"+filename[30:35]+".png";
        writer.SetFileName(saveName)
        writer.SetInputData(w2if.GetOutput())
        writer.Write()
    
        #####################################################################

        # Note that when camera movement occurs (as it does in the Dolly() method),
        # the clipping planes often
        #need adjusting.
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
