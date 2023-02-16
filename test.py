with open("UMLs/txt_files/Calibration.txt","r") as cal:
    caldata = cal.read().replace('\n', '')

with open("UMLs/txt_files/v1.txt", "r") as v1:
    v1data = v1.read().replace('\n', '')

print(v1data==caldata)