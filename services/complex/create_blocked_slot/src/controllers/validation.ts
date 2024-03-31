import { validate } from 'jsonschema'
import SlotInvalidError from '../common/SlotInvalidError';

const blockedSlotSchema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "doctorID": {
            "type": "string",
            // "format": "uuid"
        },
        "clinicID": {
            "type": "string",
            // "format": "uuid"
        },
        "date": {
            "type": "string",
            "format": "date"
        },
        "email": {
            "type": "string",
            // "format": "string"
        },
        "slotNo": {
            "type": "integer",
            "minimum": 1,
            "maximum": 24,
        },
        "reason": {
            "type": "string",
            "maxLength": 255
        }
    },
    "required": ["doctorID", "clinicID", "date", "slotNo", "reason"],
    "additionalProperties": false
}

export function validateBlockedSlotSchema(blockedSlot: BlockedSlotType): boolean {
    // validate schema, throw Error if present, else return ValidatorResult.success
    const result = validate(blockedSlot, blockedSlotSchema);
    
    if (result.errors.length > 0) {
        // converts error array to string
        const errorString: string = result.errors.join(", ");
        throw new SlotInvalidError(errorString);
    }

    return result.valid;
}


// export function formatValidationErrors(errors: ValidationError[]): String[] {
//     return errors.map((error) => error.stack);
// }