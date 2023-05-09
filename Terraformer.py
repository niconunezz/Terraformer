import serial
import matplotlib.pyplot as plt
import time
import simplekml
import pandas as pd
import time
import datetime


kml = simplekml.Kml()
its=0
#altG=500
#lonG=-3.70885+0.0005
#latG=40.388975+0.0005
coords = []

# Configuración de puerto serial
arduino = serial.Serial('COM9', baudrate=9600, timeout=1.0)

# Crear gráficas
plt.ion()


fig, ((ax1, ax2), (ax3, ax4), (ax5, ax6)) = plt.subplots(3, 2, figsize=(10, 10), sharex=True)
line1, = ax1.plot([], [], label='Sensor UV(mV)')
line2, = ax2.plot([], [], label='Indice UV')
line3, = ax3.plot([], [], label='Temperatura(°C)')
line4, = ax4.plot([], [], label='Presión(Pa)')
line5, = ax5.plot([], [], label='Altitud(m)')
line6,= ax6.plot([],[],label='Voltaje sensor(mv)')
ax1.legend()
ax2.legend()
ax3.legend()
ax4.legend()
ax5.legend()
ax6.legend()
fig.suptitle('M+NDAP', fontsize=20)
# Definir variables para los datos y el tiempo
data1 = []  # Lista para Lectura sensor UV
data2 = []  # Lista para Indice UV
data3 = []  # Lista para Temperatura
data4 = []  # Lista para Presión
data5 = []  # Lista para Altitud Aproximada
data6 = []
Latitud=[]
Longitud=[]
Hora=[]
x_data = []

# Iniciar temporizador
start_time = time.time()

while True:
    # Leer línea de Arduino
    raw_line = arduino.readline()

    try:
        # Convertir línea a valores numéricos
        values = raw_line.decode().strip().split(' ')
        sensor = float(values[10])
        uv_index = float(values[20])
        temperature = float(values[22])
        pressure = float(values[24])
        altitude = float(values[26])
        voltaje= float(values[15])
        
        lonG=float(values[2])
        latG=float(values[5])
        #lonG-=0.0005
        #altG+=50
        #latG-=0.0005
        hora_actual = datetime.datetime.now().time()
        coords.append((lonG, latG, altitude))
        linestring=kml.newlinestring(name="trayectoria", coords=coords)
        linestring.altitudemode = simplekml.AltitudeMode.absolute
        linestring.style.linestyle.color = simplekml.Color.rgb(169, 220, 227)

        linestring.style.polystyle.polyextrude = 0
        linestring.style.polystyle.color = simplekml.Color.rgb(118, 137, 222)
        linestring.extrude = 1
        
        # Abre el archivo KML en modo de escritura
        with open(r"C:\Users\alumno\Documents\Google-Nico\Nico.kml", "w") as f:
            # Escribe el contenido del objeto Kml en el archivo
            f.write(kml.kml())

        # Añadir valores a las listas
        data1.append(sensor)
        data2.append(uv_index)
        data3.append(temperature)
        data4.append(pressure)
        data5.append(altitude)
        data6.append(voltaje)
        Longitud.append(lonG)
        Latitud.append(latG)
        Hora.append(hora_actual)
        

        x_data.append(time.time() - start_time)

        its+=1
        df = pd.DataFrame({'Hora':Hora ,'Latitud': latG, 'Longitud': lonG, 'Altitud': altitude,'Sensor UV':data1,'Indice UV':data2,'Voltaje UV':data6,'Presión':data4,'Temperatura':data3})
        df.to_excel(r'C:\Users\alumno\Documents\Google-Nico\datos.xlsx', index=False)
        # Actualizar las líneas
        line1.set_xdata(x_data)
        line1.set_ydata(data1)
        line2.set_xdata(x_data)
        line2.set_ydata(data2)
        line3.set_xdata(x_data)
        line3.set_ydata(data3)
        line4.set_xdata(x_data)
        line4.set_ydata(data4)
        line5.set_xdata(x_data)
        line5.set_ydata(data5)
        line6.set_xdata(x_data)
        line6.set_ydata(data6)
        ax1.relim()
        ax1.autoscale_view()
        ax2.relim()
        ax2.autoscale_view()
        ax3.relim()
        ax3.autoscale_view()
        ax4.relim()
        ax4.autoscale_view()
        ax5.relim()
        ax5.autoscale_view()
        ax6.relim()
        ax6.autoscale_view()
        fig.canvas.draw()
        fig.canvas.flush_events()

        time.sleep(0.1)

    except (ValueError, IndexError):
        pass
