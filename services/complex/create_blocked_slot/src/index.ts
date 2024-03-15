import { Hono } from 'hono';
import { createBlockedSlot, createInvalidSlotResponse, isDoctorIDValid, hasNoConflictingSlots, hasNoConflictingBookings, createNormalErrorResponse } from './utils';
import { validateBlockedSlotSchema, formatValidationErrors } from './validation';

const app = new Hono();

app.get("/", (c) => {
    return c.json({ message: "Hello, World!" });
});

app.post("/", async (c) => {
  // get blocked Slot from request body
  const blockedSlot = await c.req.json() as BlockedSlotType;

  try {
    await checkValidBlockedSlot(blockedSlot);
    const res = await createBlockedSlot(blockedSlot);
    const body = await res.json();
    return c.json(body);
  }
  catch (error) {
    if (error instanceof AggregateError)
      return createInvalidSlotResponse(c, error);

    return createNormalErrorResponse(c, "Something went wrong. Please try again later.");
  }
})

async function checkValidBlockedSlot(blockedSlot: BlockedSlotType) {
  const schemaValidationResult = validateBlockedSlotSchema(blockedSlot);
  const errors = formatValidationErrors(schemaValidationResult.errors);

  const doctorIsValid = await isDoctorIDValid(blockedSlot.doctorID);

  if (!doctorIsValid)
    errors.push("Invalid doctorID");

  const noConflictingSlots = await hasNoConflictingSlots(blockedSlot);

  if (!noConflictingSlots)
    errors.push("Conflicting slot");

  const noConflictingBookings = await hasNoConflictingBookings(blockedSlot);  

  if (!noConflictingBookings)
    errors.push("Conflicting booking");

  if (errors.length > 0)
    throw new AggregateError(errors);
}

export default {
  port: process.env.CREATE_BLOCKED_SLOT_PORT! ?? 50000,
  fetch: app.fetch,
}


