#-------------- 6gym Verias Greece --------------

#--------------  initialization  -----------------
from sense_hat import SenseHat
import time, logging

sense = SenseHat()
sense.clear()

#--------------Start logfile  -----------------
timestamp = time.strftime("%d/%m/%Y-%H:%M:%S")
logging.basicConfig(filename='6gymastro'+'.log',level=logging.DEBUG)

m = timestamp + " **** Starting Experiment ****"+"\n"
logging.info(m)

m="---------------------------------------"+"\n"
logging.info(m)

#--------------Display basiline message  -----------------
red = (255, 0, 0)
white = (255, 255, 255)

sense.show_message("6gym Verias", text_colour = red)

#--------------Reseting Counters  -----------------
sum_hum = 0
min_hum = 100
max_hum = 0
sum_temp = 0
min_temp = 100
max_temp = 0

#--------------Measure Baseline humidity every 30 seconds for 10 minutes  -----------------
timestamp = time.strftime("%d/%m/%Y-%H:%M:%S")
m = timestamp + " **** Starting Baseline Humidity Measurement **** "+"\n"
logging.info(m)

#----- counters ------
c1 = 0     
c2 = 0
nav = 20
x = 0

#----- temp counters
tempup = 0
tempdown = 0
min_temp = 100
max_temp = 0
templast = 0
minust = 100
maxit  = 0

for x in range(360):     # 360 times with 30 sec delay = 180 min = 3 hours

    #----- humidity Counting 20 measures to collect the average------
    if c1 < nav:    
        humidity = sense.get_humidity()
        humidity = round(humidity, 1)
    
        if humidity > 100:
            humidity = 100.0
    
        if humidity < min_hum:
            min_hum = humidity
    
        if humidity > max_hum:
            max_hum = humidity

        sum_hum = sum_hum + humidity
        c1 += 1
        
    else:
        if c2 == 0:
            #----Calculate average and range of humidity  min max -----------------
            mohum = round(sum_hum / nav,1)  

            #--------------Write average and range of humidity to a file -----------------
            print("Mo Humidity=",mohum)

            mo="Average Humidity="+ str(mohum) + "\n"
            logging.info(mo)
            c2 = 1

    #----- taking humidity measures ------                
    humidity = sense.get_humidity()
    humidity = round(humidity, 1)
    
    if c2 == 1:        
        diafora = round(humidity - mohum,1)
        diaf = round(diafora / mohum,1)
        
        if diaf > 0.1: #insteadof 0.05
            print(humidity, mohum, diafora, diaf)            
            m = "I found you"
            logging.info(m)
            sense.show_message("I found you", text_colour = red)
                
    time.sleep(30)     #30 seconds normally    


    #----- temperature taking measures to compute the average------
    temp = sense.get_temperature()
    temp = round(temp, 1)    

    if temp < min_temp:
            min_temp = temp
            tempdown += 1
            if min_temp < minust:
                minust = min_temp
    
    if temp > max_temp:
            max_temp = temp
            tempup += 1
            if max_temp > maxit:
                maxit = max_temp

    temp_diaf = round(temp - templast,1)
    if tempup > 10:
        m = timestamp + "  day is coming " + str(tempup) + " temp rises="+ str(temp)
        tempup = 0
        tempdown = 0
	min_temp = 100
	max_temp = 0
        logging.info(m)              
        print(m)
        sense.show_message("day is coming", text_colour = red)

    elif tempdown >10:
        m = timestamp + "  night is coming " + str(tempup) + " temp decreases="+ str(temp)
        tempup = 0
        tempdown = 0
	min_temp = 100
	max_temp = 0
        logging.info(m)              
        print(m)
        sense.show_message("night is coming", text_colour = red)
        
       
    templast = temp           
        

    timestamp = time.strftime("%d/%m/%Y-%H:%M:%S")
    
    m = timestamp + "  hum="+ str(humidity) + "  --  temp="+ str(temp) + " -- diaf_temp = " + str(temp_diaf) + "  -- tempup = " + str(tempup) + "  -- tempdown = " + str(tempdown) 
    logging.info(m)          
       
    print(m)


m = timestamp + "  min_hum="+ str(min_hum) + "  max_hum="+ str(max_hum) +"  --  mintemp="+ str(minust) + "  --  maxtemp="+ str(maxit) 
logging.info(m)           
print(m)
 
