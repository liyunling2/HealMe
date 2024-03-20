export default class Rule {
    // fetches the data according to params
    fetcherFn: FetcherFn

    // checks whether rule passed based on return json
    checkRulePassedFn: CheckRulePassedFn
    failedMessage: string
    
    constructor(fetcherFn: FetcherFn, checkRulePassedFn: CheckRulePassedFn, failedMessage: string = "Rule check failed") {
        this.fetcherFn = fetcherFn;
        this.checkRulePassedFn = checkRulePassedFn;
        this.failedMessage = failedMessage;
    }

    async check(params: URLSearchParams): Promise<boolean> {
        return this.checkRulePassedFn(await this.fetcherFn(params), params);
    }
}