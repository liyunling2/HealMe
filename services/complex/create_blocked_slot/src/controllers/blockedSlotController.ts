import { fetchBlockedSlotsWithParams, fetchBookingsWithParams, fetchDoctorWithParams } from "../data/dataFetchers";
import { validateBlockedSlotSchema } from "./validation";
import { saveBlockedSlot } from "../data/dataSavers";
import Rule from "../common/Rule";
import AllowedSlotsChecker from "../common/AllowedSlotsChecker";

export default async function createBlockedSlot(blockedSlot: BlockedSlotType) {
    const isValidBlockedSlot = checkValidBlockedSlot(blockedSlot);
    const isBlockedSlotAllowed = await checkAllowedBlockedSlot(blockedSlot);
    
    if (isValidBlockedSlot && isBlockedSlotAllowed)
        return await saveBlockedSlot(blockedSlot);
}

async function checkAllowedBlockedSlot(blockedSlot: BlockedSlotType): Promise<boolean> {
    // throws error if fail

    const params = new URLSearchParams({
        doctorID: blockedSlot.doctorID,
        date: blockedSlot.date,
        slotNo: blockedSlot.slotNo.toString()
    });

    const checker = new AllowedSlotsChecker(rules, params);
    return await checker.run();
}

function checkValidBlockedSlot(blockedSlot: BlockedSlotType): boolean {
    return validateBlockedSlotSchema(blockedSlot);
}

const rules: Rule[] = [
    //@ts-ignore
    new Rule(fetchDoctorWithParams, (body) => body?.doctorID !== null, "Not a valid doctor ID"),
    //@ts-ignore
    new Rule(fetchBlockedSlotsWithParams, (body) => (body?.data as any[]).length == 0, "Blocked slot already exists"),
    //@ts-ignore
    new Rule(fetchBookingsWithParams, (body) => (body?.data as any[]).length == 0, "There is an existing booking at the time slot"),
]
