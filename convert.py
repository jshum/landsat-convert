
import os
import re
import numpy
from PIL import Image
import matplotlib

def get_metadata(filename):
   minr_dict = dict()
   maxr_dict = dict()
   qmin_dict = dict()
   qmax_dict = dict()
   f = open(filename)
   for l in f:
      l = l.strip()
      if len(l.split('=')) > 1:
         numval = l.split('=')[1].strip()

      if re.match('^(RADIANCE_MAXIMUM_BAND_([0-9]).+)$',l):
         maxr = re.match('^(RADIANCE_MAXIMUM_BAND_([0-9]).+)$',l)
         maxr_dict[int(maxr.group(2))] = float(numval)
      elif re.match('^(RADIANCE_MINIMUM_BAND_([0-9]).+)$',l):
         minr = re.match('^(RADIANCE_MINIMUM_BAND_([0-9]).+)$',l)
         minr_dict[int(minr.group(2))] = float(numval) 
      elif re.match('^(QUANTIZE_CAL_MIN_BAND_([0-9]).+)$',l):
         qmin = re.match('^(QUANTIZE_CAL_MIN_BAND_([0-9]).+)$',l)
         qmin_dict[int(qmin.group(2))] = float(numval) 
      elif re.match('^(QUANTIZE_CAL_MAX_BAND_([0-9]).+)$',l):
         qmax = re.match('^(QUANTIZE_CAL_MAX_BAND_([0-9]).+)$',l)
         qmax_dict[int(qmax.group(2))] = float(numval)
      elif re.match('^(SUN_ELEVATION.+)$', l):
         sun_elev = float(numval) 
   return {'lmax': maxr_dict, 'lmin' : minr_dict, 'qmin' : qmin_dict, 'qmax' : qmax_dict, 'elev' : sun_elev} 
         
def dn_to_radiance():
   ((lmax - lmin)/(qmax - qmin)) * (dn - qmin) + lmin

def convert_to_radiance(filename, band_num, metadata):
   b = band_num
   im = Image.open(filename)
   im.show()
   imarray = numpy.array(im) 
   radiance = numpy.zeros_like (imarray, dtype=numpy.float32)
   metadata['lmax'][b]
   metadata['lmin'][b]
   metadata['qmax'][b]
   metadata['qmin'][b]
   radiance = ((metadata['lmax'][b] - metadata['lmin'][b]) / (metadata['qmax'][b] - metadata['qmin'][b])) * (imarray - metadata['qmin'][b]) + metadata['lmin'][b]
   outim = Image.fromarray(radiance, mode='F')
   outim.show()

def main():
   loscenes = os.listdir('.')
   for scene in loscenes:
      if os.path.isdir(scene):
         lofiles = os.listdir(scene)     
         lobands = [None] * 8
         for f in lofiles:
            if re.match('.+_MTL.txt$',f):
               metadata = get_metadata(os.path.join(scene,f))
               print metadata
               ''
            elif re.match('.+_B([0-9]).TIF$',f):
               bandtif = re.match('.+_B([0-9]).TIF$',f)
               lobands[int(bandtif.group(1))] = f
         print lobands 
         for band_num in range(len(lobands)):
            if lobands[band_num]:
               print lobands[band_num]
               convert_to_radiance(os.path.join(scene,lobands[band_num]), band_num, metadata)

            
            

if __name__ == "__main__":
        main()
