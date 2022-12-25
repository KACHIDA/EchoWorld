# from xvfbwrapper import Xvfb

from confluent_kafka import Producer
from confluent_kafka import Consumer
from robot.libraries.BuiltIn import BuiltIn
from collections import OrderedDict


import io
import json
import uuid
import robot
import robot.libraries

input_msg = ""
receivedMsg = ""

transactionId = uuid.uuid4()

print("============== Start of Functional Block Robot execution ==============")

""" Kafka Consumer to receive the json message and process it """
consumer_conf = {
    "bootstrap.servers": "kafka:9092",
    "group.id": "command_consumer_group_01",
    "auto.offset.reset": "earliest",
}

""" Kafka Producer to send the json message and process it """
producer_conf = {"bootstrap.servers": "kafka:9092"}


consumer = Consumer(consumer_conf)


def consumer_loop(consumer, topics):
    running = True
    try:
        print(" polling started : " + topics[0])
        consumer.subscribe(topics)
        while running:
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                print(msg)
                print("error")
            else:
                """once the message is processed , stop the kafka consumer"""
                print("Received message: {}".format(msg.value().decode("utf-8")))
                receivedMsg = msg.value().decode("utf-8")
                jsonData = json.loads(receivedMsg)
                print(jsonData)
                print(type(jsonData))
                requestParams = (
                    "dict_args:{"
                    + '"message"'
                    + ":"
                    + '"'
                    + jsonData["message"]
                    + '"'
                    + ","
                    + '"commandId"'
                    + ":"
                    + '"'
                    + str(jsonData["commandId"])
                    + '"'
                    + ","
                    + '"SLA"'
                    + ":"
                    + str(jsonData["SLA"])
                    + ","
                    + '"SLA_unit"'
                    + ":"
                    + '"'
                    + jsonData["SLA_unit"]
                    + '"'
                    + ","
                    + '"execution_time"'
                    + ":"
                    + '"'
                    + str(jsonData["execution_time"])
                    + '"'
                    + ","
                    + '"execution_time_unit"'
                    + ":"
                    + '"'
                    + jsonData["execution_time_unit"]
                    + '"'
                    + "}"
                )
                robot.run(
                    "./robots/tasks.robot",
                    variable=requestParams,
                )
                print(
                    "============== Completion of Functional Block Robot execution =============="
                )
                #    vdisplay.stop()
                running = False

    finally:
        consumer.close()


running = True
consumer_loop(consumer, ["command_topic"])


""" Kafka Producer to send the json message and process it """
p = Producer({"bootstrap.servers": "kafka:9092"})


def delivery_report(err, msg):
    if err is not None:
        print("Message delivery failed: {}".format(err))
    else:
        print("Message delivered to {} [{}]".format(msg.topic(), msg.partition()))


data_str = (
    "echo message From RobotFramework, transaction : "
    + str(transactionId)
    + " is processed"
)

p.produce("event_topic", data_str.encode("utf-8"), callback=delivery_report)

p.flush()


# send response message to events kafka topic


# Initialize the X virtual framebuffer
# def robot_execution():
# vdisplay = Xvfb()
# vdisplay.start()
