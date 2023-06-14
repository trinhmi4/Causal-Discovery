import random
import csv 
mylist = [ ## z = 0
          "-z, -x, -m ,- y", "-z, -x, -m ,y", "-z, -x, m ,- y", "-z, -x, m , y",
          "-z, x, -m ,- y", "-z, x, -m , y", "-z, x, m ,- y", "-z, x, m , y",
          ### z = 1
          "z, -x, -m ,- y", "z, -x, -m ,y", "z, -x, m ,- y", "z, -x, m , y",
          "z, x, -m ,- y", "z, x, -m , y", "z, x, m ,- y", "z, x, m , y",]

w = [0.0392, 0.0098, 0.1372, 0.0588, 0.0399, 0.0021, 0.05355, 0.00945,
     0.0286, 0.0234, 0.0832, 0.1248, 0.1014, 0.0546, 0.117, 0.117]

data = random.choices(mylist, weights = w, k = 500)

with open('pharm_data.csv', 'w', encoding='UTF8') as f:
    writer = csv.writer(f)
    # write the header
    writer.writerow(["Z", "X", "M", "Y"])
    # write the data 
    for row in data:
        d = row.split(",")
        writer.writerow(d)
