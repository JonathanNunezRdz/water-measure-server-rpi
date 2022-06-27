from time import sleep
from paho.mqtt import client as mqtt_client

broker = '192.168.1.73'
port = 4001
topic = 'presence'
client_id = 'raspberry-pi-jonas'
username = 'jonas'
password = '1793'

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0: print("Connceted to MQTT Broker")
        else: print("Failed to connect to MQTT Broker")
    
    client = mqtt_client.Client(client_id, True, None, mqtt_client.MQTTv31)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port=port)
    return client

def publish(client: mqtt_client.Client):
    msg_count = 0
    while True:
        sleep(1)
        msg = "messages: {}".format(msg_count)
        result = client.publish(topic, msg)
        status = result[0]
        if status == 0:
            print('Send {} to topic {}'.format(msg, topic))
        else:
            print('Failed to send message to topic {}'.format(topic))
        msg_count += 1

def main():
    client = connect_mqtt()
    client.loop_start()
    # publish(client)

if __name__ == '__main__':
    main()
