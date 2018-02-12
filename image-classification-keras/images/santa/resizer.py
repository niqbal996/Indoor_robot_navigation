from PIL import Image


size = 640,480

i= 1 

for i in range(1,76):
	im = Image.open("Door_resized(" +str(i) +").jpg")
	im_resized = im.resize(size, Image.ANTIALIAS)
	im_resized.save("Door_resized" + str(i)+ ".jpg","JPEG")


