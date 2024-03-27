export class Query {
    constructor(private expectation: Expectation, private context: Context = {}) {
    }

    join(query: Query): Query {
        // Joining the expectation (object) as well as the context object containing query params
        // Base object with empty expectation
        const joined = new Query(
        {},
        {
            ...this.context,
            ...query.context
        })


        joined.resolve = async (additionalContext: Context) => ({
            ...await this.resolve(additionalContext),
            ...await query.resolve(additionalContext)
        });

        return joined;
    }

    // top-level resolution. A resolved query is a reified Query with real data
    async resolve(additionalContext: Context | null = null): Promise<object> {
        // if expectation is function, call
        if (additionalContext)
            this.context = {...this.context, ...additionalContext};

        // Base case
        if (typeof this.expectation === "function") {
            return await this.expectation(this.context);
        }
        // if expectation is object, walk
        return await this.walk(this.expectation);
    }

    // if expectation is an object
    async walk(expectation: Expectation): Promise<object> {
        const entries = Object.entries(expectation);
        const resolvedEntries: { [key: string]: any } = {};
        // walk through each key
        for (let [key, value] of entries) {
            if (value instanceof Query) {
                // provide context down to child queries
                value.context = this.context;
                resolvedEntries[key] = await value.resolve();
            }
        }

        return resolvedEntries;
    }
}

export default Query;