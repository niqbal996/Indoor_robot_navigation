import os
from shutil import move

dataset = 'images'
pos     = dataset + '/door/'
neg     = dataset + '/notdoor/'
files_positive = os.listdir(pos)
files_negative = os.listdir(neg)
current_file = ''

for key in range(0, len(files_positive)):
    current_file = '%06d' % key + '.jpg'
    os.rename((pos + files_positive[key]), current_file)
    move(current_file, (pos + current_file))

for key in range(0, len(files_negative)):
    current_file = '%06d' % key + '.jpg'
    os.rename((neg + files_negative[key]), current_file)
    move(current_file, (neg + current_file))



print ('[INFO] Output status ' + str(len(files_positive)) + ' positive and ' + str(len(files_negative)) + ' negative files have been renamed and moved')