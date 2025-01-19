from aiokafka import AIOKafkaProducer


class KafkaManager:
    def __init__(self, servers: str, topic: str):
        self.servers = servers
        self.topic = topic
        self.producer = None

    async def startup(self):
        self.producer = AIOKafkaProducer(bootstrap_servers=self.servers)
        await self.producer.start()

    async def shutdown(self):
        if self.producer:
            await self.producer.stop()

    async def send_message(self, message: dict):
        if not self.producer:
            raise RuntimeError("Kafka producer is not initialized.")
        await self.producer.send_and_wait(self.topic, value=str(message).encode("utf-8"))

kafka_manager = KafkaManager(servers="kafka:9092", topic="applications")
