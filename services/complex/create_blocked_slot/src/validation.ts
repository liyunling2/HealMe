import { ValidatorResult, validate } from 'jsonschema'
import { ValidationError } from "jsonschema";

const blockedSlotSchema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "doctorID": {
            "type": "string",
            "format": "uuid"
        },
        "clinicID": {
            "type": "string",
            "format": "uuid"
        },
        "date": {
            "type": "string",
            "format": "date"
        },
        "slotNo": {
            "type": "integer"
        },
        "reason": {
            "type": "string",
            "maxLength": 255
        }
    },
    "required": ["doctorID", "clinicID", "date", "slotNo", "reason"],
    "additionalProperties": false
}

export function validateBlockedSlotSchema(blockedSlot: BlockedSlotType): ValidatorResult {
    return validate(blockedSlot, blockedSlotSchema);
}

export function formatValidationErrors(errors: ValidationError[]): String[] {
    return errors.map((error) => error.stack);
}