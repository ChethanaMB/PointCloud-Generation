from importlib.resources import path
import os
import open3d as o3d
import tqdm
from pathlib import Path

# from PCD_CONFIG import *
from dispcd_gen import *

import pdb
pdb.set_trace()
stereoimg_rootdir = r"/media/storage/ATV_Data/2-1-22/day_cart_data_Jan_31_2022/image_gps_data/20220131_105851"

#pcd_rootdir = r'C:\Users\Chethana\Desktop\feb 11\20220131_114013\pcds\20220131_114013'

output_dir = r"/home/chethana/Outputs"
try:
    os.makedirs(output_dir)
except:
    pass
output_dir = os.path.join(output_dir,os.path.basename(stereoimg_rootdir))
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

dpcdgen.pcd_outrem = False

dpcdgen.pcd_downsample = False

for left_img, right_img in zip(sorted(Path(os.path.join(stereoimg_rootdir)).glob('20220131_114011_left_*.png')),
                                sorted(Path(os.path.join(stereoimg_rootdir)).glob('20220131_114011_right_*.png'))):
    
    dpcdgen.read_img(str(left_img), str(right_img))
    dpcdgen.init_savepath()
    dpcdgen.gen_disparity()
    dpcdgen.gen_pcd()
    
    dpcdgen.save_disparity()
    dpcdgen.save_pcd()
