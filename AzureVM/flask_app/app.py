import base64
from io import BytesIO
from datetime import datetime
from matplotlib.figure import Figure
from matplotlib import cm
import matplotlib.colors as mcolors
from flask import Flask, render_template
from get_data import *
import paho.mqtt.publish as publish

app = Flask(__name__)
app.run(debug=True)
def stue_temp():
    timestamps, temp, hum, tvoc, part, co2 = get_stue_data(1)
   
    fig = Figure()
    
    
    ax1 = fig.add_subplot(2, 1, 1)
    ax1.tick_params(axis='x', which='both', rotation=30)
    ax1.set_facecolor("white")
    ax1.plot(timestamps, temp, linestyle="dashed", c="#11f", linewidth="1.5", marker="d")
    ax1.set_xlabel("Timestamps")
    ax1.set_ylabel("Temp in C")
    ax1.tick_params(axis="x", colors="black")
    ax1.tick_params(axis="y", colors="blue")
    ax1.spines["left"].set_color("blue")

    ax2 = fig.add_subplot(2, 1, 2)
    ax2.tick_params(axis='x', which='both', rotation=30)
    ax2.set_facecolor("white")
    ax2.plot(timestamps, hum, linestyle="dashed", c="#11f", linewidth="1.5", marker="d")
    ax2.set_xlabel("Timestamps")
    ax2.set_ylabel("Humidity in %")

    
    ax2.tick_params(axis="x", colors="black")
    ax2.tick_params(axis="y", colors="blue")
    ax2.spines["left"].set_color("blue")
    fig.subplots_adjust(bottom=0.3)
    fig.patch.set_facecolor("orange")
    buf = BytesIO()
    fig.savefig(buf, format="png")
    
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return data

def stue_data():
    timestamps, temp, hum, tvoc, part, co = get_stue_data(1)
    
    fig = Figure()
    ax1, ax2 = fig.subplots(1, 3)
    fig.subplots_adjust(bottom=0.3)
    ax1.tick_params(axis='x', which='both', rotation=30)
    ax1.set_facecolor("white")
    ax1.plot(timestamps, hum, linestyle="dashed", c="#11f", linewidth="1.5", marker="d")
    ax1.set_xlabel("Timestamps")
    ax1.set_ylabel("Humidity %")
    ax1.tick_params(axis="x", colors="black")
    ax1.tick_params(axis="y", colors="blue")
    ax1.spines["left"].set_color("blue")

    ax2.tick_params(axis='x', which='both', rotation=30)
    ax2.set_facecolor("white")
    ax2.plot(timestamps, hum, linestyle="dashed", c="#11f", linewidth="1.5", marker="d")
    ax2.set_xlabel("Timestamps")
    ax2.set_ylabel("Humidity %")
    ax2.tick_params(axis="x", colors="black")
    ax2.tick_params(axis="y", colors="blue")
    ax2.spines["left"].set_color("blue")
    fig.patch.set_facecolor("orange")
    
    
    
    buf = BytesIO()
    fig.savefig(buf, format="png")
    
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return data

def bat_stat():
    timestamps, temp, hum, bat1 = get_bath_data(1)
    timestamps, temp, hum, bat2 = get_bedroom_data(1)
    
    fig = Figure(figsize=(4,4))
    
    esp1 = [bat1[0], 100 - int(bat1[0])]
    esp2 = [bat2[0], 100 - int(bat2[0])]
    
    ax1, ax2 = fig.subplots(2, 1)

    ax1.pie(esp1, radius=1, center=(0.5, 0.5),
                frame=False, labels=['tilbage', ' '],
                colors=['Green', 'Red'], autopct='%1.0f%%', startangle=270)
    ax1.set_title("ESP1")
    ax2.pie(esp2, radius=1, center=(0.5, 0.5),
                frame=False, labels=['tilbage', ' '],
                colors=['Green', 'Red'], autopct='%1.0f%%', startangle=270)
    ax2.set_title("ESP2")

    fig.tight_layout()

    buf = BytesIO()
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return data

def humidity_realtime():
    timestamps, temp, hum1, bat = get_bath_data(1)
    timestamps, temp, hum2, bat = get_bedroom_data(1)
    timestamps, temp, hum3, tvoc, part, co2 = get_stue_data(1)
    
    fig = Figure(figsize=(3,6))
   
    hum1 = [hum1[0]]
    hum2 = [hum2[0]]
    hum3 = [hum3[0]]
    x = 1
    ax1, ax2, ax3 = fig.subplots(3, 1)
    fig.subplots_adjust(left=0.5, right=0.6)

    colors = [(0, 'green'), (0.5, 'yellow'), (1, 'red')]
    custom_cmap = mcolors.LinearSegmentedColormap.from_list('custom', colors)

    ax1.bar(x, hum1, width=1, edgecolor="white", linewidth=0.7,  color=custom_cmap(hum1))
    ax1.set(xlim=(1, 1), xticks=list(range(1, 1)),
            ylim=(0, 4), yticks=list(range(0, 101, 25)))
    ax1.set_title("Humidity 1")

    ax2.bar(x, hum2, width=1, edgecolor="white", linewidth=0.7,  color=custom_cmap(hum1))
    ax2.set(xlim=(1, 1), xticks=list(range(1, 1)),
            ylim=(0, 4), yticks=list(range(0, 101, 25)))
    ax2.set_title("Humidity 2")
    
    ax3.bar(x, hum3, width=1, edgecolor="white", linewidth=0.7,  color=custom_cmap(hum1))
    ax3.set(xlim=(1, 1), xticks=list(range(1, 1)),
            ylim=(0, 4), yticks=list(range(0, 101, 25)))
    ax3.set_title("Humidity 3")

    buf = BytesIO()
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return data

def temp_realtime():
    timestamps, temp1, hum1, bat = get_bath_data(1)
    timestamps, temp2, hum2, bat = get_bedroom_data(1)
    timestamps, temp3, hum3, tvoc, part, co2 = get_stue_data(1)

    fig = Figure(figsize=(3,6))
    measurement = 18
    temp1 = [temp1[0]]
    temp2 = [temp2[0]]
    temp3 = [temp3[0]]
    x = 1
    ax1, ax2, ax3 = fig.subplots(3, 1)

    fig.subplots_adjust(left=0.5, right=0.6)   

    ax1.bar(x, temp1, width=1, edgecolor="white", linewidth=0.7)
    ax1.set(xlim=(1, 1), xticks=list(range(1, 1)),
            ylim=(0, 4), yticks=list(range(10, 41, 10)))
    ax1.set_title("Temperature 1")

    ax2.bar(x, temp2, width=1, edgecolor="white", linewidth=0.7)
    ax2.set(xlim=(1, 1), xticks=list(range(1, 1)),
            ylim=(0, 4), yticks=list(range(10, 41, 10)))
    ax2.set_title("Temperature 2")

    ax3.bar(x, temp3, width=1, edgecolor="white", linewidth=0.7)
    ax3.set(xlim=(1, 1), xticks=list(range(1, 1)),
            ylim=(0, 4), yticks=list(range(10, 41, 10)))
    ax3.set_title("Temperature 3")

    buf = BytesIO()
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return data

def Tvoc_co2__particle_real():
    timestamps, temp3, hum3, tvoc, part, co2 = get_stue_data(1)

    fig = Figure(figsize=(3,6))
    measurement = 18
    tvoc = [tvoc[0]]
    co2 = [co2[0]]
    pm = [part[0]]
    x = 1
    ax1, ax2, ax3 = fig.subplots(3, 1)
    
    fig.subplots_adjust(left=0.5, right=0.6)

    ax1.bar(x, tvoc, width=1, edgecolor="white", linewidth=0.7)
    ax1.set(xlim=(1, 1), xticks=list(range(1, 1)),
            ylim=(0, 4), yticks=list(range(0, 2001, 500)))
    ax1.set_title("Tvoc")

    ax2.bar(x, co2, width=1, edgecolor="white", linewidth=0.7)
    ax2.set(xlim=(1, 1), xticks=list(range(1, 1)),
            ylim=(0, 4), yticks=list(range(0, 4001, 500)))
    ax2.set_title("CO2")

    ax3.bar(x, part, width=1, edgecolor="white", linewidth=0.7)
    ax3.set(xlim=(1, 1), xticks=list(range(1, 1)),
            ylim=(0, 4), yticks=list(range(0, 301, 50)))
    ax3.set_title("Particles")

    buf = BytesIO()
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return data



@app.route('/')
def home():
    return render_template('index.html')

@app.route('/mqtt')
def mqtt():
    esp_bat_stat = bat_stat()
    humidity = humidity_realtime()
    temperature = temp_realtime()
    Tvoc = Tvoc_co2__particle_real()
    return render_template('mqtt.html', esp_bat_stat=esp_bat_stat, humidity=humidity, temperature=temperature,
                           Tvoc=Tvoc,)


@app.route('/kitchen')
def kitchen():
    return render_template('kitchen.html')

@app.route('/livingroom')
def livingroom():
    stue_temperature = stue_temp()
    stue_data = stue_data()
    return render_template('livingroom.html', stue_temperature=stue_temperature, stue_data=stue_data)

@app.route('/taend/', methods=['POST'])
def taend():
    publish.single("LED", "taend", hostname="localhost")
    return render_template('kitchen.html')

@app.route('/sluk/', methods=['POST'])
def sluk():
    publish.single("LED", "sluk", hostname="localhost")
    return render_template('kitchen.html')
