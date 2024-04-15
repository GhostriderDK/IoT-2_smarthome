import base64
from io import BytesIO
from matplotlib.figure import Figure
import matplotlib.colors as mcolors
from flask import Flask, render_template
from get_data import *
import paho.mqtt.publish as publish

app = Flask(__name__)
app.run(debug=True)
datapoints = 100
num_ticks = 20

def bath_temp():
    timestamps, temp, hum, bat = get_bath_data(datapoints)
   
    fig = Figure() 
    ax1 = fig.add_subplot(2, 1, 1)
    fig.subplots_adjust(bottom=0.1)
    ax1.set_facecolor("white")
    ax1.plot(timestamps, temp, linestyle="solid", c="#11f", linewidth="1.5")
    ax1.set_ylabel("Temp in C")
    ax1.tick_params(axis="y", colors="blue")
    ax1.spines["left"].set_color("blue")
    tick_positions = range(0, len(timestamps), len(timestamps) // num_ticks)  
    ax1.set_xticks(tick_positions) 
    ax1.set_xticklabels([])
    ax1.grid(axis='y', linestyle='--')

    ax2 = fig.add_subplot(2, 1, 2)
    ax2.tick_params(axis='x', which='both', rotation=90)
    ax2.set_facecolor("white")
    ax2.plot(timestamps, hum, linestyle="solid", c="#11f", linewidth="1.5")
    ax2.set_xlabel("Timestamps")
    ax2.set_ylabel("Humidity in %")
    ax2.tick_params(axis="x", colors="black")
    ax2.tick_params(axis="y", colors="blue")
    tick_positions = range(0, len(timestamps), len(timestamps) // num_ticks)
    ax2.set_xticks(tick_positions)
    ax2.spines["left"].set_color("blue")
    ax2.grid(axis='y', linestyle='--')
    
    fig.subplots_adjust(bottom=0.3)
    fig.patch.set_facecolor("orange")
    buf = BytesIO()
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return data

def bedroom_temp():
    timestamps, temp, hum, bat = get_bedroom_data(datapoints)
   
    fig = Figure() 
    ax1 = fig.add_subplot(2, 1, 1)
    fig.subplots_adjust(bottom=0.1)
    ax1.set_facecolor("white")
    ax1.plot(timestamps, temp, linestyle="solid", c="#11f", linewidth="1.5")
    ax1.set_ylabel("Temp in C")
    ax1.tick_params(axis="y", colors="blue")
    ax1.spines["left"].set_color("blue")
    tick_positions = range(0, len(timestamps), len(timestamps) // num_ticks)  
    ax1.set_xticks(tick_positions) 
    ax1.set_xticklabels([])
    ax1.grid(axis='y', linestyle='--')

    ax2 = fig.add_subplot(2, 1, 2)
    ax2.tick_params(axis='x', which='both', rotation=90)
    ax2.set_facecolor("white")
    ax2.plot(timestamps, hum, linestyle="solid", c="#11f", linewidth="1.5")
    ax2.set_xlabel("Timestamps")
    ax2.set_ylabel("Humidity in %")
    ax2.tick_params(axis="x", colors="black")
    ax2.tick_params(axis="y", colors="blue")
    tick_positions = range(0, len(timestamps), len(timestamps) // num_ticks)
    ax2.set_xticks(tick_positions)
    ax2.spines["left"].set_color("blue")
    ax2.grid(axis='y', linestyle='--')
    
    fig.subplots_adjust(bottom=0.3)
    fig.patch.set_facecolor("orange")
    buf = BytesIO()
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return data

def stue_temp():
    timestamps, temp, hum, tvoc, part, co2 = get_stue_data(datapoints)
   
    fig = Figure() 
    ax1 = fig.add_subplot(2, 1, 1)
    fig.subplots_adjust(bottom=0.1)
    ax1.set_facecolor("white")
    ax1.plot(timestamps, temp, linestyle="solid", c="#11f", linewidth="1.5")
    ax1.set_ylabel("Temp in C")
    ax1.tick_params(axis="y", colors="blue")
    ax1.spines["left"].set_color("blue")
    tick_positions = range(0, len(timestamps), len(timestamps) // num_ticks)  
    ax1.set_xticks(tick_positions) 
    ax1.set_xticklabels([])
    ax1.grid(axis='y', linestyle='--')

    ax2 = fig.add_subplot(2, 1, 2)
    ax2.tick_params(axis='x', which='both', rotation=90)
    ax2.set_facecolor("white")
    ax2.plot(timestamps, hum, linestyle="solid", c="#11f", linewidth="1.5")
    ax2.set_xlabel("Timestamps")
    ax2.set_ylabel("Humidity in %")
    ax2.tick_params(axis="x", colors="black")
    ax2.tick_params(axis="y", colors="blue")
    tick_positions = range(0, len(timestamps), len(timestamps) // num_ticks)
    ax2.set_xticks(tick_positions))
    ax2.spines["left"].set_color("blue")
    ax2.grid(axis='y', linestyle='--')
    
    fig.subplots_adjust(bottom=0.3)
    fig.patch.set_facecolor("orange")
    buf = BytesIO()
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return data

def stue_data_co2_tvoc_part():
    timestamps, temp, hum, tvoc, part, co2 = get_stue_data(datapoints)
    
    fig = Figure()
    ax1 = fig.add_subplot(2, 1, 1)
    fig.subplots_adjust(bottom=0.3)
    ax1.set_facecolor("white")
    ax1.plot(timestamps, tvoc, linestyle="solid", c="#11f", linewidth="1.5")
    ax1.set_ylabel("TVOC in ppb")
    ax1.tick_params(axis="y", colors="blue")
    ax1.spines["left"].set_color("blue")
    tick_positions = range(0, len(timestamps), len(timestamps) // num_ticks)
    ax1.set_xticks(tick_positions)
    ax1.set_xticklabels([])
    ax1.grid(axis='y', linestyle='--')

    ax2 = fig.add_subplot(2, 1, 2)
    ax2.tick_params(axis='x', which='both', rotation=90)
    ax2.set_facecolor("white")
    ax2.plot(timestamps, co2, linestyle="solid", c="#11f", linewidth="1.5")
    ax2.set_xlabel("Timestamps")
    ax2.set_ylabel("CO2 in ppm")
    ax2.tick_params(axis="x", colors="black")
    ax2.tick_params(axis="y", colors="blue")
    ax2.spines["left"].set_color("blue")
    tick_positions = range(0, len(timestamps), len(timestamps) // num_ticks)
    ax2.set_xticks(tick_positions)
    ax2.grid(axis='y', linestyle='--')
    fig.patch.set_facecolor("orange")
        
    buf = BytesIO()
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return data

def part_in_air():
    timestamps, temp, hum, tvoc, part, co2 = get_stue_data(datapoints)
    
    fig = Figure()
    ax = fig.subplots()
    fig.subplots_adjust(bottom=0.3)
    
    ax.tick_params(axis='x', which='both', rotation=90)
    ax.set_facecolor("white")
    ax.plot(timestamps, part, linestyle="solid", c="#11f", linewidth="1.5")
    ax.set_xlabel("Timestamps")
    ax.set_ylabel("particles in µg/m³")
    ax.tick_params(axis="x", colors="black")
    ax.tick_params(axis="y", colors="blue")
    ax.spines["left"].set_color("blue")
    tick_positions = range(0, len(timestamps), len(timestamps) // num_ticks)
    ax.set_xticks(tick_positions)
    ax.grid(axis='y', linestyle='--')
    fig.patch.set_facecolor("orange")
    
    buf = BytesIO()
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return data

def bat_stat():
    timestamps, temp, hum, bat1 = get_bath_data(1)
    timestamps, temp, hum, bat2 = get_bedroom_data(1)
    
    fig = Figure(figsize=(3,6))
    
    bath_esp = bat1[0]
    bed_esp = bat2[0]
    x = 1
    ax1, ax2 = fig.subplots(2, 1)
    fig.subplots_adjust(left=0.5, right=0.6)

    ax1.bar(x, bed_esp, width=1, edgecolor="white", linewidth=0.7)
    ax1.set(xlim=(1, 1), xticks=list(range(1, 1)),
            ylim=(0, 4), yticks=list(range(0, 101, 25)))
    ax1.bar_label(ax1.containers[0], fmt='%d', padding=3)
    ax1.set_title("ESP Bed Bat")

    ax2.bar(x, bath_esp, width=1, edgecolor="white", linewidth=0.7)
    ax2.set(xlim=(1, 1), xticks=list(range(1, 1)),
            ylim=(0, 4), yticks=list(range(0, 101, 25)))
    ax2.bar_label(ax2.containers[0], fmt='%d', padding=3)
    ax2.set_title("ESP Bath Bat")

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
    ax1.bar_label(ax1.containers[0], fmt='%d', padding=3)
    ax1.set_title("Humidity Bath")

    ax2.bar(x, hum2, width=1, edgecolor="white", linewidth=0.7,  color=custom_cmap(hum1))
    ax2.set(xlim=(1, 1), xticks=list(range(1, 1)),
            ylim=(0, 4), yticks=list(range(0, 101, 25)))
    ax2.bar_label(ax2.containers[0], fmt='%d', padding=3)
    ax2.set_title("Humidity Bedroom")
    
    ax3.bar(x, hum3, width=1, edgecolor="white", linewidth=0.7,  color=custom_cmap(hum1))
    ax3.set(xlim=(1, 1), xticks=list(range(1, 1)),
            ylim=(0, 4), yticks=list(range(0, 101, 25)))
    ax3.bar_label(ax3.containers[0], fmt='%d', padding=3)
    ax3.set_title("Humidity Stue")

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
    ax1.bar_label(ax1.containers[0], fmt='%d', padding=3)
    ax1.set_title("Temperature Bath")

    ax2.bar(x, temp2, width=1, edgecolor="white", linewidth=0.7)
    ax2.set(xlim=(1, 1), xticks=list(range(1, 1)),
            ylim=(0, 4), yticks=list(range(10, 41, 10)))
    ax2.bar_label(ax2.containers[0], fmt='%d', padding=3)
    ax2.set_title("Temperature Bedroom")

    ax3.bar(x, temp3, width=1, edgecolor="white", linewidth=0.7)
    ax3.set(xlim=(1, 1), xticks=list(range(1, 1)),
            ylim=(0, 4), yticks=list(range(10, 41, 10)))
    ax3.bar_label(ax3.containers[0], fmt='%d', padding=3)
    ax3.set_title("Temperature Stue")

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
    ax1.bar_label(ax1.containers[0], fmt='%d', padding=3)
    ax1.set_title("Tvoc")

    ax2.bar(x, co2, width=1, edgecolor="white", linewidth=0.7)
    ax2.set(xlim=(1, 1), xticks=list(range(1, 1)),
            ylim=(0, 4), yticks=list(range(0, 4001, 500)))
    ax2.bar_label(ax2.containers[0], fmt='%d', padding=3)
    ax2.set_title("CO2")

    ax3.bar(x, part, width=1, edgecolor="white", linewidth=0.7)
    ax3.set(xlim=(1, 1), xticks=list(range(1, 1)),
            ylim=(0, 4), yticks=list(range(0, 20, 2)))
    ax3.bar_label(ax3.containers[0], fmt='%d', padding=3)
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
    return render_template('mqtt.html', esp_bat_stat=esp_bat_stat, humidity=humidity, 
                           temperature=temperature, Tvoc=Tvoc,)

@app.route('/bath')
def bath():
    bath_data = bath_temp()
    return render_template('bath.html', bath_data=bath_data)

@app.route('/bedroom')
def bedroom():
    bedgraph_data = bedroom_temp()
    return render_template('bedroom.html', bedgraph_data=bedgraph_data)

@app.route('/livingroom')
def livingroom():
    stue_temperature = stue_temp()
    stue_data = stue_data_co2_tvoc_part()
    part_air = part_in_air()
    return render_template('livingroom.html', stue_temperature=stue_temperature, 
                           stue_data=stue_data, part_air=part_air)

@app.route('/taend/', methods=['POST', 'GET'])
def taend():
    publish.single("sensor/stue/fan", "1", hostname="localhost")
    stue_temperature = stue_temp()
    stue_data = stue_data_co2_tvoc_part()
    part_air = part_in_air()
    return render_template('livingroom.html', stue_temperature=stue_temperature, 
                           stue_data=stue_data, part_air=part_air)

@app.route('/sluk/', methods=['POST', 'GET'])
def sluk():
    publish.single("sensor/stue/fan", "0", hostname="localhost")
    stue_temperature = stue_temp()
    stue_data = stue_data_co2_tvoc_part()
    part_air = part_in_air()
    return render_template('livingroom.html', stue_temperature=stue_temperature, 
                           stue_data=stue_data, part_air=part_air)

@app.route('/config')
def config():
    return render_template('config.html')
