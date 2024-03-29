type BlockedSlotType = {
    id?: string;
    doctorID: string;
    clinicID: string;
    date: string;
    slotNo: number;
    reason: string;
}

// any number of function args
type FetcherFn = (params: URLSearchParams) => Promise<Object>

type CheckRulePassedFn = (data: Object, params: URLSearchParams) => boolean;