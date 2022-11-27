from pub_sub_factory import PublisherFactory


def consumer_consume(text):
    print(f'Overriding consumer, consume - {text}')


factory = PublisherFactory()
# publisher = factory.get_publisher()
# Overriding the consumer function
publisher = factory.get_publisher(
    override_fn=consumer_consume)
publisher.publish_text("text 1")
publisher.publish_text("text 2")
publisher.publish_text("text 3")
publisher.publish_text("text 4")
publisher.publish_text("text 5")
publisher.publish_text("text 51")
publisher.publish_text("text 52")
publisher.publish_text("text 53")
