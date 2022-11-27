class Broker:
    def __init__(self, text_list_obj):
        self.text_list_obj = text_list_obj

    def publish_text(self, text, **kwargs):
        self.text_list_obj.add_text(text)
