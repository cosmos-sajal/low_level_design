class Publisher:
    def __init__(self, broker):
        self.broker_obj = broker

    def publish_text(self, text):
        self.broker_obj.publish_text(text)
