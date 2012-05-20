#!/usr/bin/python3
import math
a = float(input("a: "))
b = float(input("b: "))
c = float(input("c: "))
x1 = (-b+math.sqrt(b*b-4*a*c))/(2*a)
x2 = (-b-math.sqrt(b*b-4*a*c))/(2*a)
def isWhole(xval):
  if(xval%1 == 0):
    return True
  else:
    return False
x1whole = isWhole(x1)
x2whole = isWhole(x2)
if(x1whole == True):
  prin1 = str(int(x1))
else:
  prin1 = str(round(x1,2))
if(x2whole == True):
  prin2 = str(int(x2))
else:
  prin2 = str(round(x2,2))
print(prin1 + " and " + prin2)
##############################
#            TODO            #
# - Add discriminant:        #
#     b*b-4*a*c              #
# - Add non-discriminant:    #
#     -b/2a                  #
##############################
