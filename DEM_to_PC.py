import numpy as np
import pandas as pd
import lidario as lio
import open3d as o3d
from plyfile import PlyData, PlyElement

'''
This code is written to convert a DEM geotiff to a point cloud / mesh of elevations for use in 3D software.
'''

# Path to DEM
dem = "DEM.tif"

# Create a Translator object which will take a tif file and return a np.array
translator = lio.Translator("geotiff", "dataframe")

# Translate the tif file and get the np.array
point_cloud = translator.translate(dem, no_data=0, band=1)

print("Point Cloud Created")

# Scale DEM (otherwise it comes out very small)
point_cloud['x'] = point_cloud['x'] * 100 # Adjust values according to DEM range
point_cloud['y'] = point_cloud['y'] * 100
point_cloud['z'] = point_cloud['z'] * 0.003

# Convert DataFrame to numpy ndarray
data = point_cloud[['x', 'y', 'z']].values

# Create a list of tuples where each tuple is a row in your ndarray
data = [tuple(row) for row in data]

# Define the PlyElement. Specify the data and the properties
vertex = PlyElement.describe(
    np.array(data, dtype=[('x', 'f4'), ('y', 'f4'), ('z', 'f4')]),
    'vertex'
)

# Write the .ply file
PlyData([vertex], text=True).write('Point_Cloud.ply')
print("Point Cloud Written")

'''
# USE THIS CODE FOR ROUGH MESH
# I RECOMMEND USING 3RD PARTY SOFTWARE FOR MESHING

# Read point cloud from file
point_cloud = o3d.io.read_point_cloud("Point_Cloud.ply")

# Estimate normals
point_cloud.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30))
print("Normals Estimated")

# Create mesh using Poisson surface reconstruction with increased depth
poisson_mesh, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(point_cloud,
                                                                                    depth=11 ) # Adjust depth to desired resolution: Larger depth means more detail
print("Mesh Created")

# Extract the triangle mesh
mesh = poisson_mesh

o3d.io.write_triangle_mesh("Poisson_Mesh.ply", mesh)
print("Mesh Written")

# o3d.visualization.draw_geometries([mesh])
'''