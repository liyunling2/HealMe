import { Hono } from 'hono';
import { createInvalidSlotResponse, createNormalErrorResponse } from './responseUtils';
import createBlockedSlot from '../controllers/blockedSlotController';
import SlotNotAllowedError from '../common/SlotNotAllowedError';
import SlotInvalidError from '../common/SlotInvalidError';
import { StatusCode } from 'hono/utils/http-status';

const app = new Hono();

console.log(process.env.CREATE_BLOCKED_SLOT_URL);

app.get("/", (c) => {
    return c.json({ message: "Hello, World!" });
});

app.post("/", async (c) => {
  // get blocked Slot from request body
  const blockedSlot = await c.req.json();

  try {
    const body = await createBlockedSlot(blockedSlot);
    return c.json(body, 201);
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

export default {
  port: process.env.CREATE_BLOCKED_SLOT_PORT! ?? 50000,
  fetch: app.fetch,
}
