import Rule from "./Rule";
import SlotNotAllowedError from "./SlotNotAllowedError";

export default class AllowedSlotsChecker {
    // 
    rules: Rule[];
    params: URLSearchParams;

    constructor(rules: Rule[], params: URLSearchParams) {
        this.rules = rules;
        this.params = params;
    }

    // run all rules, coalesce failed rule errors, throw request errors
    async run(): Promise<boolean> {
        // if fetcherFn fails, error thrown
        for (const rule of this.rules) {
            const isRulePassed: boolean = await rule.check(this.params);

            if (!isRulePassed)
                throw new SlotNotAllowedError(rule.failedMessage);
        }

        return true
    }
    
}