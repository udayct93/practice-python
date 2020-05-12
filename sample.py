import os
count = 0
cdate = '/2020/04/29/'
for filename in os.listdir("D:/Users/turamau/PycharmProjects/gpss-consolidatedmovement/lambda/CMReconProcess{}dev".format(cdate)):
    with open('D:/Users/turamau/PycharmProjects/gpss-consolidatedmovement/lambda/CMReconProcess{}dev/{}'.format(cdate, filename), 'r') as input_data:
        for line in input_data:
            if "david" in line:
                count += 1
                print(filename)
            else:
                print("not fund")
print(count)
