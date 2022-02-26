from channels.consumer import SyncConsumer

class ChatConsumer(SyncConsumer):
    def websocket_connect(self, event):
        print("consumer connect event")

    def websocket_receive(self, event):
        print("new event is received")
        print(event)