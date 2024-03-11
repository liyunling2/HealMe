import { Context } from "hono";
import { ValidationError } from "jsonschema";
import { formatValidationErrors } from "./validation";

export function createInvalidSlotResponse(c: Context, errors: ValidationError[]) {
    c.status(400);
    return c.json({
        "errors": formatValidationErrors(errors),
        "message": "Bad request. See errors"
    });
}

export async function isDoctorIDValid(doctorID: string): Promise<boolean> {
    const response = await fetch(process.env.BLOCKED_SLOTS_URL
        ?? "localhost:5001" + `doctors/${doctorID}`);
    
    if (response.status == 200) {
        const body = await response.json();
        const doctor = body?.doctor;

        if (doctor)
            return true;
    }
    
    return false;
}

export async function isFreeOfConflict(blockedSlot: BlockedSlotType): Promise<boolean> {
    // call blocked_slot service
    const { doctorID, date, slotNo } = blockedSlot;
    const params = new URLSearchParams({
        doctorID,
        date: date.toString(),
        slotNo: slotNo.toString()
    })

    const matchingSlots = await getMatchingSlotsFromParams(params);

    if (matchingSlots && matchingSlots.length == 0)
        return true;

    return false;
}

async function getMatchingSlotsFromParams(params: URLSearchParams): Promise<any[] | null> {
    const response = await fetch(process.env.BLOCKED_SLOTS_URL
        ?? "localhost:5002" + params);

    const body = await response.json();
    const matchingSlots = body?.data;

    return matchingSlots;
}

export async function createBlockedSlot(blockedSlot: BlockedSlotType): Promise<Response> {
    return await fetch(process.env.BLOCKED_SLOTS_URL ?? "localhost:5002", {
        method: "POST",
        body: JSON.stringify(blockedSlot)
    });
}