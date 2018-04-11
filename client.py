import pika
import uuid
import sys
import ast

URL = 'amqp://fltduuba:Ab5hRre535jg--4YYVXAfgcq11_O57-F@mustang.rmq.cloudamqp.com/fltduuba'

class Client(object):

    def __init__(self):
        # self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        
        parameters = pika.URLParameters(URL)
        self.connection = pika.BlockingConnection(parameters)        

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(self.on_response, no_ack=True, queue=self.callback_queue)


    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body


    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange='',
                                   routing_key='worker_queue',
                                   properties=pika.BasicProperties(
	                                         reply_to = self.callback_queue,
	                                         correlation_id = self.corr_id,
                                    	),
                                   body=str(n))
        
        while self.response is None:
            self.connection.process_data_events()

        return self.response.decode()


def main():
    client = Client()

    print('Fetching list of available modules from server..\n')
    request = '__modules__'
    response = client.call(request)

    modules = ast.literal_eval(response)

    while True:
        for i, module in enumerate(modules):
            print('{}. {}'.format(i+1, module))

        choice = input('Choose module: ')
        try:
            module = modules[int(choice) - 1]
        except:
            print('Invalid module\n')
            continue

        param = input('Parameter: ')
        request = (module, param)

        print('Request : ', request)
        response = client.call(request)
        print('Response : ', response, '\n')
    	

if __name__ == '__main__':
	main()
