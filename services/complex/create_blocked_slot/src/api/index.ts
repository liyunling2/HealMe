import { Context, Hono } from 'hono';
import { createInvalidSlotResponse, createNormalErrorResponse } from './responseUtils';
import createBlockedSlot from '../controllers/blockedSlotController';
import SlotNotAllowedError from '../common/SlotNotAllowedError';
import SlotInvalidError from '../common/SlotInvalidError';
import { StatusCode } from 'hono/utils/http-status';
import mqConnection from '../notif/amqp';
import { loggingHandlerFactory } from '../notif/log';
// import pub from '../notif/amqp';
import notify from '../notif/notify';

const app = new Hono();

console.log(process.env.CREATE_BLOCKED_SLOT_URL);

app.get("/", (c) => {
    return c.json({ message: "Hello, World!" });
});

// app.post("/", loggingHandlerFactory(mqConnection));

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
