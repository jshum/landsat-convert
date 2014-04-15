
import os
import re

def process_file(filename):
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
         maxr_dict[maxr.group(2)] = numval
      elif re.match('^(RADIANCE_MINIMUM_BAND_([0-9]).+)$',l):
         minr = re.match('^(RADIANCE_MINIMUM_BAND_([0-9]).+)$',l)
         minr_dict[minr.group(2)] = numval 
      elif re.match('^(QUANTIZE_CAL_MIN_BAND_([0-9]).+)$',l):
         qmin = re.match('^(QUANTIZE_CAL_MIN_BAND_([0-9]).+)$',l)
         qmin_dict[qmin.group(2)] = numval 
      elif re.match('^(QUANTIZE_CAL_MAX_BAND_([0-9]).+)$',l):
         qmax = re.match('^(QUANTIZE_CAL_MAX_BAND_([0-9]).+)$',l)
         qmax_dict[qmax.group(2)] = numval 
      print maxr_dict, minr_dict, qmin_dict, qmax_dict
         

def main():
   loscenes = os.listdir('.')
   for scene in loscenes:
      if os.path.isdir(scene):
         lofiles = os.listdir(scene)     
         for f in lofiles:
            if re.match('.+_MTL.txt',f):
   
               process_file(os.path.join(scene,f))
               break

if __name__ == "__main__":
        main()
