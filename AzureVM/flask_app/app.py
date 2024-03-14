import base64
from io import BytesIO
from datetime import datetime
from matplotlib.figure import Figure
from matplotlib import cm
import matplotlib.colors as mcolors
from flask import Flask, render_template
from get_stue_dht11_data import *
import paho.mqtt.publish as publish

app = Flask(__name__)
app.run(debug=True)
def stue_temp():
    timestamps, temp, hum = get_stue_data(10)

    # Generate the figure **without using pyplot**.
    fig = Figure()
    ax = fig.subplots()
    fig.subplots_adjust(bottom=0.3)
    ax.tick_params(axis='x', which='both', rotation=30)
    ax.set_facecolor("white")
    ax.plot(timestamps, temp, linestyle="dashed", c="#11f", linewidth="1.5", marker="d")
    ax.set_xlabel("Timestamps")
    ax.set_ylabel("Temp in C")
    fig.patch.set_facecolor("orange")
    ax.tick_params(axis="x", colors="black")
    ax.tick_params(axis="y", colors="blue")
    ax.spines["left"].set_color("blue")

    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return data

def stue_hum():
    timestamps, temp, hum = get_stue_data(10)
    # Generate the figure **without using pyplot**.
    fig = Figure()
    ax = fig.subplots()
    fig.subplots_adjust(bottom=0.3)
    ax.tick_params(axis='x', which='both', rotation=30)
    ax.set_facecolor("white")
    ax.plot(timestamps, hum, linestyle="dashed", c="#11f", linewidth="1.5", marker="d")
    ax.set_xlabel("Timestamps")
    ax.set_ylabel("Humidity %")
    fig.patch.set_facecolor("orange")
    ax.tick_params(axis="x", colors="black")
    ax.tick_params(axis="y", colors="blue")
    ax.spines["left"].set_color("blue")
    
    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return data

def bat_stat():
    fig = Figure()
    # make data
    measurement = 75
    esp1 = [measurement, 100-measurement]
    esp2 = [measurement, 100-measurement]
    esp3 = [measurement, 100-measurement]
    esp4 = [measurement, 100-measurement]
    # plot
    ax = fig.subplots(2, 2)

    ax[0, 0].pie(esp1, radius=1, center=(2, 2),
                frame=False, labels=['tilbage', 'brugt'],
                colors=['Green', 'Red'], autopct='%1.0f%%', startangle=270)
    ax[0, 0].set_title("ESP1")
    ax[0, 1].pie(esp2, radius=1, center=(2, 2),
                frame=False, labels=['tilbage', 'brugt'],
                colors=['Green', 'Red'], autopct='%1.0f%%', startangle=270)
    ax[0, 1].set_title("ESP2")
    ax[1, 0].pie(esp3, radius=1, center=(2, 2),
                frame=False, labels=['tilbage', 'brugt'],
                colors=['Green', 'Red'], autopct='%1.0f%%', startangle=270)
    ax[1, 0].set_title("ESP3")
    ax[1, 1].pie(esp4, radius=1, center=(2, 2),
                frame=False, labels=['tilbage', 'brugt'],
                colors=['Green', 'Red'], autopct='%1.0f%%', startangle=270)
    ax[1, 1].set_title("ESP4")


    buf = BytesIO()
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return data

def humidity_realtime():
    fig = Figure(figsize=(3,5))
    measurement = 100
    hum1 = [measurement]
    hum2 = [measurement]
    x = 1
    ax1, ax2 = fig.subplots(2, 1)
    colors = [(0, 'green'), (0.5, 'yellow'), (1, 'red')]
    custom_cmap = mcolors.LinearSegmentedColormap.from_list('custom', colors)

    ax1.bar(x, hum1, width=1, edgecolor="white", linewidth=0.7,  color=custom_cmap(hum1))
    ax1.set(xlim=(1, 1), xticks=list(range(1, 1)),
            ylim=(0, 4), yticks=list(range(0, 101, 10)))
    ax1.set_title("Humidity 1")

    ax2.bar(x, hum2, width=1, edgecolor="white", linewidth=0.7,  color=custom_cmap(hum1))
    ax2.set(xlim=(1, 1), xticks=list(range(1, 1)),
            ylim=(0, 4), yticks=list(range(0, 101, 10)))
    ax2.set_title("Humidity 2")

    buf = BytesIO()
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return data

def temp_realtime():
    fig = Figure(figsize=(3,5))
    measurement = 100
    temp1 = [measurement]
    temp2 = [measurement]
    x = 1
    ax1, ax2 = fig.subplots(2, 1)
    

    ax1.bar(x, temp1, width=1, edgecolor="white", linewidth=0.7)
    ax1.set(xlim=(1, 1), xticks=list(range(1, 1)),
            ylim=(0, 4), yticks=list(range(10, 41, 10)))
    ax1.set_title("Temperature 1")

    ax2.bar(x, temp2, width=1, edgecolor="white", linewidth=0.7)
    ax2.set(xlim=(1, 1), xticks=list(range(1, 1)),
            ylim=(0, 4), yticks=list(range(10, 41, 10)))
    ax2.set_title("Temperature 2")

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
    #fire_status = fire()
    #particle_count = part_count()
    #co2 = co_2()
    return render_template('mqtt.html', esp_bat_stat=esp_bat_stat, humidity=humidity, temperature=temperature)


@app.route('/kitchen')
def kitchen():
    return render_template('kitchen.html')

@app.route('/livingroom')
def livingroom():
    stue_temperature = stue_temp()
    stue_humidity = stue_hum()
    return render_template('livingroom.html', stue_temperature=stue_temperature, stue_humidity=stue_humidity)

@app.route('/taend/', methods=['POST'])
def taend():
    publish.single("LED", "taend", hostname="localhost")
    return render_template('kitchen.html')

@app.route('/sluk/', methods=['POST'])
def sluk():
    publish.single("LED", "sluk", hostname="localhost")
    return render_template('kitchen.html')

@app.route('/F_U')
def f_u():
    return render_template('FuckJer.html')
