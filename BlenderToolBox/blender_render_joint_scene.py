import sys
sys.path.append('C:\\Users\\otmanbench\\Desktop\\utils\\BlenderToolbox\\') # change this to your path to “path/to/BlenderToolbox/
import BlenderToolBox as bt
import os, bpy, bmesh
import numpy as np
from os import listdir

def blender_render_joint_scene( scene_dir,mesh_names, render_dir,
                           frames=[0],
                           mesh_colors=None,
                           imgRes_x=800, imgRes_y=800, numSamples=10, exposure=2,
                           location=[0, 0, 0], rotation=[0, 0, 0],
                           scale=[1, 1, 1], camLocation=[0.5, -1, 0.5], lookAtLocation=[0, 0, 0],
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

    os.makedirs(render_dir, exist_ok=True)

    for frame in frames:
        bt.blenderInit(imgRes_x, imgRes_y, numSamples, exposure)
        outputPath = os.path.join(cwd, render_dir, str(frame).zfill(4) + '.png')

        cam = bt.setCamera(camLocation, lookAtLocation, focalLength)
        sun = bt.setLight_sun(lightAngle, lightStrength, shadowSoftness)
        bt.setLight_ambient(color=lightAmbient)
        for i, name in enumerate(mesh_names):
            obj_dir = os.path.join(scene_dir, name)
            obj_file =  os.path.join(cwd,  obj_dir , str(frame).zfill(4) + ".obj")

            mesh = bt.readOBJ(obj_file, tuple(location[i]), tuple(rotation[i]), tuple(scale[i]));
            bevel_mod = mesh.modifiers.new(name="MY-Bevel2", type='BEVEL')
            bevel_mod.width = 1.0
            # bt.subdivision(mesh, level = 1)
            meshColor = bt.colorObj(mesh_colors[i], 0.5, 1.3, 1.0, 0.4, 2.0)
            AOStrength = 2
            bt.setMat_balloon(mesh, meshColor, AOStrength)
            bpy.ops.object.shade_smooth()

            # bpy.ops.wm.save_mainfile(filepath=os.getcwd() + render_dir + '/test.blend')


        bt.invisibleGround(location=(0, 0, -0.05), shadowBrightness=0.0)
        bt.shadowThreshold(shadowThreshold)
        bt.renderImage(outputPath, cam)


