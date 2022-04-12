from importlib.resources import path
import os
import open3d as o3d
import tqdm
from pathlib import Path

# from PCD_CONFIG import *
from dispcd_gen import *

# import pdb
# pdb.set_trace()
rootdir = '/media/storage/ATV_Data/1-18-21/day_cart_data_Jan_13_2022/image_gps_data'
for folder in os.listdir(rootdir):
    stereoimg_rootdir = os.path.join(rootdir, folder)
    # print(stereoimg_rootdir)
# stereoimg_rootdir = r"/media/storage/ATV_Data/1-18-21/day_cart_data_Jan_11_2022/image_gps_data/20220111_164734"

#pcd_rootdir = r'C:\Users\Chethana\Desktop\feb 11\20220131_114013\pcds\20220131_114013'

    output_dir = r"/home/chethana/Outputs"
    try:
        os.makedirs(output_dir)
    except:
        pass
    output_dir = os.path.join(output_dir,"13th jan",os.path.basename(stereoimg_rootdir))
    try:
        os.makedirs(output_dir)
    except:
        pass


    dpcdgen = disppcd_gen(cam0_config_path, cam1_config_path)
    dpcdgen.save_pcd_rootdir = os.path.join(stereoimg_rootdir,'pcds')
    dpcdgen.save_disp_rootdir = os.path.join(stereoimg_rootdir,'disp')

    dpcdgen.img_downsample = True

    # for dir in sorted(os.listdir(stereoimg_rootdir)): 
    # dpcdgen.save_pcd_rootdir = os.path.join(stereoimg_rootdir, dir, 'pcds')
    # dpcdgen.save_disp_rootdir = os.path.join(stereoimg_rootdir, dir, 'disp')

    dpcdgen.save_pcd_rootdir = os.path.join(output_dir, 'pcds')
    dpcdgen.save_disp_rootdir = os.path.join(output_dir, 'disp')


    dpcdgen.img_downsample = True

    dpcdgen.cam_params_downsample = True

    dpcdgen.pcd_outrem = True

    dpcdgen.pcd_downsample = False


    for left_img, right_img in zip(sorted(Path(os.path.join(stereoimg_rootdir)).glob('left_*.png')),
                                    sorted(Path(os.path.join(stereoimg_rootdir)).glob('right_*.png'))):
        
        dpcdgen.read_img(str(left_img), str(right_img))
        dpcdgen.init_savepath()
        dpcdgen.gen_disparity()
        dpcdgen.gen_pcd()
        
        dpcdgen.save_disparity()
        dpcdgen.save_pcd()
