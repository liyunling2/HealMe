import { Context } from "hono";
import { ValidationError } from "jsonschema";
import { formatValidationErrors } from "./validation";
import axios from "axios";

export function createInvalidSlotResponse(c: Context, aggregateError: AggregateError) {
    return c.json({
        "errors": aggregateError.errors,
        "message": "Bad request. See errors"
    }, 400);
}

export function createNormalErrorResponse(c: Context, error: Error) {
    return c.json({ errors: [error.message] }, 500);
}

export function createSlotSuccessResponse(c: Context, blockedSlot: BlockedSlotType) {
    return c.json({
        message: "Slot created successfully",
        data: blockedSlot
    }, 201);
}

export async function createBlockedSlot(blockedSlot: BlockedSlotType): Promise<{ data: BlockedSlotType }> {
    const response = await fetch(process.env.BLOCKED_SLOTS_URL ?? "http://localhost:5002", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(blockedSlot)
    });

    const data = await response.json();

    if (response.ok)
        return await data;

    throw new Error("Error creating slot");
}

export async function isDoctorIDValid(doctorID: string): Promise<boolean> {
    const response = await fetch((process.env.PROFILE_URL
        ?? "http://localhost:5003") + `/doctors/${doctorID}`);

    if (response.ok && isResponseJson(response)) {
        const body = await response.json();
        const doctor = body

        if (doctor)
            return true;
    }

    throw new Error("Error fetching doctor");
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
    return await getMatchingItemsFromParams(params, process.env.BLOCKED_SLOTS_URL ?? "http://localhost:5001", "Error fetching slots");
}

export async function hasNoConflictingBookings(blockedSlot: BlockedSlotType): Promise<boolean> {
    return await hasNoConflictingItems(blockedSlot, getMatchingBookingsFromParams);
}

async function getMatchingBookingsFromParams(params: URLSearchParams): Promise<any[] | null> {
    return await getMatchingItemsFromParams(params, process.env.BOOKINGS_URL ?? "http://localhost:5005/bookings", "Error fetching bookings");
}

async function getMatchingItemsFromParams(params: URLSearchParams, url: string, errorMessage: string = "Error fetching items"): Promise<any[] | null> {
    const fullUrl =  url + "?" + params;
    const response = await fetch(fullUrl);

    if (response.ok && isResponseJson(response)) {
        const body = await response.json();
        const matchingItems = body?.data;

        return matchingItems;
    }

    throw new Error(errorMessage);
}

function isResponseJson(response: Response): boolean {
    return response.headers.get("Content-Type")?.includes("application/json") ?? false;
}