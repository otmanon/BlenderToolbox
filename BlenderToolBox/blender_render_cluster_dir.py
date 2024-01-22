import sys
sys.path.append('C:\\Users\\otmanbench\\Desktop\\utils\\BlenderToolbox\\') # change this to your path to “path/to/BlenderToolbox/
import BlenderToolBox as bt
import os, bpy, bmesh
import numpy as np
from os import listdir

def find_max_file_number(directory_path):
    max_file_number = -1

    # Ensure the provided path is a directory
    if os.path.isdir(directory_path):
        # List all items in the directory
        items = os.listdir(directory_path)

        for item in items:
            item_path = os.path.join(directory_path, item)

            # Check if it's a file and follows the naming pattern "cluster_<xxxx>.obj"
            if os.path.isfile(item_path) and item.startswith("cluster_") and item[8:-4].isdigit():
                file_number = int(item[8:-4])
                max_file_number = max(max_file_number, file_number)

    return max_file_number
def blender_render_cluster_dir( cluster_dir, l_path, bI_path, render_dir,
                           texture_path="./RdBu_11.png",
                           imgRes_x=800, imgRes_y=800, numSamples=10, exposure=2,
                           location=[0, 0, 0], rotation=[0, 0, 0],
                           scale=[1, 1, 1], camLocation=[0.5, -1, 0.5], lookAtLocation=[0, 0, 0],
                           lightAngle=[-50, 5, -150], lightStrength=1, shadowSoftness=0.05, shadowThreshold=0.1,
                            lightAmbient=(0.1, 0.1, 0.1, 1)):
    cwd = os.getcwd()

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

    max_cluster = find_max_file_number(cluster_dir)
    i = 0

    l = np.load(l_path)
    Cdata = l
    maxim = np.abs(Cdata).max()
    # Cdata = (Cdata) + maxim;
    # Cdata = Cdata / (2.0 * maxim);
    # Cdata += 1e-3
    # Cdata = np.minimum(Cdata, 0.99)

    bI = np.load(bI_path)
    print(max_cluster)
    # for cluster_num in range(max_cluster):
    os.makedirs(render_dir, exist_ok=True)
    bt.blenderInit(imgRes_x, imgRes_y, numSamples, exposure)
    cam = bt.setCamera(camLocation, lookAtLocation, focalLength)
    sun = bt.setLight_sun(lightAngle, lightStrength, shadowSoftness)
    bt.setLight_ambient(color=lightAmbient)

    for i in range(max_cluster + 1):
        obj_file = os.path.join(cwd, cluster_dir + "/cluster_" + str(i).zfill(4) + ".obj")
        mesh = bt.readOBJ(obj_file, location, rotation, scale);
        # bevel_mod = mesh.modifiers.new(name="MY-Bevel2", type='BEVEL')
        # bevel_mod.width = 0.01
        # bt.subdivision(mesh, level = 1)
        # print("mesh ", len(mesh.data.vertices))
        # print("min", Cdata.min())
        # max
        # print("max", Cdata.max())
        Cdata_cluster = (( bI[i] / maxim)) # np.minimum((cluster_num + maxim)/(2.0 * maxim) + 1e-3, 0.99);
        vertex_scalars = np.ones( len(mesh.data.vertices)) * Cdata_cluster  # vertex color list
        mesh = bt.vertexScalarToUV_unnormalized(mesh, vertex_scalars)
        useless = (0, 0, 0, 1)
        meshColor = bt.colorObj(useless, 0.5, 1, 1.6, 0.0, 0.0)
        bt.setMat_texture(mesh, texture_path, meshColor)
        # bpy.ops.object.shade_smooth()

        # bpy.ops.wm.save_mainfile(filepath=os.getcwd() + render_dir + '/test.blend')
        outputPath = os.path.join(cwd, render_dir , str(i).zfill(4) + '.png')

        bt.invisibleGround(location=(0, 0, -100), shadowBrightness=0.0)
        bt.shadowThreshold(shadowThreshold)
        bt.renderImage(outputPath, cam)


