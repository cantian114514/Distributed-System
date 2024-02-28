import grpc
import time
import proto.pubsub_pb2
import proto.pubsub_pb2_grpc

from threading import Event
from concurrent import futures

_HOST = 'localhost'
_PORT = '50051'

class Pubsub(object):
    def __init__(self): #初始化
        self.storage = {} #已发布消息
        self.event = {} #是否订阅
    
    def publish(self, topic, message): #发布消息
        new_message = ''
        add_message = {'create time':time.time(), 'message': message}
        if topic not in self.storage: #存储发布消息
            self.storage[topic] = [add_message]
            new_message += f"create topic:{topic}\n"
        else:
            self.storage[topic].append(add_message)
        new_message += 'successfully publish'

        if topic in self.event: #检查是否有客户端订阅消息
            for client in self.event[topic]:
                self.event[topic][client].set() #将该事件设为已设置（线程通信）

        return new_message

    def refresh(self, TTL = 5): #更新时间 超时则删除
        t = time.time() - TTL
        for topic in self.storage: # 检查消息库里的所有消息
            while len(self.storage[topic]) and self.storage[topic][0]['create time'] <= t:
                del self.storage[topic][0] #在该主题下有消息且该消息时间过久时 删除

    def subcribe(self, topic, clientID, TTL = 10): #订阅某消息
        T1 = time.time()
        T2 = TTL
        if topic not in self.event: #该订阅行为未被创建过 现创建
            self.event[topic] = {}
        self.event[topic][clientID] = Event() #创建事件
        while T2 > 0:
            if topic in self.storage and len(self.storage[topic]) > 0:
                m = self.storage[topic][-1] #最新的一条消息
                msg = str(m['create time']) + ":" + m['message']
                yield msg
                self.event[topic][clientID].clear() # 确保循环结束时状态为unset
            else:
                self.event[topic][clientID].wait(timeout=1) #等待1秒
                T2 = TTL - (time.time() - T1) #更新剩余时间
        return None #超时仍未收到消息，则返回none

class PubsubServer(proto.pubsub_pb2_grpc.Pubsub): #实现pubsub.proto中的功能
    def __init__(self):
        self.pubsub = Pubsub()
    
    def publish(self, request, context):
        result = self.pubsub.publish(request.topic, request.context)
        response = proto.pubsub_pb2.reply(message = result)
        return response

    def subcribe(self, request, context):
        for result in self.pubsub.subcribe(request.topic, request.clientID, request.TTL):
            response = proto.pubsub_pb2.reply(message = result)
            yield response

def serve():
    pubsubserver = PubsubServer()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10)) # 创建grpc服务器，最大工作线程数为10
    proto.pubsub_pb2_grpc.add_PubsubServicer_to_server(pubsubserver, server) #将pubsubserver加入到服务器中
    server.add_insecure_port('[::]:'+_PORT) #服务器上添加端口 监听
    server.start()
    try:
        while True:
            time.sleep(1)
            pubsubserver.pubsub.refresh()
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    print("Hello! client!")
    serve()