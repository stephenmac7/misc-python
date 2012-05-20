from math import sqrt
def distance(co1, co2):
  td = sqrt((co1[0] - co2[0])**2 + (co1[1] - co2[1])**2)
  return td
co1 = [float(input("Coordinate 1 (x): ")), float(input("Coordinate 1 (y): "))]
co2 = [float(input("Coordinate 2 (x): ")), float(input("Coordinate 2 (y): "))]
answer = round(distance(co1, co2),2)
print("Distance: ", answer)
