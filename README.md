# MQTT_Sensor_Data
Zenatix MQTT Assignment

How to use-
  1) First execute subscribe.py via terminal, command- python subscribe.py.
  2) Then execute publish.py via another terminal window, command- python publish.py.
  3) You can see when the data is published in publish window, the data is recieved in subscribe window.

Important Points-
  1) Details about config.json-
    - MQTT URL, Port and Topic (if you recieve some other data than published one, try changing topic, default topic is "sensor_data").
    - Publish time interval and alert time interval in seconds (Default- 60 secs and 300 secs respectively).
    - In sensors field, we can add more sensors, currently there are temperature and humidity sensors.
    - Both sensors have unit, optimal range and simulate range fields. Optimal range is the range that we need for the factory to run pefectly. Simulate range is the range that         we are simulating for testing.     
    - Simulate range is kept higher than optimal range by default so as to recieve alerts by mail as we'll recieve higher values.
    - Alert field has alert mail, humidity alert message and temperature alert message fields, all which can be edited as per need. Alert mail is the mail where we'll recieve the        alert notifications.
   
  2) I have used a custom gmail account to send alert mails. Mail ID- mqtt.sensor.data@gmail.com
  
  3) The subscribe.py script is set to forever loop so after it sends out alerts, it'll still run.
  
  4) The script sends alerts when the average of temperature and humidity values recieved are above max range of optimal value for certain duration of time. This time can be            changed by changing alert time interval field in config file. (Defalut max range is 28C for temperature and 80% for humidity)
  
  5) Public MQTT broker used is Eclipse.
