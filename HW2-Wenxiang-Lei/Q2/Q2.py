 #!/usr/bin/env python

# -*- coding:utf-8 -*-


import csv

with open('nepal.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile)
    y07=[]
    y08=[]
    y09=[]
    y10=[]
    y11=[]
    disName=[]
    data=[]

    for line in reader:

      if line[1] == "2007":
          y07.append(line[2])

      elif line[1] == "2008":
          y08.append(line[2])
          disName.append(line[0])

      elif line[1] == "2009":
          y09.append(line[2])

      elif line[1] == "2010":
          y10.append(line[2])

      elif line[1] == "2011":
          y11.append(line[2])

csvfile = file('new_nepal.csv', 'wb')
writer = csv.writer(csvfile)
writer.writerow(['District', '2007', '2008', '2009', '2010', '2011'])

for i in range(75):
  data.append([disName[i],y07[i],y08[i],y09[i],y10[i],y11[i]])

writer.writerows(data)
csvfile.close()
