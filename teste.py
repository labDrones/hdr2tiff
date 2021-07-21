import imageio
import matplotlib.pyplot as plt
import cv2
hdr_path = 't1\\raw_0.hdr'
# im = imageio.imread(hdr_path, format='HDR-FI')
im = cv2.imread(hdr_path, flags=cv2.IMREAD_ANYDEPTH)
print(im)
imgplot = plt.imshow(im)
plt.show()



# IMREAD_ANYDEPTH is needed because even though the data is stored in 8-bit channels
# when it's read into memory it's represented at a higher bit depth