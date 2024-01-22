import sys
sys.path.append('C:\\Users\\otmanbench\\Desktop\\utils\\BlenderToolbox\\') # change this to your path to “path/to/BlenderToolbox/
import BlenderToolBox as bt
import os, bpy, bmesh
import numpy as np
from os import listdir

def blender_render_obj_dir( obj_dir,render_dir,
                           frames=[0],
                           color=[158.0 / 255, 154.0 / 255, 200.0 / 255, 1],
                           imgRes_x=800, imgRes_y=800, numSamples=10, exposure=2,
                           location=[0, 0, 0], rotation=[0, 0, 0],
                           scale=[1, 1, 1], camLocation=[0.5, -1, 0.5], lookAtLocation=[0, 0, 0],
                           lightAngle=[-50, 5, -150], lightStrength=1, shadowSoftness=0.05, shadowThreshold=0.1,
                            lightAmbient=(0.1, 0.1, 0.1, 1)):
    cwd = os.getcwd()
    if isinstance(color, list):
        color = tuple(color)
    if isinstance(location, list):
        location = tuple(location)
    if isinstance(rotation, list):
        rotation = tuple(rotation)
    if isinstance(scale, list):
        scale = tuple(scale)
    if isinstance(camLocation, list):
        camLocation = tuple(camLocation)
    if isinstance(lookAtLocation, list):
        lookAtLocation = tuple(lookAtLocation)
    if isinstance(lightAngle, list):
        lightAngle = tuple(lightAngle)
    if isinstance(lightAmbient, list):
        lightAmbient = tuple(lightAmbient)
    focalLength = 45 # (UI: click camera > Object Data > Focal Length)

    i = 0
    for frame in frames:
        obj_file =  os.path.join(cwd,  obj_dir , str(frame).zfill(4) + ".obj")
        os.makedirs(render_dir, exist_ok=True)
        bt.blenderInit(imgRes_x, imgRes_y, numSamples, exposure)

        mesh = bt.readOBJ(obj_file, location, rotation, scale);
        bevel_mod = mesh.modifiers.new(name="MY-Bevel2", type='BEVEL')
        bevel_mod.width = 1.0
        # bt.subdivision(mesh, level = 1)
        meshColor = bt.colorObj(color, 0.5, 1.3, 1.0, 0.4, 2.0)
        AOStrength = 100
        bt.setMat_balloon(mesh, meshColor, AOStrength)

        bpy.ops.object.shade_smooth()
        cam = bt.setCamera(camLocation, lookAtLocation, focalLength)
        sun = bt.setLight_sun(lightAngle, lightStrength, shadowSoftness)
        bt.setLight_ambient(color=lightAmbient)
        # bpy.ops.wm.save_mainfile(filepath=os.getcwd() + render_dir + '/test.blend')
        outputPath = os.path.join(cwd, render_dir , str(frame).zfill(4) + '.png')


        bt.invisibleGround(location=(0, 0, -100), shadowBrightness=0.0)
        bt.shadowThreshold(shadowThreshold)
        bt.renderImage(outputPath, cam)


