import shutil
import os
 
# copy all the files in the subfolders to main folder
 
# The current working directory
src_dir = "/Users/sjayakum/Desktop/csci599/StyleNet/MillionSongSubset/clean_midi"
# The generator that walks over the folder tree
walker = os.walk(src_dir)

dest_dir= '/Users/sjayakum/Desktop/csci599/StyleNet/MillionSongSubset/generated_output/'
 
# the first walk would be the same main directory
# which if processed, is
# redundant
# and raises shutil.Error
# as the file already exists
 
rem_dirs = walker.next()[1]
 
for data in walker:
	for files in data[2]:
		try:
			shutil.move(data[0] + os.sep + files, dest_dir)
		except shutil.Error:
			pass

 
