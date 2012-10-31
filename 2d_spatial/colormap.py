#! /usr/bin/env python
import vtk
import sys

def main(argv):
  if len(argv) < 2:
    print "usage: ",argv[0]," <data> [flat]"
    exit(1)
  data_fn = argv[1]
  flat = False
  if len(argv) > 2:
    flat = True
  
  mapper = vtk.vtkPolyDataMapper()
  if data_fn.find('.vtk') != -1:
    reader = vtk.vtkPolyDataReader()
    reader.SetFileName(data_fn)
    reader.Update()
    data = reader.GetOutput()
    trianglize = vtk.vtkDelaunay2D()
    trianglize.SetInput(data)
    trianglize.Update()
    mapper.SetInputConnection(trianglize.GetOutputPort())
  elif data_fn.find('.pgm') != -1:
    reader = vtk.vtkPNMReader()
    reader.SetFileName(data_fn)
    reader.Update()
    data = reader.GetOutput()
    trianglize = vtk.vtkImageDataGeometryFilter()
    trianglize.SetInput(data)
    trianglize.Update()
    if flat:
      mapper.SetInputConnection(trianglize.GetOutputPort())
    else:
      warp = vtk.vtkWarpScalar()
      warp.SetScaleFactor(0.2) # "looked the best"
      warp.SetInputConnection(trianglize.GetOutputPort())
      warp.Update()
      mapper.SetInputConnection(warp.GetOutputPort())
  elif data_fn.find('.dcm') != -1:
    reader =vtk.vtkDICOMImageReader()
    reader.SetFileName(data_fn)
    reader.Update()
    data = reader.GetOutput()
    trianglize = vtk.vtkImageDataGeometryFilter()
    trianglize.SetInput(data)
    trianglize.Update()
    if flat:
      mapper.SetInputConnection(trianglize.GetOutputPort())
    else:
      warp = vtk.vtkWarpScalar()
      warp.SetScaleFactor(0.2) # "looked the best"
      warp.SetInputConnection(trianglize.GetOutputPort())
      warp.Update()
      mapper.SetInputConnection(warp.GetOutputPort())
  else:
    print "unrecognized data file:",data_fn
    exit(1)
  
 
  actor = vtk.vtkActor()
  actor.SetMapper(mapper)
  
  renderer = vtk.vtkRenderer()
  renderWindow = vtk.vtkRenderWindow()
  renderWindow.SetSize(400,300)
  renderWindow.AddRenderer(renderer)
 
  renderer.AddActor(actor)
  renderer.SetBackground(0.4,0.3,0.2)

  interactor = vtk.vtkRenderWindowInteractor()
  interactor.SetRenderWindow(renderWindow)
  
  renderWindow.Render()
  interactor.Start()

if __name__ == "__main__":
  main(sys.argv)
