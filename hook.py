import os
import sys

# environment parameters
os.environ['PROJ_LIB'] = os.path.dirname(sys.argv[0])
os.environ['GDAL_DATA'] = os.path.dirname(sys.argv[0]) + r'\gdal'
os.environ['PROJ_DATA'] = os.environ['PATH'].split(";")[0]+ r'\Library\share\proj'
print(os.environ)