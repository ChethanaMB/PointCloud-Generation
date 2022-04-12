import numpy as np
import open3d as o3d   

def main():
    cloud = o3d.io.read_point_cloud("/home/chethana/Outputs/20220105_123013/pcds/20220105_123013/pcd_left_6.ply") # Read the point cloud
    o3d.visualization.draw_geometries([cloud]) # Visualize the point cloud     

if __name__ == "__main__":
    main()