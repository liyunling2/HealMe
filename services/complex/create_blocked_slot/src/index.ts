import { Hono } from 'hono';
import { createInvalidSlotResponse, isDoctorIDValid, isFreeOfConflict } from './utils';
import { validateBlockedSlot } from './validation';

const app = new Hono();

app.get("/", (c) => {
    return c.json({ message: "Hello, World!" });
});

app.post("/", async (c) => {
  // get blocked Slot from request body
  const blockedSlot = await c.req.json() as BlockedSlotType;
  const schemaValidationResult = validateBlockedSlot(blockedSlot);

  if (!schemaValidationResult.valid) {
    return createInvalidSlotResponse(c, schemaValidationResult.errors);
  }

  const doctorID = blockedSlot.doctorID;
  const doctorIsValid: boolean = await isDoctorIDValid(doctorID);

  if (!doctorIsValid) {
    c.status(400);
    return c.json({ message: "Doctor not found" });
  }

  const freeOfConflict = await isFreeOfConflict(blockedSlot);

  if (!freeOfConflict) {
    c.status(400);
    return c.json({ message: "Slot conflict" })
  }

//   await createBlockedSlot(blockedSlot);

  return c.json({ wow: "hello" })
})

export default {
  port: process.env.CREATE_BLOCKED_SLOT_PORT! ?? 50000,
  fetch: app.fetch,
}


