
import matplotlib.pyplot as plt
import time
import simplekml
import pandas as pd
import random
import datetime


kml = simplekml.Kml()

coords=[]
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



data=pd.DataFrame(columns=['Sensor','UV_index','Temp','Pressure','Altitud',
                   'Voltaje','Latitud','Longitud',
                   'Hora','x_data'])

# Iniciar temporizador
start_time = time.time()
i=0
while True:


    try:    
        altitude = round(random.uniform(1000, 10000), 2)
        lonG = round(random.uniform(-180, 180), 2)
        latG = round(random.uniform(-90, 90), 2)
        voltaje = round(random.uniform(0, 5), 2)
        sensor = random.randint(1, 10)
        uv = round(random.uniform(0, 10), 2)
        uv_index = random.randint(1, 100)
        temperature = round(random.uniform(-50, 50), 2)
        pressure = round(random.uniform(800, 1200), 2)
        tm=time.time() - start_time
        hora_actual = datetime.datetime.now().time()

        
        dic={'Sensor':sensor,'UV_index':uv_index,'Temp':temperature,'Pressure':pressure,'Altitud':altitude,
                   'Voltaje':voltaje,'Latitud':latG,'Longitud':lonG,
                   'Hora':hora_actual,'x_data':tm}

        data.loc[i]=dic

        coords.append((lonG, latG, altitude))

        linestring=kml.newlinestring(name="trayectoria", coords=coords)
        linestring.altitudemode = simplekml.AltitudeMode.absolute
        linestring.style.linestyle.color = simplekml.Color.rgb(169, 220, 227)
        linestring.style.polystyle.polyextrude = 0
        linestring.style.polystyle.color = simplekml.Color.rgb(118, 137, 222)
        linestring.extrude = 1
        
        # Abre el archivo KML en modo de escritura
        with open(r"Trayectoria.kml", "w") as f:
             #Escribe el contenido del objeto Kml en el archivo
            f.write(kml.kml())

        # Añadir valores a las listas

        df = pd.DataFrame({'Hora':data['Hora'] ,'Latitud': data['Latitud'], 'Longitud': data['Longitud'],
                                'Altitud':  data['Altitud'],'Sensor UV':data['Sensor'],'Indice UV':data['UV_index'],
                                'Voltaje UV':data['Voltaje'],'Presión':data['Pressure'],'Temperatura':data['Temp']})
            
        data.to_excel(r'data.xlsx', index=False)
        df.to_excel(r'datos.xlsx', index=False)
        
        # Actualizar las líneas
        line1.set_xdata(data['x_data'])
        line1.set_ydata(data['Sensor'])
        line2.set_xdata(data['x_data'])
        line2.set_ydata(data['UV_index'])
        line3.set_xdata(data['x_data'])
        line3.set_ydata(data['Temp'])
        line4.set_xdata(data['x_data'])
        line4.set_ydata(data['Pressure'])
        line5.set_xdata(data['x_data'])
        line5.set_ydata(data['Altitud'])
        line6.set_xdata(data['x_data'])
        line6.set_ydata(data['Voltaje'])
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

