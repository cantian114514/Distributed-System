import grpc
import time
import threading
import proto.pubsub_pb2
import proto.pubsub_pb2_grpc

_HOST = 'localhost'
_PORT = '50051'

clientID = input("please enter an ID:")
channel = grpc.insecure_channel(_HOST + ':' + _PORT)
stub = proto.pubsub_pb2_grpc.PubsubStub(channel) #存根 封装

def publish(topic, context):
    msg1 = f"Publish message in {topic}:{context}"
    rsp = proto.pubsub_pb2.PubRequest(topic = topic, context = context)
    response = stub.publish(rsp)
    print(msg1,"\n",response.message)

def receive(topic, clientID, TTL):
    msg1=''
    msg2=''
    for msg in stub.subcribe(proto.pubsub_pb2.SubRequest(topic = topic, clientID = clientID, TTL = TTL)):
        msg1 = f"Receive message from {topic}:{msg.message}"
        if msg1 == msg2: #防止重复信息无限输出
            break
        print(msg1)
        msg2=msg1

def subcribe(topic, clientID, TTL = 10):
    msg1 = f"Successfully subcribe from {topic}"
    thread = threading.Thread(target=receive, args=(topic, clientID, TTL))
    print(msg1)
    thread.start()

publish('test_topic', 'message1')
time.sleep(5)
publish('test_topic', 'message2')
time.sleep(6)
subcribe('test_topic', clientID, 10)
publish('test_topic', 'message3')
