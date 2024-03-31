import { Connection, Channel, ConsumeMessage } from "amqplib";
const client = require("amqplib");

const rmqUser = "guest";
const rmqPass = "guest";

const rmqhost = process.env.AMQP_HOST || "rabbitmq";

export class RabbitMQConnection {
  connection!: Connection;
  channel!: Channel;
  private connected!: Boolean;

  async connect() {
    if (this.connected && this.channel) return;
    else this.connected = true;

    try {
      console.log(`⌛️ Connecting to Rabbit-MQ Server`);
      console.log(client)
      this.connection = await client.connect(
        {
          hostname: rmqhost,
          port: 5672,
          // vhost: '/',
          clientProperties: {
            connection_name: 'create_blocked_slot'
          }
        }
      );

      console.log(`✅ Rabbit MQ Connection is ready`);

      this.channel = await this.connection.createChannel();

      console.log(`🛸 Created RabbitMQ Channel successfully`);
    } catch (error) {
      console.error(error);
      console.error(`Not connected to MQ Server`);
    }
  }

  async sendToQueue(queue: string, message: any) {
    try {
      if (!this.channel) {
        await this.connect();
      }

      this.channel.sendToQueue(queue, Buffer.from(JSON.stringify(message)));
    } catch (error) {
      console.error(error);
      throw error;
    }
  }
}

const mqConnection = new RabbitMQConnection();

export default mqConnection;