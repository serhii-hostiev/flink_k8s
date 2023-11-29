"""A Python Pulumi program"""
import pulumi

from components.flink import Flink_k8s
from components.oracle import Oracle_k8s
from components.kafka import Kafka_k8s
from components.kafka_ui import Kafka_ui_k8s

stack = pulumi.get_stack()

if stack == "flink":
    flink = Flink_k8s()

if stack == "oracle":
    oracle = Oracle_k8s()

if stack == "kafka":
    kafka = Kafka_k8s()

if stack == "kafka-ui":
    kafka = Kafka_ui_k8s()
