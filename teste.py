from spectral import *
import spectral.io.envi as envi


# lib = envi.read_envi_header(r't1\raw_0.hdr')

# print(lib)
# # Get wavelengths and convert to NumPy array
# wavelengths = lib['wavelength'] #.split(',')[0:-1]
# # wavelengths = [float(w) for w in wavelengths]
# for i, wave in enumerate(wavelengths):
#     print(i, wave)
# # wavelengths = numpy.array(wavelengths)

# IMREAD_ANYDEPTH is needed because even though the data is stored in 8-bit channels
# when it's read into memory it's represented at a higher bit depth


for i in range(1, 271):
    if 270%i == 0:
        print(i)