export default class SlotNotAllowedError extends Error {
    constructor(message: string) {
        super(message);
        this.name = "SlotNotAllowedError";
    }
}