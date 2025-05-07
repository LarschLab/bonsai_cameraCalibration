import traceback

import clr
clr.AddReference("OpenTK")
clr.AddReference("OpenCV.Net")
from System.Collections.Generic import IList
from OpenCV.Net import CV, Point2f, Mat,Depth

from OpenTK import Vector2, Vector3
from System import Array, Single, Random,Tuple




def prepVariables(projected,detected,projectionProps):

	pl=[] # list 'projected list' with dot coordinates for projection
	dl=[] # list 'detected list' with coordinates of detected dots

	dotList=[] # list for all dots (shaped for .Net array building)
	try:
		
		for i in range(4):
			xp=projected[i].Item1
			yp=projected[i].Item2

			
			dsx=projectionProps.Item1 #scale x
			dshx=projectionProps.Item2 #shift x
			dsy=projectionProps.Item3 #scale y
			dshy=projectionProps.Item4 #shift y
			#apply shift and scale to projected dots
			xp=xp#*dsx+dshx
			yp=yp#*dsy+dshy

			#populate list of projected dots
			pl.append([xp,yp])

			#dlOld=dl

			xd=detected[i].Centroid.X
			yd=detected[i].Centroid.Y
			#populate list of detected dots
			dl.append([int(xd),int(yd)])

			dotList.append(pl[i][0])
			dotList.append(pl[i][1])
			dotList.append(dl[i][0])
			dotList.append(dl[i][1])
		
		dst=Array[Point2f]([Point2f(dotList[0],dotList[1]),Point2f(dotList[4],dotList[5]),Point2f(dotList[8],dotList[9]),Point2f(dotList[12],dotList[13])])
		
		
		src=Array[Point2f]([Point2f(dotList[2],dotList[3]),Point2f(dotList[6],dotList[7]),Point2f(dotList[10],dotList[11]),Point2f(dotList[14],dotList[15])])
		
		values = Array[float]([1,1,1,1,1,1,1,1,1])		
		#define placeholder matrix to receive the output of function GetPerspectiveTransform
		transformationMatrix = Mat.FromArray(values, 3, 3, Depth.F64, 1)
	except:
		
		print 'return empty matrix'
		print traceback.format_exc()
		dst=[]
		src=[]
		transformationMatrix=[]

	return dst, src, transformationMatrix


def MatToList(mat):
	matList=[]
	
	for i in range(3):
		for j in range(3):
			va=float(mat.Item[i*3+j].Val0)
			da=(va)
			s = "%0.8f" % da
			matList.append(s) 
			
	return matList



# perspective transformation using calibration matrix to match camera and projector coordinates
def transf(x,y,transformationMatrixString):
  transformationMatrixArray = Array[float]([float(el) for el in transformationMatrixString.split()])

  transformationMatrix = Mat.FromArray(transformationMatrixArray, 3, 3, Depth.F64, 1)

  PointToProject = Array[float]([x,y])
  tempPoint = Array[float]([1,1])

  PointToProjectMat = Mat.FromArray(PointToProject, 1, 1, Depth.F64,2)
  CorrectedPoint = Mat.FromArray(tempPoint, 1, 1, Depth.F64,2) #placeholder variable for output of perspectiveTransform

  CV.PerspectiveTransform(PointToProjectMat,CorrectedPoint,transformationMatrix)

  x=CorrectedPoint.Item[0].Val0 #get the corrected X
  y=CorrectedPoint.Item[0].Val1 #get the corrected Y

  return x,y

def toGL(c,cMax):
  return (2.*(c-cMax/2.))/cMax
  