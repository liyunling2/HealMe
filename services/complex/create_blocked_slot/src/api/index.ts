import { Context, Hono } from 'hono';
import { createInvalidSlotResponse, createNormalErrorResponse } from './responseUtils';
import createBlockedSlot from '../controllers/blockedSlotController';
import SlotNotAllowedError from '../common/SlotNotAllowedError';
import SlotInvalidError from '../common/SlotInvalidError';
import { StatusCode } from 'hono/utils/http-status';
import mqConnection, { RabbitMQConnection } from '../notif/amqp';
// import pub from '../notif/amqp';
import { fetchDoctorWithParams } from '../data/dataFetchers';
import { Channel, Connection } from 'amqplib';

const app = new Hono();

console.log(process.env.CREATE_BLOCKED_SLOT_URL);

app.get("/", (c) => {
    return c.json({ message: "Hello, World!" });
});

// class MQChannel {
//   mqConnection: RabbitMQConnection;
//   channel: Channel;

//   constructor(mqConnection: Connection) {
//     this.mqConnection = mqConnection;
//     this.channel = null
//   }

//   async getChannel() {
//     if (this.channel === null)
//       this.channel = await this.mqConnection.connection.createChannel();
//     return this.channel;
//   }
// }

// const channel = new MQChannel(mqConnection.connection);

async function notify(context: { data: BlockedSlotType, status: number }) {
  console.log("Notifying");
  const { data, status } = context;

  if (status !== 201)
    return;

  const { doctorID, slotNo, date } = data;

  let doctorEmail: string = "";

  try {
    // doctorEmail = await fetchDoctorWithParams(new URLSearchParams({ doctorID })).then(data => (data as { email: string }).email);
    doctorEmail = "seanlim2@gmail.com"
  }
  catch (error) {
    console.error(error);
    return;
  }

  const timeNum =  7 + (slotNo - 1) * 0.5;
  const toTimeStr = (timeNum: number) => `${Math.floor(timeNum)}:${timeNum % 1 == 0 ? "00" : "30"}`;

  await mqConnection.connect();
  await mqConnection.channel.publish(
    'direct_exchange',
    'email.notification.request',
    Buffer.from(JSON.stringify({
      from: "healmeesd@gmail.com",
      to: doctorEmail,
      subject: "Blocked Slot Created",
      content: {
          title: "Blocked Slot Created",
          message: `You have blocked out a slot on ${date} from ${toTimeStr(timeNum)} to ${toTimeStr(timeNum + 0.5)}`
      }
    })
    ))
  console.log("published")
}

// app.post("/", notify);
app.post("/", async (c) => {
  // get blocked Slot from request body
  const blockedSlot = await c.req.json();

  try {
    const body = await createBlockedSlot(blockedSlot);

    // @ts-expect-error
    notify({ data: body?.data, status: 201 }).then(() => console.log("Notification requested"));

    return c.json(body);
  }

  catch (error) {
    // show stack trace
    let code: StatusCode = 500;

    if (error instanceof SlotNotAllowedError || error instanceof SlotInvalidError)
      code = 400;

    console.trace(error);
    return createNormalErrorResponse(c, error as Error, code);
  }
})

process.on("SIGINT", async () => {
  await mqConnection?.connection.close();
  process.exit(0);
})

process.on("SIGTERM", async () => {
  await mqConnection?.connection.close();
  process.exit(0);
})

export default {
  port: process.env.CREATE_BLOCKED_SLOT_PORT! ?? 50000,
  fetch: app.fetch,
}
