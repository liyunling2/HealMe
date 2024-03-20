const ENTITY_PATHS = {
    doctor: process.env.PROFILE_URL ?? "http://localhost:5003" + "/doctors",
    blockedSlots: process.env.BLOCKED_SLOTS_URL ?? "http://localhost:5001",
    bookings: process.env.BOOKING_URL ?? "http://localhost:5005" + "/bookings"
}

export default ENTITY_PATHS;