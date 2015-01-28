# python-traffic-sim
Python traffic simulation script. Created for Autodesk Maya 2014

AI Python Script
Created by Ramesh Balachandran

How to run AI script in Maya
For any information about any of the functions use: help( function name ) in the script editor once the script has been run

If using supplied Maya .mb file:

- Open the supplied Maya .mb file
- The scene is already set up with all of the cars, building sets and additional meshes needed to run the AI script
- Load the supplied AI .py script in the script editor and run all (click the double 'play' button at the top of the script editor)
- The supplied .mb file already has the necessary expression in the expression editor
- Press play on the timeline and AI will begin

If using custom scene:

- Load the supplied AI .py script in the script editor
- Open the expression edtor and input the expression: python("update("+frame+")");
- Ensure that the carList in the script is filled with the names of all the cars in your scene
- Ensure that the junctionList is filled with the names of all the junctions in the scene
- Make sure that any taxis in the scene start with the name 'taxi' (and are part of the carList)
- Ensure that the taxiStandList is filled with the names of all taxi stands in the scene
- Once all assets have been set in the scene, don't run the reset function (only applicable to the supplied .mb file)
- Run the rest of the script
- Press play on the timeline and AI will begin
