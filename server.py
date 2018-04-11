import pika
import importlib
import ast
import pkgutil
import time

URL = 'amqp://fltduuba:Ab5hRre535jg--4YYVXAfgcq11_O57-F@mustang.rmq.cloudamqp.com/fltduuba'
class Server:
    def __init__(self):
        # self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        
        parameters = pika.URLParameters(URL)
        self.connection = pika.BlockingConnection(parameters)

        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='worker_queue')


    def process_request(self, request):

        if request == '__modules__':
            modules_available = [name for _, name, _ in pkgutil.iter_modules(['registry'])]
            return modules_available

        request = ast.literal_eval(request)
        module_name = request[0]
        param = request[1]

        try:
            module = importlib.import_module('registry.' + module_name)
            return getattr(module, 'call')(param)

        except:
            return 'Module not found'


    def on_request(self, ch, method, props, body):
        start_time = time.time()
        request = body.decode()
        print('Request :', request)

        response = self.process_request(request)
        print('Response :', response)
        print('Time taken :', time.time() - start_time, 'seconds\n')

        ch.basic_publish(exchange='',
                         routing_key=props.reply_to,
                         properties=pika.BasicProperties(correlation_id = props.correlation_id),
                         body=str(response))

        ch.basic_ack(delivery_tag = method.delivery_tag)


    def run(self):
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(self.on_request, queue='worker_queue')

        print('Waiting for requests...\n')
        self.channel.start_consuming()


def main():
    server = Server()
    server.run()
    

if __name__ == '__main__':
    main()
