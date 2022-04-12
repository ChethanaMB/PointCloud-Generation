
## Camera config file
cam0_config_path = r"/media/storage/ATV_Data/2-1-22/day_cart_data_Jan_31_2022/image_gps_data/20220131_110712/18497314.yaml"#r"D:\Dimaag\K\K\CMU_DATA\Test_3view\20220128_130900\18497314.yaml"
cam1_config_path = r"/media/storage/ATV_Data/2-1-22/day_cart_data_Jan_31_2022/image_gps_data/20220131_110712/18497315.yaml"#r"D:\Dimaag\K\K\CMU_DATA\Test_3view\20220128_130900\18497315.yaml"

# Disparity Parameters

# NewCamera Params
window_size = 0
min_disp = 32
max_disp = 160#384 #224 #208 #128 #80    #224 --> 0.5m 
num_disp = max_disp - min_disp
blockSize = 1
# P1 = 8 * 3 * window_size ** 2
# P2 = 32 * 3 *window_size ** 2

P1 = 8 * window_size ** 2
P2 = 32 * window_size ** 2

disp12MaxDiff = 1
uniquenessRatio =10
speckleWindowSize = 100
speckleRange = 1




# #cane_type check
# window_size = 3
# min_disp = 0
# max_disp = 464
# num_disp = max_disp
# # blockSize = 1
# P1 = 8 * window_size ** 2
# P2 = 32 * window_size ** 2
# disp12MaxDiff = max_disp + 32
# uniquenessRatio = 15
# speckleWindowSize = 200
# speckleRange = 1


# ## BOTTOM SPUR TYPE**************
# window_size = 0
# min_disp = 0 #80
# num_disp = 304 - min_disp
# blockSize = 1
# P1 = 8 * window_size ** 2
# P2 = 32 * window_size ** 2
# disp12MaxDiff = 1
# uniquenessRatio = 5
# speckleWindowSize = 100
# speckleRange = 1

# ## BOTTOM SPUR TYPE -- Hearse Vineyard**************
# window_size = 3
# min_disp = 0 #80
# max_disp = 288
# num_disp = max_disp
# blockSize = 1
# P1 = 8 * window_size ** 2
# P2 = 32 * window_size ** 2
# disp12MaxDiff = max_disp + 32
# uniquenessRatio = 15
# speckleWindowSize = 30
# speckleRange = 1

# ## BOTTOM SPUR TYPE -- Hearse Vineyard -- ImgSize - 1024X768**************
# window_size = 0
# block_size = 0
# min_disp = 0
# max_disp = 128
# num_disp = max_disp 
# uniquenessRatio = 0
# speckleWindowSize = 100
# speckleRange = 1
# disp12MaxDiff = max_disp + 32
# P1 = 8 * window_size ** 2
# P2 = 32 * window_size ** 2

# ## BOTTOM SPUR TYPE -- Hearse Vineyard -- ImgSize - 2048X1536********
# window_size = 3
# min_disp = 16
# max_disp = 276
# num_disp = max_disp
# # blockSize = 1
# P1 = 8 * window_size ** 2
# P2 = 32 * window_size ** 2
# disp12MaxDiff = max_disp + 32
# uniquenessRatio = 30
# speckleWindowSize = 300
# speckleRange = 1


# ## 20220112_212358_pcds Dr.Abhi********
# window_size = 3
# min_disp = 0
# max_disp = 276
# num_disp = max_disp
# # blockSize = 1
# P1 = 8 * window_size ** 2
# P2 = 32 * window_size ** 2
# disp12MaxDiff = max_disp + 32
# uniquenessRatio = 60
# speckleWindowSize = 30
# speckleRange = 1




