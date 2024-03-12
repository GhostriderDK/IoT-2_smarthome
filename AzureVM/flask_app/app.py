import base64
from io import BytesIO
from datetime import datetime
from matplotlib.figure import Figure
from flask import Flask, render_template
from get_stue_dht11_data import get_stue_data
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

def bat_stat_1():
    fig = Figure()
    
    # make data
    measurement = 75
    x = [measurement, 100-measurement]
    

    # plot
    ax = fig.subplots()
    ax.pie(x, radius=3, center=(4, 4),
           wedgeprops={"linewidth": 1, "edgecolor": "white"}, frame=True)

    ax.set(xlim=(0, 8), xticks=(0,8),
           ylim=(0, 8), yticks=(0,8))
    
    buf2 = BytesIO()
    fig.savefig(buf2, format="png")
    # Embed the result in the html output.
    data1 = base64.b64encode(buf2.getbuffer()).decode("ascii")
    return data1
    


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/mqtt')
def mqtt():
    esp1_bat_stat = bat_stat_1()
    #esp2_bat_stat = bat_stat_2()
    #esp3_bat_stat = bat_stat_3()
    #esp4_bat_stat = bat_stat_4()
    #hum1 = hum()
    #temp1 = temp()
    #fire_status = fire()
    #particle_count = part_count()
    #co2 = co_2()
    return render_template('mqtt.html', esp1_bat_stat=esp1_bat_stat)


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
