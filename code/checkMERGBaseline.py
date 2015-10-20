import time
import subprocess
import os
import glob
import numpy as np
from netCDF4 import Dataset, date2num
from datetime import datetime


def main():
	check_merg_file_differences("/Users/kwhitehall/Documents/capstones/usc2015/baselineTimingscopy1/test/MERGnetcdfCEs",
								"/Users/kwhitehall/Documents/capstones/usc2015/baselineTimingscopy2/test/MERGnetcdfCEs",
								"/Users/kwhitehall/Documents/capstones/usc2015/diff")

#*********************************************************************************************************************
def check_merg_file_differences(baselinePath1, baselinePath2,  outputDir):
	'''
        Purpose:: To compare MERG files cloud elements from two directories

        Input:: baselinePath1: a string representing the path to the files
        	 	baselinePath2: a string representing the path to the files
        	 	outputDir: a string representing the path to store the results at
                

        Output::
                diffDir: the path to a directory with the differences 
                diffDirText: a text file with the differences logged. This is stored in diffDir

        Assumptions:: 

    '''
	dir1Filenames = []
	dir2Filenames = []
	diffNames = []

	if not os.path.exists(baselinePath1):
		print 'Please check inputs. No folder named %s ' %baselinePath1
		return
	else:
		dir1Filenames = [os.path.basename(x) for x in glob.glob(baselinePath1+'/*.nc')]
		
	if not os.path.exists(baselinePath2):
		print 'Please check inputs. No folder named %s ' %baselinePath2
		return
	else:
		dir2Filenames = [os.path.basename(x) for x in glob.glob(baselinePath2+'/*.nc')]
		
	if not os.path.exists(outputDir):
		os.mkdir(outputDir)

	diffLog = open(outputDir+'/diffLog.txt','wb')
	diffLog.write('\n baselinePath1 is %s ' %baselinePath1)
	diffLog.write('\n baselinePath2 is %s ' %baselinePath2)

	# 1. Check if there are differences in the filenames
	diffNames = list(set(dir1Filenames) - set(dir2Filenames))
	if len(diffNames) == 0:
		diffLog.write('\n Differences in filenames: None')
		print 'Differences in filenames: None'
	else:
		diffLog.write('\n Differences in filenames: \n')
		print 'Differences in filenames: \n'

		for eachFile in diffNames:
			diffLog.write('%s\n' %eachFile)
			print '%s' %eachFile
		diffLog.write(('*')*80)
		print ('*')*80
		return

	#2. Check the content of each pair of similarly names files using nco ncdiff
	print 'checking the content \n'
	for i in xrange(len(dir1Filenames)):
		print ('-'*80)
		print '%s/%s and %s/%s ' %(baselinePath1, dir1Filenames[i], baselinePath2, dir2Filenames[i])

		# open the two files and diff the arrays
		file1 = Dataset(baselinePath1+'/'+dir1Filenames[i], 'r', format='NETCDF4')
		file1Data = file1.variables['brightnesstemp'][:,:,:]

		file2 = Dataset(baselinePath2+'/'+dir2Filenames[i], 'r', format='NETCDF4')
        file2Data = file2.variables['brightnesstemp'][:,:,:]

        if np.array_equal(file1Data, file2Data):
        	diffLog.write('%s/%s and %s/%s are equal \n' %(baselinePath1, dir1Filenames[i], baselinePath2, dir2Filenames[i]))
        	print '%s/%s and %s/%s are equal' %(baselinePath1, dir1Filenames[i], baselinePath2, dir2Filenames[i])
        else:
        	diffLog.write('\n** %s/%s and %s/%s are NOT equal. Check the outputDir for the diff file.\n' %(baselinePath1, dir1Filenames[i], baselinePath2, dir2Filenames[i]))
        	print '** %s/%s and %s/%s are NOT equal. Check the outputDir for the diff file.\n'%(baselinePath1, dir1Filenames[i], baselinePath2, dir2Filenames[i])
        	file1 = Dataset(baselinePath1+'/'+dir1Filenames[i], 'r', format='NETCDF4')
        	alllatsraw = file1.variables['latitude'][:]
        	alllonsraw = file1.variables['longitude'][:]
        	timesraw = file1.variables['time'][:]
        	file1.close

        	LON, LAT = np.meshgrid(alllonsraw, alllatsraw)

        	diff = Dataset(outputDir+'/'+dir1Filenames[i], 'w', format='NETCDF4')
        	diff.description = 'Difference between '+dir1Filenames[i]+' & '+dir2Filenames[i]
        	diff.calendar = 'standard'
        	diff.conventions = 'COARDS'
        	diff.createDimension('time', None)
        	diff.createDimension('lat', len(LAT[:,0]))
        	diff.createDimension('lon', len(LON[0,:]))

        	tempDims = ('time', 'lat', 'lon',)
        	times = diff.createVariable('time', 'f8', ('time',))
        	latitude = diff.createVariable('latitude', 'f8', ('lat',))
        	longitude = diff.createVariable('longitude', 'f8', ('lon',))
        	brightnesstemp = diff.createVariable('brightnesstemp', 'i16', tempDims)
        	brightnesstemp.units = 'Kelvin'

        	# write NETCDF data
        	times[:] = timesraw
        	longitude[:] = LON[0, :]
        	longitude.units = 'degrees_east'
        	longitude.long_name = 'Longitude'
        	latitude[:] = LAT[:, 0]
        	latitude.units = 'degrees_north'
        	latitude.long_name = 'Latitude'
        	brightnesstemp[:] = file1Data - file2Data

        	diff.close

	diffLog.close()
	return
main()
