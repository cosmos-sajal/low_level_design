from threading import Thread
import time


class Consumer:
    def __init__(self, text_list_obj, consumer_number, **kwargs):
        self.override_fn = kwargs.pop('override_fn', None)
        self.text_list_obj = text_list_obj
        self.is_killed = False
        self.consumer_number = consumer_number
        t = Thread(
            target=self.consume_text,
            args=[]
        )
        t.start()

    def kill(self):
        print(f"{self.consumer_number}---consumer getting deleted---")
        self.is_killed = True

    def consume(self, text, *args, **kwargs):
        if self.override_fn is not None:
            self.override_fn(text, *args, **kwargs)
        else:
            print(f"{self.consumer_number}---Received message {text}---")

    def consume_text(self):
        while True:
            if len(self.text_list_obj.text_list) > 0 and \
                    not self.is_killed:
                text = self.text_list_obj.text_list.pop(0)
                self.consume(text)


class ConsumerManager:
    def __init__(self, no_of_consumers, text_list_obj, **kwargs):
        self.override_fn = kwargs.pop('override_fn', None)
        self.consumer_counter = 0
        self.consumer_list = []
        self.text_list_obj = text_list_obj
        self.add_consumers(no_of_consumers)

    def add_consumers(self, no_of_consumers):
        for i in range(0, no_of_consumers):
            self.consumer_list.append(
                Consumer(
                    self.text_list_obj,
                    self.consumer_counter,
                    override_fn=self.override_fn
                )
            )
            self.consumer_counter += 1

    def remove_consumers(self):
        time.sleep(5)
        print('--------Removing consumers--------')
        while (True):
            self.consumer_list[0].kill()
            del self.consumer_list[0]

            if len(self.consumer_list) == 0:
                break
