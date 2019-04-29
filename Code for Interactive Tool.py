# Name: Code for Interactive Tool
# Purpose: Prompt the user for the buffer distance for parks, day care and subway entrance.
# Author: Faith Zou, Garret Hiles
# Created: 04/25/2019

try:
    # Import the modles
    import arcpy
    import sys
    from arcpy import env

    # Set up the environment
    # Workspace needs to be changed manually because local path might be different.
    # For workspace, make sure to use \\.
    env.workspace = raw_input("Enter the file path. Use 2\ instead of \: ")
    env.OverwriteOutput = True
    
    # Get input from user.
    
    bufferPark = raw_input("Enter an integer. Buffer distance(in meters) for parks: ")
    bufferDay = raw_input("Enter an integer. Buffer distance(in meters) for day care centers: ")
    bufferSubway = raw_input("Enter an integer. Buffer distance(in meters) for subway entrances: ")

    #Buffer for parks
    
    parks = "Parks.shp"
    parksBuffer = "parks_output"
    buffer_distance = int(bufferPark)
    dissolve_option = "ALL"
    arcpy.Buffer_analysis(parks, parksBuffer, buffer_distance,'' ,'',dissolve_option)

    #Buffer for Day Care Center
    
    DayCareCenter = "DayCareCenter.shp"
    DayBuffer = "DayCareCenter_output"
    buffer_distance = int(bufferDay)
    dissolve_option = "ALL"
    arcpy.Buffer_analysis(DayCareCenter, DayBuffer, buffer_distance,'' ,'',dissolve_option)

    #Buffer for subway entrances
    
    SubwayEntrance = "SubwayEntrance.shp"
    SubwayBuffer = "SubwayEntrance_output"
    buffer_distance = int(bufferSubway)
    dissolve_option = "ALL"
    arcpy.Buffer_analysis(SubwayEntrance, SubwayBuffer, buffer_distance,'' ,'',dissolve_option)

    # Find the joint area
    
    inFeatures = ["parks_output.shp", "DayCareCenter_output.shp", "SubwayEntrance_output.shp"]
    intersectOutput = "JointArea"
    arcpy.Intersect_analysis(inFeatures, intersectOutput,'','','INPUT')

    # Clip Houses
    in_features = "Houses.shp"
    clip_features = "JointArea.shp"
    out_feature_class = "QualifiedHouses.shp"
    xy_tolerance = ""
    arcpy.Clip_analysis(in_features, clip_features, out_feature_class, xy_tolerance)

    # Start of map production.
    map_document = arcpy.mapping.MapDocument("380 Final Project.mxd")

    # Print out the number of housing projects that fit the requirements.
    result = arcpy.GetCount_management("QualifiedHouses.shp")
    print ('{} has {} records'.format("QualifiedHouses.shp", result[0]))

    # Add the qualified layer to the map
    data_frame = arcpy.mapping.ListDataFrames(map_document,"*")[0]
    add_layer = arcpy.mapping.Layer("QualifiedHouses.shp")
    
    # Turn off the existing QualifiedHouses layer.
    lyrlist = arcpy.mapping.ListLayers(map_document)
    for lyr in lyrlist:
        if lyr.name == "QualifiedHouses":
            lyr.visible = False

    # Add layer
    arcpy.mapping.AddLayer(data_frame, add_layer)
    map_document.save()
    
    # Export to pdf
    out_pdf = "user_output"
    print "There is a map generated for you!"
    arcpy.mapping.ExportToPDF(map_document, out_pdf)

    # Delete everything except for the pdf document, in order to create spaces for new files for next run.
    
    del map_document
    arcpy.Delete_management("parks_output.shp")
    arcpy.Delete_management("SubwayEntrance_output.shp")
    arcpy.Delete_management("DayCareCenter_output.shp")
    arcpy.Delete_management("JointArea.shp")
    arcpy.Delete_management("QualifiedHouses.shp")
    
    # Throw exceptions.

except arcpy.ExecuteError:
    print arcpy.GetMessages(2)
except:
    print "Process did not complete, no map was generated."
