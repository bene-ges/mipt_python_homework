# реализация сервера для тестирования метода get по заданию - Клиент для отправки метрик
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket

class Server:
    def __init__(self, host, port):
        assert(host != ""), "empty host"
        assert(port > 1023 and port <= 65535), "port should be integer between 1024 and 65535, got " + str(port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((host, port))
        self.sock.listen(1)
        self.database = {}

    def __del__(self):
        self.sock.close()

    def run(self):
        while True:
            conn, addr = self.sock.accept()
            print('Соединение установлено:', addr)
            while True:
                # предполагаем, что запросы у нас короткие и будут всегда целиком влезать в 1024 байта
                data = conn.recv(1024)
                if not data:
                    break
                request = data.decode('utf-8')
                print(f'Получен запрос: {ascii(request)}')
                response = self.process_request(request)
                print('Отправлен ответ ', response)
                conn.sendall(response.encode("utf-8"))
            conn.close()
   
    def process_request(self, request):
        #put palm.cpu 23.7 1150864247\n
        #get palm.cpu\n
        #get *\n
        parts = request.strip().split()
        if parts[0] == 'put':
            if len(parts) != 4:
                return "error\nwrong command\n\n"
            metric, percentage, timestamp = parts[1:]
            try:
                percentage = float(percentage)
                timestamp = int(timestamp)
            except:
                return "error\nwrong command\n\n"
            else:
                return self.put(metric, percentage, timestamp)
        else:
            if parts[0] != 'get':
                return "error\nwrong command\n\n"
            if len(parts) != 2:
                return "error\nwrong command\n\n"
            if parts[1] == '*':
                return self.get_all()
            else:
                return self.get(metric)

    def put(self, metric, percentage, timestamp):
        self.database.setdefault(metric, dict())
        self.database[metric][timestamp] = percentage
        return "ok\n\n"

    def get_all(self):
        strs = []
        for metric in self.database:
            for timestamp in self.database[metric]:
                percentage = self.database[metric][timestamp]
                strs.append(metric + " " + str(percentage) + " " + str(timestamp))
        if len(strs) > 0:
            return "ok\n" + "\n".join(strs) + "\n\n"
        else:
            return "ok\n\n"

    def get(self, metric):
        strs = []
        for timestamp in self.database[metric]:
            percentage = self.database[metric][timestamp]
            strs.append(metric + " " + str(percentage) + " " + str(timestamp))
        if len(strs) > 0:
            return "ok\n" + "\n".join(strs) + "\n\n"
        else:
            return "ok\n\n"

# переменная response хранит строку возвращаемую сервером, если вам для
# тестирования клиента необходим другой ответ, измените ее
#response = b'ok\npalm.cpu 10.5 1501864247\neardrum.cpu 15.3 1501864259\n\n'


if __name__ == "__main__":
    server = Server("127.0.0.1", 8888)
    server.run()
