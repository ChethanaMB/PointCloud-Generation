# import os
  
# # path
# path = '/media/storage/ATV_Data/1-7-21/day_cart_data_01_05_2022_spur/image_gps_data/20220105_123013'
  
# # Split the path in 
# # head and tail pair
# head_tail = os.path.split(path)
  
# # print head and tail
# # of the specified path
# print("Head of '% s:'" % path, head_tail[0])
# print("Tail of '% s:'" % path, head_tail[1], "\n")


import os
rootdir = '/media/storage/ATV_Data/1-7-21/day_cart_data_01_05_2022_spur/image_gps_data'

for file in os.listdir(rootdir):
    stereoimg_rootdir = os.path.join(rootdir, file)
    print(stereoimg_rootdir)
  
