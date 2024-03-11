import { expect, test } from "bun:test";
import { isFreeOfConflict } from "../src/utils";
import exp = require("constants");

const blockedSlot = {
    "doctorID": "123e4567-e89b-12d3-a456-426614174000",
    "clinicID": "123e4567-e89b-12d3-a456-426614174001",
    "date": "2022-01-01",
    "slotNo": 2,
    "reason": "Unavailable"
};

const noConflicts = {
    data: []
};

const conflictSlots = [
    {
        "doctorID": "123e4567-e89b-12d3-a456-426614174000",
        "clinicID": "123e4567-e89b-12d3-a456-426614174001",
        "date": "2022-01-01",
        "slotNo": 2,
        "reason": "Unavailable"
    }
];

test("no conflict", async () => {

    //@ts-ignore
    global.fetch = async (url: string) => {
        return {
            status: 200,
            json: async () => {
                return noConflicts;
            },
        } as any;
    }

    const freeOfConflict = await isFreeOfConflict(blockedSlot);
    expect(freeOfConflict).toBe(true);
});

test("conflict", async () => {
    //@ts-ignore
    global.fetch = async (url: string) => {
        return {
            status: 200,
            json: async () => {
                return conflictSlots;
            },
        } as any;
    }

    const hasConflict = await isFreeOfConflict(blockedSlot);
    expect(hasConflict).toBe(false);
})