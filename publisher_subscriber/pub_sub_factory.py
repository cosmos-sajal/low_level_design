from text_list import TextList
from broker import Broker
from consumer import ConsumerManager
from publisher import Publisher


class PublisherFactory:
    def __init__(self):
        self.consumer_manager = None

    def get_publisher(self, **kwargs):
        override_fn = kwargs.pop('override_fn', None)
        text_list_obj = TextList()
        broker = Broker(text_list_obj)
        self.consumer_manager = ConsumerManager(
            4, text_list_obj, override_fn=override_fn)
        pub = Publisher(broker)

        return pub

    def remove_publisher(self):
        self.consumer_manager.remove_consumers()
