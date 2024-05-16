import time
import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class AnimationPlot:

    def animate(self, i, dataListAcX, dataListAcY, dataListAcZ, dataListGyX, dataListGyY, dataListGyZ, ser):
        ser.write(b'a')                                     # renvoi a dans le port série pour recevoir les données.
        arduinoData_string = ser.readline().decode('ascii') # traitement des données reçues au format string
        print(arduinoData_string)
        arduinoData_array = arduinoData_string.split("|")

        try:
            arduinoDataAcX_float = float(arduinoData_array[0])
            arduinoDataAcY_float = float(arduinoData_array[1])
            arduinoDataAcZ_float = float(arduinoData_array[2])
            arduinoDataGyX_float = float(arduinoData_array[3])
            arduinoDataGyY_float = float(arduinoData_array[4])
            arduinoDataGyZ_float = float(arduinoData_array[5])
            #ajout des valeurs dans les tableaux des différentes valeurs
            dataListAcX.append(arduinoDataAcX_float)
            dataListAcY.append(arduinoDataAcY_float)
            dataListAcZ.append(arduinoDataAcZ_float)
            dataListGyX.append(arduinoDataGyX_float)
            dataListGyY.append(arduinoDataGyY_float)
            dataListGyZ.append(arduinoDataGyZ_float)
        #Si les données sont mauvaises, empêche le traitement
        except:                             
            pass
        #ne tient compte que des 50 derniers points
        dataListAcX = dataListAcX[-50:]
        dataListAcY = dataListAcY[-50:]
        dataListAcZ = dataListAcZ[-50:]
        dataListGyX = dataListGyX[-50:]
        dataListGyY = dataListGyY[-50:]
        dataListGyZ = dataListGyZ[-50:]   

        #nettoyage des graphiques
        axs[0].clear()
        axs[1].clear()

        #remise en formes des graphiques
        self.getPlotFormat()
        axs[0].plot(dataListAcX)
        axs[0].plot(dataListAcY)
        axs[0].plot(dataListAcZ)
        axs[0].legend(['AcX','AcY','AcZ'])
        axs[1].plot(dataListGyX)
        axs[1].plot(dataListGyY)
        axs[1].plot(dataListGyZ)
        axs[1].legend(['GyX','GyY','GyZ'])
        
        
    def getPlotFormat(self):
        axs[0].set_ylim([-20000, 20000])
        axs[0].set_title("accelerometers")
        #ax[0,0].set_ylabel("Value")
        axs[1].set_title("Gyroscopes")
        axs[1].set_ylim([-20000, 20000])
#préparation pour réutilisation des valeurs
dataListAcX = []
dataListAcY = []
dataListAcZ = []
dataListGyX = []
dataListGyY = []
dataListGyZ = []

fig, axs = plt.subplots(2)
realTimePlot = AnimationPlot()

#préparation et attente liaison série
ser = serial.Serial("COM3", 9600)
time.sleep(2)

ani = animation.FuncAnimation(fig, realTimePlot.animate, frames=100, fargs=(dataListAcX, dataListAcY, dataListAcZ, dataListGyX, dataListGyY, dataListGyZ, ser), interval=500) 

plt.show()
ser.close()
