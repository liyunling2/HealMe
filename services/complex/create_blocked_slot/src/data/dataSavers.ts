import FetchingError from "../common/FetchingError";
import { isResponseJson } from "./dataUtils";
import ENTITY_PATHS from "./entityPaths";

async function saveData(path: string, body: Object, entityName:string = "data"): Promise<Object> {
    const url = new URL(path);
    const response = await fetch(url, {
        method: "POST",
        body: JSON.stringify(body),
        headers: {
            "Content-Type": "application/json"
        }
    })

    if (!response.ok) {
        if (isResponseJson(response)) {
            const error = await response.json();
            throw new FetchingError(error.message);
        }
        throw new FetchingError("Error saving " + entityName);
    }

    return await response.json();
}

export async function saveBlockedSlot(blockedSlot: BlockedSlotType) {
    return saveData(ENTITY_PATHS.blockedSlots, blockedSlot, "blocked slot");
}
