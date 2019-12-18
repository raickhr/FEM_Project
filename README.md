## Shikhar Rai 

This is a FEM course project at University of Rochester. Fall 2019
## Input format

An input folder location is to be provided in file main.py inside codes folder. The input file should contain files:

1. bc_code.txt
2. coord.txt
3. elemconn.txt
4. elementid.txt
5. loads.txt
6. matprop.txt
7. nodeid.txt

Sample of the input files are in FEM_Project\input folder and FEM_Project\inputCoarse folder for fine and coarse mesh. The lines that start with '%' are the comment lines and are ignored by the code.

## Running the code

Download the folder FEM_project and go to FEM_Project/codes folder.

* Run for reduced integraion
    * python main.py --integration reduced --inputDir ../input

* Run for full integraion
    * python main.py --integration full --inputDir ../input

A user defined location for input folder can be given instead of '../input' for inputDir argument.

## Cases
The problem solved here is a planar problem, where a unit point force is applied to a cylinder radially at top of the circumference of the cylinder. Because of the symmetry of the problem only a quarter of the problem is solved.
<img src="FEM_Project/images/ProblemDes.png" height=250 width =520 />

<center>
<table>
  <tr>
     <td>
        <img style="width: 200px; height: 200px" src="FEM_Project/images/Undeformed Coarse.png"/>
         <br/>Figure: Coarse Mesh</a>
     </td>
     <td>
        <img style="width: 200px; height: 200px" src="FEM_Project/images/Undeformed Fine.png"/>
        <br/>Figure: Fine Mesh</a>
     </td>
  </tr>
</table>
</center>

Four cases as following has been documented here:

1. Coarse Mesh Reduced Integration
2. Coarse Mesh Full Integraion
3. Fine Mesh Reduced Integration
4. Fine Mesh Full Integration

All of the cases have same boundary conditions and loading