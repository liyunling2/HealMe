import ENTITY_PATHS from "./entityPaths";
import FetchingError from "../common/FetchingError";

async function fetchData(path: string, params: URLSearchParams | null = null, entityName: string = "data"): Promise<Object> {
    // return json data
    let data;
    try {
        // throws error if url invalid
        const url = new URL(path + (params ? "?" + params.toString(): ""));

        console.log(`Fetching ${entityName} at ${url}`)
        const response = await fetch(url);
        // throws error if response not valid JSON
        data = await response.json();

        console.log("Fetched " + entityName + " " + response.status, data);

        if (!response.ok)
            throw new FetchingError(`Request to ${url.toString()} failed with ${response.status}: ${response.statusText}`);
        
    }
    catch (e) {
        console.error(e);
        throw e;
    }

    return data;
}

export async function fetchDoctorWithParams(params: URLSearchParams): Promise<Object> {
    const doctorID = params.get("doctorID");
    return fetchData(ENTITY_PATHS.doctor + `/doctors/${doctorID}`, null, "doctor");
}

export async function fetchBlockedSlotsWithParams(params: URLSearchParams): Promise<Object> {
    return fetchData(ENTITY_PATHS.blockedSlots, params, "blocked slots");
}

export async function fetchBookingsWithParams(params: URLSearchParams): Promise<Object> {
    return fetchData(ENTITY_PATHS.bookings, params, "bookings");
}