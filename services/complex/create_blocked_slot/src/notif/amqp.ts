import { AMQPChannel, AMQPClient } from "@cloudamqp/amqp-client"
import { AMQPBaseClient } from "@cloudamqp/amqp-client/types/amqp-base-client";

const client = new AMQPClient("amqp://guest:guest@rabbitmq:5672/");

export class RabbitMQConnection {
  connection!: AMQPBaseClient
  channel!: AMQPChannel
  private connected!: Boolean;

  async connect() {
    if (this.connected && this.channel) return;
    else this.connected = true;

    try {
      console.log(`⌛️ Connecting to Rabbit-MQ Server`);
      this.connection = await client.connect();

      console.log(`✅ Rabbit MQ Connection is ready`);

      this.channel = await this.connection.channel()

      console.log(`🛸 Created RabbitMQ Channel successfully`);
    } catch (error) {
      console.error(error);
      console.error(`Not connected to MQ Server`);
    }
  }

}

const mqConnection = new RabbitMQConnection();

export default mqConnection;