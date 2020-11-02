import paho.mqtt.client as mqtt
import json
import random
import time

#Function to generate random integer between ranges(inclusive)
def rand_int(ls):
    return random.randint(ls[0], ls[1])


########################### CONFIG_FILE ###############################
with open("config.json") as openfile:                                   # read config file
    config = json.load(openfile)

mqtt_config = config.get("mqtt")                                        # mqtt config
broker_url = mqtt_config['broker_url']
broker_port = mqtt_config['broker_port']

topic = mqtt_config["topic"]                                            # topic to subscribe at (default- "sensor_data" )
sensors = config.get("sensors")
publish_time = config.get("time_seconds")["publish_time_interval"]      # publish interval time (default- 60 secs or 1 min.)
#######################################################################


#Code to publish data in interval time
while(True):
    data = f"Temp={rand_int(sensors['temperature']['simulate_range'])}{sensors['temperature']['unit']},Humidity={rand_int(sensors['humidity']['simulate_range'])}{sensors['humidity']['unit']}"

    client = mqtt.Client()
    client.connect(broker_url, broker_port)
    client.publish(topic = topic, payload = data, qos = 0, retain = False)
    print("Data Published: ", data)

    time.sleep(publish_time)