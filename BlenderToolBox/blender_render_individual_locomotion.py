import sys
sys.path.append('C:\\Users\\otmanbench\\Desktop\\utils\\BlenderToolbox\\') # change this to your path to “path/to/BlenderToolbox/
import BlenderToolBox as bt
import os, bpy, bmesh
import mathutils
import numpy as np
from os import listdir


def move_by_amount(x, y, z, only_selected=True): # Default is True
    if only_selected:
        meshes = (obj.data for obj in bpy.context.selected_objects if obj.type == 'MESH')
    else:
        meshes = bpy.data.meshes
    for mesh in meshes: # We move selected/all meshes
        for vertex in mesh.vertices:
            vertex.co += Vector((x, y, z)) # See comments

def blender_render_individual_locomotion( scene_dir,mesh_names, render_dir,
                           frames=[0],
                           mesh_colors=None,
                           imgRes_x=800, imgRes_y=800, numSamples=10, exposure=2,
                           location=[0, 0, 0], rotation=[0, 0, 0],
                           scale=[1, 1, 1], camLocation=[0, -3, 0], lookAtLocation=[0, 0, 0],
                           lightAngle=[-50, 5, -150], lightStrength=1, shadowSoftness=0.05, shadowThreshold=0.1,
                            lightAmbient=(0.1, 0.1, 0.1, 1)):
    cwd = os.getcwd()
    if mesh_colors is None:
        mesh_colors = [bt.derekBlue] * len(mesh_names)

    if isinstance(camLocation, list):
        camLocation = tuple(camLocation)
    if isinstance(lookAtLocation, list):
        lookAtLocation = tuple(lookAtLocation)
    if isinstance(lightAngle, list):
        lightAngle = tuple(lightAngle)
    if isinstance(lightAmbient, list):
        lightAmbient = tuple(lightAmbient)
    focalLength = 45 # (UI: click camera > Object Data > Focal Length)



    for i, name in enumerate(mesh_names):
        obj_dir = os.path.join(scene_dir, name)

        obj_file = os.path.join(cwd, obj_dir, str(frames[0]).zfill(4) + ".obj")
        bt.blenderInit(imgRes_x, imgRes_y, numSamples, exposure)

        # mesh = bt.readOBJ(obj_file, tuple([0, 0, 0]), tuple([0, 0, 0]), tuple(scale[i]));
        # vertices_co = [v.co for v in mesh.data.vertices]
        # center_of_mass = sum(vertices_co, mathutils.Vector()) / len(vertices_co)
        # offset = mathutils.Vector((0, center_of_mass[1], 0)) - center_of_mass

        outputDir = os.path.join(cwd, render_dir, name)
        os.makedirs(outputDir, exist_ok=True)

        for frame in frames:
            obj_file = os.path.join(cwd, obj_dir, str(frame).zfill(4) + ".obj")

            bt.blenderInit(imgRes_x, imgRes_y, numSamples, exposure)

            outputPath = os.path.join(cwd, outputDir, str(frame).zfill(4) + '.png')


            mesh = bt.readOBJ(obj_file, tuple([0, 0, 0]), tuple([90, 0, 0]), tuple(scale[i]));


            vertices_co = [v.co for v in mesh.data.vertices]
            center_of_mass = sum(vertices_co, mathutils.Vector()) / len(vertices_co)
            offset = mathutils.Vector((0, center_of_mass[1], 0)) - center_of_mass

            for vertex in mesh.data.vertices:
                vertex.co += offset
            # # Update vertices to move the center of mass to the origin

            # print(center_of_mass)
            print("######### Center of MAss : " + str(center_of_mass))
            camLocation_2 = (camLocation[0] , camLocation[1], camLocation[2])
            lookAtLocation_2 = (lookAtLocation[0] + center_of_mass[0], lookAtLocation[1], lookAtLocation[2])
            cam = bt.setCamera(camLocation_2, lookAtLocation_2, focalLength)
            sun = bt.setLight_sun(lightAngle, lightStrength, shadowSoftness)
            bt.setLight_ambient(color=lightAmbient)
            # print(np.array(mesh.data.vertices.mean(0).shape))
            # break
            # mean_location = (0, 0, 0, 1) #np.mean(np.array(mesh.data.vertices), axis=0)
            # print(mean_location)
            # for vert in mesh.data.vertices:
            #     new_location = vert.co
            #     mean_location[0] = mean_location[0] + 1  # X
            #     mean_location[1] = mean_location[1] + 1  # Y
            #     mean_location[2] = mean_location[2] + 1  # Z
            #     vert.co = new_location



            # bevel_mod = mesh.modifiers.new(name="MY-Bevel2", type='BEVEL')
            # bevel_mod.width = 1.0
            # bt.subdivision(mesh, level = 1)
            meshColor = bt.colorObj(mesh_colors[i], 0.5, 1.3, 1.0, 0.4, 2.0)
            AOStrength = 2
            bt.setMat_balloon(mesh, meshColor, AOStrength)
            bpy.ops.object.shade_smooth()

            # bpy.ops.wm.save_mainfile(filepath= outputDir + '/test_' +  str(frame).zfill(4) + '.blend')


            bt.invisibleGround(location=(0, 0, -0.05), shadowBrightness=0.0)
            bt.shadowThreshold(shadowThreshold)
            bt.renderImage(outputPath, cam)


