import { Context } from "hono";
import { StatusCode } from "hono/utils/http-status";

export function createInvalidSlotResponse(c: Context, aggregateError: AggregateError) {
    return c.json({
        "errors": aggregateError.errors,
        "message": "Bad request. See errors"
    }, 400);
}

export function createNormalErrorResponse(c: Context, error: Error, code: StatusCode = 500) {

    if (error instanceof AggregateError) {
        const errors = error.errors;

        return c.json({
            errors: [errors.map(e => e.message)]
        }, code);
    }

    return c.json({ errors: [error.message]}, code);
}

export function createSlotSuccessResponse(c: Context, blockedSlot: BlockedSlotType) {
    return c.json({
        message: "Slot created successfully",
        data: blockedSlot
    }, 201);
}