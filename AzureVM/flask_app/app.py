import base64
from io import BytesIO
from datetime import datetime
from matplotlib.figure import Figure
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
                wedgeprops={"linewidth": 1, "edgecolor": "white"}, frame=False, labels=['tilbage', 'brugt'],
                colors=['Green', 'Red'], autopct='%1.1f%%', startangle=270)
    ax[0, 0].set_title("ESP1")
    ax[0, 1].pie(esp2, radius=1, center=(2, 2),
                wedgeprops={"linewidth": 1, "edgecolor": "white"}, frame=False, labels=['tilbage', 'brugt'],
                colors=['Green', 'Red'], autopct='%1.1f%%', startangle=270)
    ax[0, 1].set_title("ESP2")
    ax[1, 0].pie(esp3, radius=1, center=(2, 2),
                wedgeprops={"linewidth": 1, "edgecolor": "white"}, frame=False, labels=['tilbage', 'brugt'],
                colors=['Green', 'Red'], autopct='%1.1f%%', startangle=270)
    ax[1, 0].set_title("ESP3")
    ax[1, 1].pie(esp4, radius=1, center=(2, 2),
                wedgeprops={"linewidth": 1, "edgecolor": "white"}, frame=False, labels=['tilbage', 'brugt'],
                colors=['Green', 'Red'], autopct='%1.1f%%', startangle=270)
    ax[1, 1].set_title("ESP4")


    buf = BytesIO()
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return data

def humidity_realtime():
    fig = Figure()
    measurement = 45
    hum1 = [measurement, 100-measurement]
    hum2 = [measurement, 100-measurement]

    ax = fig.subplots(2, 0)

    ax.bar(x, y, width=1, edgecolor="white", linewidth=0.7)

    ax.set(xlim=(0, 8), xticks=np.arange(1, 8),
            ylim=(0, 8), yticks=np.arange(1, 8))

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
    #hum1 = hum()
    #temp1 = temp()
    #fire_status = fire()
    #particle_count = part_count()
    #co2 = co_2()
    return render_template('mqtt.html', esp_bat_stat=esp_bat_stat)


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
