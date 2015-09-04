
import numpy as np
import argparse
import cv2

def order_points(pts):
	#define rectangle
	rect = np.zeros((4, 2), dtype = "float32")
 
	#tl and br will have min and max of x+y resp
	s = pts.sum(axis = 1)
	rect[0] = pts[np.argmin(s)]
	rect[2] = pts[np.argmax(s)]
 
	#tr and bl will have min and max of diff(x-y) resp
	diff = np.diff(pts, axis = 1)
	rect[1] = pts[np.argmin(diff)]
	rect[3] = pts[np.argmax(diff)]
 
	return rect

def four_point_transform(image, pts):
	
	rect = order_points(pts)
	(tl, tr, br, bl) = rect
 
	# width of new image will be max of dist between (br and bl) ans (tr and tl)
	widthmaxA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
	widthmaxB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
	maxWidth = max(int(widthmaxA), int(widthmaxB))
 
	# height of new image will be max of dist between (tr and br) ans (tl and bl)
	heightmaxA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
	heightmaxB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
	maxHeight = max(int(heightmaxA), int(heightmaxB))
 
	# Specifying points in the order of tl,tr,br,bl
	dst = np.array([
		[0, 0],
		[maxWidth - 1, 0],
		[maxWidth - 1, maxHeight - 1],
		[0, maxHeight - 1]], dtype = "float32")
 
	
	M = cv2.getPerspectiveTransform(rect, dst)
	warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
 
	
	return warped
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", help = "path to the image file")
ap.add_argument("-c", "--coords",
	help = "comma seperated list of source points")
args = vars(ap.parse_args())
 

image = cv2.imread(args["image"])
pts = np.array(eval(args["coords"]), dtype = "float32")
 
warped = four_point_transform(image, pts)
 
# show the original and warped images
cv2.imshow("Original", image)
cv2.imshow("Warped", warped)
cv2.waitKey(0)
