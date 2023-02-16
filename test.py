with open("UMLs/txt_files/Calibration.txt","r") as cal:
    caldata = cal.read().replace('\n', '').lower()

with open("UMLs/txt_files/v1.txt", "r") as v1:
    v1data = v1.read().replace('\n', '').lower()

print(v1data==caldata)
statement = v1data==caldata
