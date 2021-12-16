import socket
import time

class ClientError(Exception):
    """Класс для генерации ошибок работы протокола"""
    pass

class Client:
    def __init__(self, host, port, timeout=None):
        assert(host != ""), "empty host"
        assert(port > 1023 and port <= 65535), "port should be integer between 1024 and 65535, got " + str(port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(timeout)
        self.sock.connect((host, port))

    def __del__(self):
        self.sock.close()

    def get(self, key):
        request = "get " + key + "\n"
        self.sock.send(request.encode("utf-8"))
        result = b''
        while True:
            data = self.sock.recv(1024)
            if data:
                result += data
            else:
                break
            if data.endswith(b"\n\n"): #ответ прочитан полностью
                break
        result = result.decode("utf-8")
        js = {}
        parts = result.strip().split("\n")
        if parts[0] != "ok":
            raise ClientError
        for p in parts[1:]:
            metric, percentage, timestamp = p.split(" ")
            percentage = float(percentage)
            timestamp = int(timestamp)
            js.setdefault(metric, list())
            js[metric].append((int(timestamp), float(percentage)))
        
        #сортируем списки в каждой метрике по возрастанию timestamp
        for metric in js:
            js[metric] = sorted(js[metric], key=lambda t: t[0])
        return js
    
    def put(self, metric, percentage, timestamp=None):
        if timestamp is None:
            timestamp = int(time.time())
        request = "put " + metric + " " + str(percentage) + " " + str(timestamp) + "\n"
        self.sock.send(request.encode("utf-8"))
        result = b''
        while True:
            data = self.sock.recv(1024)
            print("received ", data)
            if data:
                result += data
            else:
                break
            if data.endswith(b"\n\n"): #ответ прочитан полностью
                break
        result = result.decode("utf-8")  
        if result == "ok\n\n":
            return
        else:
            raise ClientError


if __name__ == "__main__":
    client = Client("127.0.0.1", 8888, timeout=15)
    client.put("palm.cpu", 0.5, timestamp=1150864247)
    client.put("palm.cpu", 2.0, timestamp=1150864248)
    client.put("palm.cpu", 0.5, timestamp=1150864248)
    client.put("eardrum.cpu", 3, timestamp=1150864250)
    client.put("eardrum.cpu", 4, timestamp=1150864251)
    client.put("eardrum.memory", 4200000)
    print(client.get("*"))


    