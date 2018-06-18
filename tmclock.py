# simple clock program in micropython for tm1637
# Tommy Faasen 2018

import time
import tm1637

#init clock 
#pin 15 is clk
#pin 13 is data
#brightness is set to 2 (0-7)
display=tm1637.TM1637(15,13,2)
#clear screen
display.Clear()

while True:
  #get the time
  lt=time.localtime()
  #lt[3] = hour
  #lt[4] = minutes
  mytime="%d%d"%(lt[3],lt[4])
  #check if hour or minutes is 1 or 2 digits
  if lt[3]<10:
    if(lt[4])<10:
      mytime=" %d0%d"%(lt[3],lt[4])
    else:
      mytime=" %d%d"%(lt[3],lt[4])
  else:
     if(lt[4])<10:
       mytime="%d0%d"%(lt[3],lt[4])
       
  #set display with list of 4 digits 0=0, 1=1, 10=A, 15=F
  display.Show([int(mytime[0]),int(mytime[1]),int(mytime[2]),int(mytime[3])])  
  # show colon every other second
  display.ShowDoublepoint(lt[5]%2)    
  
  time.sleep(1)
