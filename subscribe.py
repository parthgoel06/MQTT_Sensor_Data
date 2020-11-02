########### LIBRARIES ############
import paho.mqtt.client as mqtt
import json
import datetime
import smtplib
##################################


########################### CONFIG_FILE ###############################
with open("config.json") as openfile:                                   # read config file
    config = json.load(openfile)

mqtt_config = config.get("mqtt")                                        # mqtt config
broker_url = mqtt_config['broker_url']
broker_port = mqtt_config['broker_port']

topic = mqtt_config["topic"]                                            # topic to subscribe at (default- "sensor_data")
sensors = config.get("sensors")                                         # read all sensor config
alert_time = config.get("time_seconds")["alert_time_interval"]          # time to alert at (default- 300 secs or 5 min.)
alert_mail_id = config.get("alert")["alert_mail"]                       # read alert mail address from config
humidity_alert_msg = config.get("alert")["humidity_alert_msg"]          # read humidity alert message from config
temp_alert_msg = config.get("alert")["temp_alert_msg"]                  # read temperature alert message from config
#######################################################################


####################### HUMIDITY_ALERT_FUNCTION #######################
ls1 = []
t_humidity = 0
def humidity_alert(humidity_int_value, humidity_alert_value):
   global ls1
   global t_humidity

   if len(ls1) > 0:
      ls1.append(humidity_int_value)

      if sum(ls1)/len(ls1) > humidity_alert_value:                        # average of humidity greater than alert value (default- 80%)
         t = datetime.datetime.now()
         delta = t - t_humidity
         delta = int(delta.total_seconds())        

         if delta >= alert_time:                                          # if time elapsed greater or equal to alert time (default)
            alert_mail(alert_mail_id, humidity_alert_msg)
            print("HUMIDITY ALERT HAS BEEN SENT")
      
      else:
         ls1 = []
   
   if len(ls1) == 0 and humidity_int_value > humidity_alert_value:
      ls1.append(humidity_int_value)
      t_humidity = datetime.datetime.now()
#######################################################################


######################### TEMP_ALERT_FUNCTION #########################
ls2 = []
t_temp = 0
def temp_alert(temp_int_value, temp_alert_value):
   global ls2
   global t_temp

   if len(ls2) > 0:
      ls2.append(temp_int_value)

      if sum(ls2)/len(ls2) > temp_alert_value:                        # average of humidity greater than alert value (default- 80%)
         t = datetime.datetime.now()
         delta = t - t_temp
         delta = int(delta.total_seconds())        

         if delta >= alert_time:                                      # if time elapsed greater or equal to alert time (default)
            alert_mail(alert_mail_id, temp_alert_msg)
            print("TEMPERATURE ALERT HAS BEEN SENT")
      
      else:
         ls2 = []
   
   if len(ls2) == 0 and temp_int_value > temp_alert_value:
      ls2.append(temp_int_value)
      t_temp = datetime.datetime.now()
#######################################################################


###################### ALERT_MAIL_FUNCTION ############################
def alert_mail(mail_address, msg):
   server = smtplib.SMTP_SSL('smtp.gmail.com', 465)                     
   server.login("mqtt.sensor.data", "sensor_data")                       # custom gmail account credentials for this project
   server.sendmail(
   "mqtt.sensor.data@gmail.com", 
   mail_address, 
   msg)
   server.quit()
#######################################################################


########################### MQTT ######################################
def on_connect(client, userdata, flags, rc):
   print(f"Connected With Result Code: {rc}")

def on_message(client, userdata, message):
   msg = message.payload.decode()
   print("Data Recieved: "+msg)

   values = msg.split(',')
   temp_value = values[0].split('=')
   humidity_value = values[1].split('=')
   temp_int_value = int(temp_value[1][0:-1])                              # extract temp value from msg string 
   humidity_int_value = int(humidity_value[1][0:-1])                      # extract humidity value from msg string 
   humidity_alert_value = sensors['humidity']['optimal_range'][1]         # read humidity alert value from config (default- 80% (max value of optimal range))
   temp_alert_value = sensors['temperature']['optimal_range'][1]          # read temp alert value from config (default- 28C (max value of optimal range))

   humidity_alert(humidity_int_value, humidity_alert_value)
   temp_alert(temp_int_value, temp_alert_value)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker_url, broker_port)
client.subscribe(topic, qos=1)

client.loop_forever()
########################################################################

