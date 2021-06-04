import serial
import time
port="/dev/rfcomm0"
print('hello world')
bluetooth= serial.Serial(port,9600)
print ('hello world 2')
bluetooth.flushInput()
print ('hello world 3')
for i in range(100):
   print("we are in the for loop",i)
   bluetooth.write("a".encode())
   inputs=bluetooth.readline()
   print("we are in the inputs for loop",i)
   inputasinteger= int(inputs)
   if inputs:
           print('we have inputs')
           fileb= open("blue.txt",'wU')
           fileb.write(inputasInteger*10)
   time.sleep(.5)
   print('sleeping')
fileb.close()
print('file has been closse')
exit()