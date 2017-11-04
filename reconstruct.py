#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  1 17:53:05 2017

@author: serkan
"""

import ply
import numpy as np

def reconstruct3d(image,depth_map,camera_parameters,**kwargs):
    """ Reconstructs scene 
    
    Arguments:
    image -- image of the reconstructed scene
    depth_map -- depth map of the image
    camera_parameters -- Camera intrinsic matrix
                                [fx,  0, cx]
                          K =    [ 0, fy, cy]
                                [ 0,  0,  0]
                          where fx,fy is the focal length of the camera
                          and   cx,cy is the principle point of the camera

    Keyword arguments:
    step -- Controls how many 3d points point cloud will have
            if step == 1 all pixels in the image will be converted
            into a point in the cloud (default 1)
    mesh -- If True, resulting Ply object will contain faces,
            Otherwise it will only contain vertices
    
    transformation -- 4x4 matrix that represents a transformation
            Transforms all points with given transformation
            If None, transformation is not applied (None = Identity)
    """ 
    
    step = kwargs.pop('step', 1)
    mesh = kwargs.pop('mesh', False)
    transformation = kwargs.pop('transformation', None)
    
    if (transformation is None):
        transformation = np.identity(4)
    
    
    scene = ply.PLY()
    
    image_width, image_height = image.shape[1], image.shape[0]
    
    inv_intr = np.linalg.inv(camera_parameters)
    
    point_size = (len(range(0,image_width, step)), len(range(0,image_height, step)))
    points = [[None for x in range(point_size[1])] for y in range(point_size[0])]
    
    for v in range(0,image_height, step):
        for u in range(0,image_width, step):
            projected_point = np.array([u, v, 1])
            image_point     = np.matmul(inv_intr, projected_point)
            
            x, y = (image_point[0] / image_point[2]), (image_point[1] / image_point[2])
            
            depth = depth_map[v, u]
            
            Z = depth
            Y = Z * y
            X = Z * x
            
            transformed_point = np.matmul(transformation, np.array([X, Y, Z, 1]))
            transformed_point = transformed_point / transformed_point[3]
            
            p = ply.Vertex(transformed_point[0:3].tolist()) #TODO: READ COLOR FROM ORIGINAL IMAGE
            p.r = image[v,u,0] / 255.0
            p.g = image[v,u,1] / 255.0
            p.b = image[v,u,2] / 255.0
            
            p.texture_coordinates = [u / float(image_width) ,v / float(image_height)]
            
            scene.add_vertex(p)
            
            if (mesh):
                points[int(u/step)][int(v/step)] = p
#            append(p)
    if (mesh):
        for u in range(0,point_size[0] - 1):
            for v in range(0,point_size[1] - 1):
                face = ply.Face([points[u    ][v],
                                 points[u + 1][v],
                                 points[u + 1][v + 1],
                                 points[u    ][v + 1],
                                 ])

                scene.add_face(face)
            
    return scene
