
#en cours de codage, intégration des graphiques matplotlib dans une fenêtre tkinter


import time
import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class AnimationPlot:

    def animate(self, i, dataListAcX, dataListAcY, dataListAcZ, dataListGyX, dataListGyY, dataListGyZ, ser):
        ser.write(b'a')                                     # Transmit the char 'g' to receive the Arduino data point
        arduinoData_string = ser.readline().decode('ascii') # Decode receive Arduino data as a formatted string
        #print(i)                                           # 'i' is a incrementing variable based upon frames = x argument
        print(arduinoData_string)
        arduinoData_array = arduinoData_string.split("|")

        try:
            arduinoDataAcX_float = float(arduinoData_array[0])   # Convert to float
            arduinoDataAcY_float = float(arduinoData_array[1])
            arduinoDataAcZ_float = float(arduinoData_array[2])
            arduinoDataGyX_float = float(arduinoData_array[3])
            arduinoDataGyY_float = float(arduinoData_array[4])
            arduinoDataGyZ_float = float(arduinoData_array[5])
            dataListAcX.append(arduinoDataAcX_float)              # Add to the list holding the fixed number of points to animate
            dataListAcY.append(arduinoDataAcY_float)
            dataListAcZ.append(arduinoDataAcZ_float)
            dataListGyX.append(arduinoDataGyX_float)
            dataListGyY.append(arduinoDataGyY_float)
            dataListGyZ.append(arduinoDataGyZ_float)

        except:                                             # Pass if data point is bad                               
            pass

        dataListAcX = dataListAcX[-50:]                           # Fix the list size so that the animation plot 'window' is x number of points
        dataListAcY = dataListAcY[-50:]
        dataListAcZ = dataListAcZ[-50:]
        dataListGyX = dataListGyX[-50:]
        dataListGyY = dataListGyY[-50:]
        dataListGyZ = dataListGyZ[-50:]   

        axs[0].clear()
        axs[1].clear()                                          # Clear last data frame
        
        self.getPlotFormat()
        axs[0].plot(dataListAcX)                                   # Plot new data frame
        axs[0].plot(dataListAcY)
        axs[0].plot(dataListAcZ)
        axs[0].legend(['AcX','AcY','AcZ'])
        axs[1].plot(dataListGyX)
        axs[1].plot(dataListGyY)
        axs[1].plot(dataListGyZ)
        axs[1].legend(['GyX','GyY','GyZ'])
        
        
    def getPlotFormat(self):
        axs[0].set_ylim([-20000, 20000])                              # Set Y axis limit of plot
        axs[0].set_title("accelerometers")                        # Set title of figure
        #ax[0,0].set_ylabel("Value")                              # Set title of y axis
        axs[1].set_title("Gyroscopes")
        axs[1].set_ylim([-20000, 20000])

dataListAcX = []                                           # Create empty list variable for later use
dataListAcY = []
dataListAcZ = []
dataListGyX = []
dataListGyY = []
dataListGyZ = []

                                                        
#fig = plt.figure()                                      # Create Matplotlib plots fig is the 'higher level' plot window
#ax = fig.subplots(2)                               # Add subplot to main fig window
fig, axs = plt.subplots(2)
realTimePlot = AnimationPlot()

ser = serial.Serial("COM3", 9600)                       # Establish Serial object with COM port and BAUD rate to match Arduino Port/rate
time.sleep(2)                                           # Time delay for Arduino Serial initialization 

                                                        # Matplotlib Animation Fuction that takes takes care of real time plot.
                                                        # Note that 'fargs' parameter is where we pass in our dataList and Serial object. 
ani = animation.FuncAnimation(fig, realTimePlot.animate, frames=100, fargs=(dataListAcX, dataListAcY, dataListAcZ, dataListGyX, dataListGyY, dataListGyZ, ser), interval=500) 

plt.show()                                              # Keep Matplotlib plot persistent on screen until it is closed
ser.close()                                             # Close Serial connection when plot is closed
