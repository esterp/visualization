#! /usr/bin/env python
import vtk
import sys

def main(argv):
  if len(argv) < 2:
    print "usage: ",argv[0]," <data>"
    exit(1)
  data_fn = argv[1]
  
  data = None
  if data_fn.find('.vtk') != -1:
    reader = vtk.vtkStructuredPointsReader()
    reader.SetFileName(data_fn)
    reader.Update()
    data = reader.GetOutput()
  elif data_fn.find('.dcm') != -1:
    reader =vtk.vtkDICOMImageReader()
    reader.SetFileName(data_fn)
    reader.Update()
    data = reader.GetOutput()

  ptdata = data.GetPointData()
  scalars = ptdata.GetScalars()  
  data_range = scalars.GetValueRange()
  print "data range:",data_range
  contourer = vtk.vtkContourFilter()
  if data_fn.find('body') != -1:
    contourer.GenerateValues(10,data_range[0],data_range[1])
    #contourer.GenerateValues(5,data_range[0],data_range[1])
  elif data_fn.find('brain') != -1:
    contourer.GenerateValues(10,data_range[0],data_range[1])
  elif data_fn.find('artichoke') != -1:
    contourer.GenerateValues(50,data_range[0],data_range[1])
  elif data_fn.find('watermelon') != -1:
    contourer.GenerateValues(20,data_range[0],data_range[1])
    #contourer.GenerateValues(5,data_range[0],data_range[1])
  else:
    contourer.GenerateValues(10,data_range[0],data_range[1])
    #contourer.SetNumberOfContours(3)
    #contourer.SetValue(0, 100)
    #contourer.SetValue(1, 300)
    #contourer.SetValue(2, 400)
  contourer.SetInput(data)
  contourer.Update()

  mapper = vtk.vtkPolyDataMapper()
  mapper.SetInputConnection(contourer.GetOutputPort())

  actor = vtk.vtkActor()
  actor.SetMapper(mapper)
  
  renderer = vtk.vtkRenderer()
  renderWindow = vtk.vtkRenderWindow()
  renderWindow.SetSize(700,700)
  renderWindow.AddRenderer(renderer)
 
  renderer.AddActor(actor)
  renderer.SetBackground(0.4,0.3,0.2)

  interactor = vtk.vtkRenderWindowInteractor()
  interactor.SetRenderWindow(renderWindow)
  
  renderWindow.Render()
  interactor.Start()

if __name__ == "__main__":
  main(sys.argv)
