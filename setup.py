# creating executable here
from distutils.core import setup
import py2exe, sys, os#,numpy
from Tkinter import *
from operator import itemgetter
import time,string,math
import cv2
import numpy as np
from PIL import Image, ImageTk

setup(
    options = {'py2exe': {'bundle_files': 3, 'includes': 'numpy',
                "dll_excludes": [
                'api-ms-win-core-libraryloader-l1-2-2.dll',#missing
                'api-ms-win-core-largeinteger-l1-1-0.dll',#missing
                'api-ms-win-core-heap-l1-2-0.dll',#missing
                'api-ms-win-core-heap-l2-1-0.dll',#missing
                'api-ms-win-core-rtlsupport-l1-2-0.dll',#missing
                'api-ms-win-core-libraryloader-l1-2-0.dll',#missing
                'api-ms-win-core-registry-l2-2-0.dll',#missing
                'api-ms-win-security-base-l1-2-0.dll',#missing
                'api-ms-win-core-com-l1-1-1.dll',#missing
                'api-ms-win-mm-time-l1-1-0.dll',#missing
                'api-ms-win-core-version-l1-1-1.dll',#missing
                                 ]} },
    console=['4D Rendering Tool 4.py'],
    zipfile = None,
)
