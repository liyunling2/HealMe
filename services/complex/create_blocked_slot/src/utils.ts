import { Context } from "hono";
import { ValidationError } from "jsonschema";
import { formatValidationErrors } from "./validation";

export function createInvalidSlotResponse(c: Context, aggregateError: AggregateError) {
    c.status(400);
    return c.json({
        "errors": aggregateError.errors,
        "message": "Bad request. See errors"
    });
}

export function createNormalErrorResponse(c: Context, message: string) {
    c.status(500);
    return c.json({ error: message });
}

export function createSlotSuccessResponse(c: Context, blockedSlot: BlockedSlotType) {
    c.status(201);
    return c.json({
        message: "Slot created successfully",
        data: blockedSlot
    });
}

export async function createBlockedSlot(blockedSlot: BlockedSlotType): Promise<Response> {
    return await fetch(process.env.BLOCKED_SLOTS_URL ?? "localhost:5002", {
        method: "POST",
        body: JSON.stringify(blockedSlot)
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

async function hasNoConflictingItems(blockedSlot: BlockedSlotType, getMatchingSlotFn: (params: URLSearchParams) => Promise<any[] | null>): Promise<boolean> {
    const { doctorID, date, slotNo } = blockedSlot;
    const params = new URLSearchParams({
        doctorID,
        date: date.toString(),
        slotNo: slotNo.toString()
    })    

    const matchingItems = await getMatchingSlotFn(params)

    if (matchingItems && matchingItems.length == 0)
        return true;

    return false;
}

export async function hasNoConflictingSlots(blockedSlot: BlockedSlotType): Promise<boolean> {
    return await hasNoConflictingItems(blockedSlot, getMatchingSlotsFromParams);
}

async function getMatchingSlotsFromParams(params: URLSearchParams): Promise<any[] | null> {
    const response = await fetch(process.env.BLOCKED_SLOTS_URL
        ?? "localhost:5002" + params);

    const body = await response.json();
    const matchingSlots = body?.data;

    return matchingSlots;
}

export async function hasNoConflictingBookings(blockedSlot: BlockedSlotType): Promise<boolean> {
    return await hasNoConflictingItems(blockedSlot, getMatchingBookingsFromParams);
}

async function getMatchingBookingsFromParams(params: URLSearchParams): Promise<any[] | null> {
    const response = await fetch(process.env.BOOKING_URL
        ?? "localhost:5005" + params);

    const body = await response.json();
    const matchingBookings = body?.data;

    return matchingBookings;
}
