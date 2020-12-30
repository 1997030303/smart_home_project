import numpy as np
import matplotlib.pyplot as plt

#DECLARING PRODUCTS FOR POWER CONSUMPTIONS AND THEIR TIME OF USAGE
#PRIORITY: 1 IS HIGH(NOT SHIFTABLE), 2 IS MEAN(SHIFTABLE BUT ABOUT 2-3H), 3 IS LOW(SHIFTABLE BUT SHOULD BE IN DAY TIME) AND 4 IS LOWEST(TIME DOES NOT MATTER) PRIORITY.
PRODUCTS = {
    'pc_vacuumcleaner': {
    'w': 890,
    'hours': [20],
    'priority': 3},

    'pc_laptop1': {
    'w': 65,
    'hours': [17, 18, 19, 20],
    'priority': 4},

    'pc_laptop2': {
    'w': 65,
    'hours': [17, 18, 19, 20],
    'priority': 4},

    'pc_phonecharger1': {
    'w': 10,
    'hours': [17, 18, 19, 20],
    'priority': 4},

    'pc_phonecharger2': {
    'w': 10,
    'hours': [17, 18, 19, 20],
    'priority': 4},

    'pc_phonecharger3': {
    'w': 10,
    'hours': [17, 18, 19, 20],
    'priority': 4},

    'pc_phonecharger4': {
    'w': 10,
    'hours': [17, 18, 19, 20],
    'priority': 4},

    'pc_powerbank1': {
    'w': 12,
    'hours': [17, 18, 19, 20],
    'priority': 4},

    'pc_powerbank2': {
    'w': 12,
    'hours': [17, 18, 19, 20],
    'priority': 4},

    'pc_tv': { 
    'w': 98,
    'hours':[19, 20, 21, 22],
    'priority': 3},

    'pc_livingroomlight': {
    'w': 20,
    'hours': [0, 1, 19, 20, 21, 22, 23],
    'priority': 1},

    'pc_kitchenlight': {
    'w': 20,
    'hours': [7, 8, 19, 20],
    'priority': 1},

    'pc_bedroomlight': {
    'w': 53,
    'hours': [21, 22],
    'priority': 1},
    
    'pc_iron': {
    'w': 360,
    'hours':[21],
    'priority': 3},         #NOT USING FOR ONE FULL HOUR (2400W*0.15h)

    'pc_deepfreezer': {
    'w': 21,
    'hours':[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23],
    'priority': 1},

    'pc_refrigerator':{
    'w': 125,
    'hours':[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23],
    'priority': 1},

    'pc_kettle': {
    'w': 300,               #NOT USING FOR ONE FULL HOUR (2025W*0.15h)
    'hours':[7, 17],
    'priority': 3},

    'pc_combiboiler': {
    'w': 125,
    'hours':[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23],
    'priority': 1},

    'pc_toaster': {
    'w': 400,               #NOT USING FOR ONE FULL HOUR (1600W*0.25h)
    'hours':[7],
    'priority': 2},

    'pc_washingmachine': {
    'w': 500,
    'hours':[20, 21],
    'priority': 4},

    'pc_dryer': {
    'w': 1000,
    'hours':[21],
    'priority': 4},

    'pc_blowdrier': {
    'w': 200,               #NOT USING FOR ONE FULL HOUR (2000W*0.1h)
    'hours': [7],
    'priority': 3}
    }

#CREATING AND FILLING TIME INTERVALS TO PLOT
hours = {}
for i in range (0, 24):
    hours["{}.00-{}.00".format(i, i+1)] = 0

for a, b in PRODUCTS.items():           #BECAUSE OF USING A PYTHON DICTIONARY IN A DICTIONARY, USING TWO ITERATORS SUCH AS a AND b IS NEEDED. a IS FOR THE PRODUCT NAMES(strings) AND b IS FOR THEIR ATTRIBUTES(dictionaries)
    for y in range(len(b['hours'])):
        hours["{}.00-{}.00".format(b['hours'][y], b['hours'][y]+1)]=hours["{}.00-{}.00".format(b['hours'][y], b['hours'][y]+1)]+b['w']

print("INITIAL POWER CONSUMPTIONS WITHOUT BATTERY:", hours)

#BATTERY SPECIFICATIONS
batterycap = max(hours.values())/2
batterychargerate = batterycap*0.2
batterydischargerate = batterycap*0.3
battery_lowthreshold = batterycap*0.3
battery_highthreshold = batterycap*0.8
battery_current = batterycap*0.1

print("Battery capacity:" , batterycap, "Wh")
print("Battery charge rate:" , batterychargerate, "W")
print("Battery discharge rate:" , batterydischargerate, "W")
print("Initial battery charge:" , battery_current, "W")

#ISTANBUL SUNSHINE DURATION FOR FEBRUARY(3H) AND AUGUST(10H) ACCORDING TO "MGM"
sunshine_duration = 3

#UPDATING HOURLY CONSUMPTIONS WITH BATTERY STATE
for i in range(0,24):
    if i >= 7 and i < 20 and battery_current+batterychargerate<battery_highthreshold and sunshine_duration>0:          #CHARGE BATTERY BETWEEN 08.00-18.00 IN FEBRUARY AND 07.00-20.00 IN AUGUST
        sunshine_duration = sunshine_duration-1
        battery_current = battery_current+batterychargerate
        print("Battery charged at", i,". 00, Current battery charge: ", battery_current, "Wh")
    if i >= 17 and i < 23 and battery_current-batterydischargerate>battery_lowthreshold and hours["{}.00-{}.00".format(i, i+1)]-batterydischargerate>0 :      #DISCHARGE BETWEEN 17.00-22.00
        hours["{}.00-{}.00".format(i, i+1)]=hours["{}.00-{}.00".format(i, i+1)]-batterydischargerate
        battery_current = battery_current-batterydischargerate
        print("Battery discharged at", i,". 00, Current battery charge: ", battery_current, "Wh")

print("POWER CONSUMPTIONS WITH BATTERY:", hours)

#WARNING USER ABOUT POWER CONSUMPTION INTERVALS THAT GO OVER 1250W.
totalpc = 0
for i in hours:
    totalpc = totalpc + hours[i]
    if hours[i] >1250:
        print("WARNING! {} is greater than 1250W!".format(i))

#CALCULATING ENERGY COST ACCORDING TO "EPDK" (2020 DATA)
cost=0
for i in range(0,24):
    cost = cost + hours["{}.00-{}.00".format(i, i+1)] * 60.5082
print("DAILY COST w/ CONSTANT PRICING : " + str(cost/100000) + "TL")

cost=0
for i in range(0,24):
    if i >= 6 and i <= 16:
        cost = cost + hours["{}.00-{}.00".format(i, i+1)] * 61.2766
    if i >= 17 and i <= 21:
        cost = cost+hours["{}.00-{}.00".format(i, i+1)] * 89.2578
    else:
        cost = cost + hours["{}.00-{}.00".format(i, i+1)] * 38.9001
print("DAILY COST w/ 3-TIME PRICING : " + str(cost/100000) + "TL")

print("TOTAL ENERGY USED:", totalpc, "W")


#PLOTTING BEFORE SHIFTING LOADS
plt.subplot(2,1,1)
D = hours
plt.rc('xtick', labelsize=3)
plt.xticks([])
graph=plt.bar(range(len(D)), list(D.values()), color='#a0e6ff', edgecolor='#c3d5e8', align='center')
plt.ylim(0, 2500)
plt.axhline(y=2000, linewidth=1, color='r')
plt.title('Hourly Consumption Graph Before Load Shifting')
plt.ylabel('Power Consumption (W)')

#LOAD SHIFTING
toshift2 = 14
toshift3 = 10
toshift4 = 2
for i in hours:                                
    if hours[i] >1900:
        slashed = i[0:2]
        for b in PRODUCTS.items():
            for c in b:
                if isinstance(c, dict) == True:
                    for z in c["hours"]:
                        if str(z) == slashed:
                            if c["priority"] == 2:
                                c["hours"].remove(z)
                                if toshift2 not in c["hours"] and hours["{}.00-{}.00".format(toshift2, toshift2+1)] < 500:
                                    c["hours"].append(toshift2)
                                elif toshift2+1 not in c["hours"] and hours["{}.00-{}.00".format(toshift2+1, toshift2+2)] < 500:
                                    c["hours"].append(toshift2+1)
                                elif toshift2+2 not in c["hours"] and hours["{}.00-{}.00".format(toshift2+2, toshift2+3)] < 500:
                                    c["hours"].append(toshift2+2)
                                else:
                                    print("i couldn't shift this")
                                c["hours"] = sorted(c["hours"])
                            elif c["priority"] == 3:
                                c["hours"].remove(z)
                                if toshift3 not in c["hours"] and hours["{}.00-{}.00".format(toshift3, toshift3+1)] < 500:
                                    c["hours"].append(toshift3)
                                elif toshift3+1 not in c["hours"] and hours["{}.00-{}.00".format(toshift3+1, toshift3+2)] < 500:
                                    c["hours"].append(toshift3+1)
                                elif toshift3+2 not in c["hours"] and hours["{}.00-{}.00".format(toshift3+2, toshift3+3)] < 500:
                                    c["hours"].append(toshift3+2)
                                else:
                                    print("i couldn't shift this")
                                c["hours"] = sorted(c["hours"])
                        if c["priority"] == 4:
                            c["hours"].remove(z)
                            if toshift4 not in c["hours"] and hours["{}.00-{}.00".format(toshift4, toshift4+1)] < 500:
                                c["hours"].append(toshift4)
                            elif toshift4+1 not in c["hours"] and hours["{}.00-{}.00".format(toshift4+1, toshift4+2)] < 500:
                                c["hours"].append(toshift4+1)
                            elif toshift4+2 not in c["hours"] and hours["{}.00-{}.00".format(toshift4+2, toshift4+3)] < 500:
                                c["hours"].append(toshift4+2)
                            elif toshift4+3 not in c["hours"] and hours["{}.00-{}.00".format(toshift4+3, toshift4+4)] < 500:
                                c["hours"].append(toshift4+3)
                            else:
                                print("i couldn't shift this")
                            c["hours"] = sorted(c["hours"])


#RECREATING AND REFILLING TIME INTERVALS WITH UPDATED DATA
for i in range (0, 24):
    hours["{}.00-{}.00".format(i, i+1)] = 0

for a, b in PRODUCTS.items():
    for y in range(len(b['hours'])):
        hours["{}.00-{}.00".format(b['hours'][y], b['hours'][y]+1)]=hours["{}.00-{}.00".format(b['hours'][y], b['hours'][y]+1)]+b['w']

#UPDATING HOURLY CONSUMPTIONS WITH BATTERY STATE
battery_current = batterycap*0.1
sunshine_duration = 3

print("Charge at start of the day:", battery_current)
for i in range(0,24):
    if i >= 7 and i < 20 and battery_current+batterychargerate<battery_highthreshold and sunshine_duration>0:          #CHARGE BATTERY BETWEEN 08.00-18.00 IN FEBRUARY AND 07.00-20.00 IN AUGUST
        sunshine_duration = sunshine_duration-1
        battery_current = battery_current+batterychargerate
        print("Battery charged at", i,". 00, Current battery charge: ", battery_current, "Wh")
    if i >= 17 and i < 23 and battery_current-batterydischargerate>battery_lowthreshold and hours["{}.00-{}.00".format(i, i+1)]-batterydischargerate>0 :      #DISCHARGE BETWEEN 17.00-22.00
        hours["{}.00-{}.00".format(i, i+1)]=hours["{}.00-{}.00".format(i, i+1)]-batterydischargerate
        battery_current = battery_current-batterydischargerate
        print("Battery discharged at", i,". 00, Current battery charge: ", battery_current, "Wh")

#CALCULATING ENERGY COST ACCORDING TO "EPDK" (2020 DATA)
newcost=0
for i in range(0,24):
    newcost=newcost+hours["{}.00-{}.00".format(i, i+1)]*60.5082
print("DAILY COST w/ CONSTANT PRICING AFTER SHIFTING: " + str(newcost/100000) + "TL")

newcost=0
for i in range(0,24):
    if i >= 6 and i <= 16:
        newcost=newcost+hours["{}.00-{}.00".format(i, i+1)]*61.2766
    if i >= 17 and i <= 21:
        newcost=newcost+hours["{}.00-{}.00".format(i, i+1)]*89.2578
    else:
        newcost=newcost+hours["{}.00-{}.00".format(i, i+1)]*38.9001
print("DAILY COST w/ 3-TIME PRICING AFTER SHIFTING: " + str(newcost/100000) + "TL")

totalpc1=0
for i in hours:
    totalpc1= totalpc1+hours[i]
print("TOTAL ENERGY USED:", totalpc1, "W")
print("TOTAL SAVING RATE: %" + str(100-(newcost/cost*100)))

#PLOTTING AFTER SHIFTING LOADS
plt.subplot(2,1,2)
D2 = hours
plt.rc('xtick', labelsize=3)
graph2=plt.bar(range(len(D2)), list(D2.values()), color='#a0e6ff', edgecolor='#c3d5e8', align='center')
plt.xticks(range(len(D2)), list(D2.keys()), rotation=60)
plt.ylim(0, 2500)
plt.axhline(y=2000, linewidth=1, color='r')
plt.title('Hourly Consumption Graph After Load Shifting')
plt.xlabel('Time Intervals')
plt.ylabel('Power Consumption (W)')
plt.show()