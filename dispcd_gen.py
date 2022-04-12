
import copy
import os
import sys
import cv2
import time
from pathlib import Path

import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
import open3d as o3d
import pandas as pd
import tqdm
import yaml
from PIL import Image
from sklearn.preprocessing import MinMaxScaler

from PCD_CONFIG import *


class disppcd_gen():

    def __init__(self, cam0_config_path, cam1_config_path): 
        
        self.save_disp = True
        self.do_save_pcd = True
        self.pcd_downsample = False
        self.pcd_outrem = True
        self.verbose = True
        self.img_downsample = True
        
        self.img_dfactor = 2
        self.voxel_size = 0.005
        
        self.save_pcd_rootdir = os.path.join(os.getcwd(), 'pcds')
        self.save_disp_rootdir = os.path.join(os.getcwd(), 'disp')      
        self.save_pcd_prefix = 'pcd_'
        self.save_disp_prefix = 'disp_'
        
        self.cam0_config_path = cam0_config_path
        self.cam1_config_path = cam1_config_path
        
        self.K_cam0, self.D_cam0, self.R_cam0, self.P_cam0 = self.get_camparams_fromconfig(self.cam0_config_path)
        self.K_cam1, self.D_cam1, self.R_cam1, self.P_cam1 = self.get_camparams_fromconfig(self.cam1_config_path)
        
        self.get_camintrinsics()


    def get_camparams_fromconfig(self, cam_config):
        with open(cam_config, "r") as stream:
            cam_params = yaml.safe_load(stream)
        K = np.array(cam_params['camera_matrix']['data']).reshape(3,3)
        D = np.array(cam_params['distortion_coefficients']['data']).reshape(1,5)
        R = np.array(cam_params['rectification_matrix']['data']).reshape(3,3)
        P = np.array(cam_params['projection_matrix']['data']).reshape(3,4)
        
        return K, D, R, P
    # import pdb
    # pdb.set_trace()   

    def get_camintrinsics(self):   
        if self.img_downsample:
            self.P_cam0[:,:3] = self.P_cam0[:,:3] / (self.img_dfactor)
            self.P_cam1[:,:3] = self.P_cam1[:,:3] / (self.img_dfactor)
        else:
            pass
     
        self.baseline = self.P_cam1[0][3] / self.P_cam1[0][0]
        self.f_norm = self.P_cam0[0][0]
        self.Cx = self.P_cam0[0][2]
        self.Cy = self.P_cam0[1][2]
        
    
    
    def read_img(self, img_left_path, img_right_path):        
        self.img_left_path = img_left_path
        self.img_right_path = img_right_path
        
        self.img1 = Image.open(self.img_left_path).convert('L')
        self.img2 = Image.open(self.img_right_path).convert('L')
        
        ## Read RGB image for pcd colors
        self.img1_rgb = Image.open(self.img_left_path)
        
        self.w, self.h = self.img1.size
        
        if self.img_downsample:
            if type(self.img_dfactor) == int:
                self.d_w, self.d_h = int(self.w / self.img_dfactor), int(self.h / self.img_dfactor)
                self.img1 = self.img1.resize((self.d_w, self.d_h))
                self.img2 = self.img2.resize((self.d_w, self.d_h))
                
                self.img1_rgb = self.img1_rgb.resize((self.d_w, self.d_h))
            else:
                print('Provide proper image downsample factor.. Exiting...')
                sys.exit()
            
            self.w, self.h = self.d_w, self.d_h  
        else:
            pass
        
        self.img1 = np.array(self.img1)
        self.img2 = np.array(self.img2)
        self.img1_rgb = np.array(self.img1_rgb)
               
   
    def init_savepath(self):
        if self.do_save_pcd and not(os.path.exists(self.save_pcd_rootdir)):
            os.mkdir(self.save_pcd_rootdir)        
        
        if self.save_disp and not(os.path.exists(self.save_disp_rootdir)):
            os.mkdir(self.save_disp_rootdir)
        
        self.img_dirname = self.img_left_path.split('/')[-2]
        # self.img_id = os.path.basename(self.img_left_path).split('.')[0].split('_')[1]
        self.img_id = os.path.basename(self.img_left_path).split('.')[0]
        
        
        if not(os.path.exists(os.path.join(self.save_pcd_rootdir, self.img_dirname))):
            self.save_pcd_path = os.path.join(self.save_pcd_rootdir, self.img_dirname)
            os.mkdir(self.save_pcd_path)
        else:
            self.save_pcd_path = os.path.join(self.save_pcd_rootdir, self.img_dirname)
        
        if not(os.path.exists(os.path.join(self.save_disp_rootdir, self.img_dirname))):
            self.save_disp_path = os.path.join(self.save_disp_rootdir, self.img_dirname)
            os.mkdir(self.save_disp_path)
        else:
            self.save_disp_path = os.path.join(self.save_disp_rootdir, self.img_dirname)
        

        self.disp_name = self.save_disp_prefix + self.img_id + '.npy'
        self.pcd_name = self.save_pcd_prefix + self.img_id + '.ply'
        
        self.disp_savepath = os.path.join(self.save_disp_path, self.disp_name)
        self.pcd_savepath = os.path.join(self.save_pcd_path, self.pcd_name)
    
    
    def gen_disparity(self):        
        # -----------------------------------------------------------------------
        # CALCULATE DISPARITY (DEPTH MAP)
        #------------------------------------------------------------------------
        # 
        stereo = cv.StereoSGBM_create(minDisparity = min_disp,
                                    numDisparities = num_disp,
                                    # blockSize = blockSize,
                                    P1 = P1,
                                    P2 = P2,
                                    disp12MaxDiff = disp12MaxDiff,
                                    uniquenessRatio = uniquenessRatio,
                                    speckleWindowSize = speckleWindowSize,
                                    speckleRange = speckleRange,
                                    mode = 3
                                    )
        #------------------------------------------------------------------------
        self.disparity_SGBM = stereo.compute(self.img1, self.img2).astype(np.float32)
        self.disparity_SGBM = (self.disparity_SGBM / 16.) 
        

    def gen_pcd(self):        
        
        Z_thresh = 3.5 #3.5 #0.35 
    
        r = np.arange(0,self.w); r = np.stack([r]*self.h)
        c = np.arange(0,self.h); c = np.stack([c]*self.w, axis = 0).transpose()
        
        c_Cx = c - self.Cx; r_Cy = r - self.Cy

        Z = (self.f_norm*self.baseline) / self.disparity_SGBM
        Z_fnorm = Z / self.f_norm
        X = Z_fnorm * c_Cx
        Y = Z_fnorm * r_Cy
        
        pcd = np.zeros((self.w * self.h, 3))
        pcd[:,0] = X.flatten(); pcd[:,1] = Y.flatten(); pcd[:,2] = Z.flatten()
        
        colors = self.img1_rgb.reshape((-1, 3)) / 255.
         
        
        filter_idx = np.where((pcd[:,0] > np.add(pcd[:,0].min(), pcd[:,0].min() * 0.10)) &  ## Filtering 10% higher from the ground
                            #   (np.abs(pcd[:,2]) < Z_thresh)
                              (np.abs(pcd[:,2]) < np.abs((np.median(np.unique(pcd[:,2])))))            ## Filtering Z
                              )[0]  
        
        pcd = pcd[filter_idx]
        pcd[pcd == -np.inf] = 0
        pcd[pcd == np.inf] = 0
        
        colors = colors[filter_idx]
        
        self.pcd = o3d.geometry.PointCloud()
        self.pcd.points = o3d.utility.Vector3dVector(pcd)
        
        self.colors = np.array(colors)
        self.pcd.colors = o3d.utility.Vector3dVector(self.colors)

        # print("pcd downsample t or f: ",self.pcd_downsample)
        if self.pcd_downsample:
            ## Downsample the point cloud with an  apt voxel size
            self.pcd = self.pcd.voxel_down_sample(self.voxel_size) 
            print(" pcd downsample", self.voxel_size)   
                
        
        if self.pcd_outrem:
            ## Outlier Removal (Statistical)
            self.cloud, ind = self.pcd.remove_statistical_outlier(nb_neighbors=50, std_ratio=1.)
            self.pcd = self.cloud ## Overwriting pcd with cloud after outlier removal
        print(np.asarray(self.pcd.points).shape)
        

    def save_disparity(self):
        np.save(self.disp_savepath, self.disparity_SGBM)
        cv2.imwrite(self.disp_savepath.replace('.npy', '.png'), self.disparity_SGBM)
        if self.verbose: 
            print(f'Disparity saved to - {self.disp_savepath}', end=' ')
    

    def save_pcd(self):
        o3d.io.write_point_cloud(self.pcd_savepath, self.pcd)
        if self.verbose: 
            print(f'PCD saved to - {self.pcd_savepath}')
            print(self.pcd)
            


    def viz_pcd(self):
        o3d.visualization.draw_geometries([self.pcd])

