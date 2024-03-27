export default class Query {
    constructor(private expectation: Expectation) {
    }

    join(query: Query): Query {
        const joined =  new Query({
            ...this.expectation,
            ...query.expectation
        });
        console.log("JOINED expectation", joined.expectation);
        return joined;
    }

    async resolve(): Promise<object> {
        // if expectation is function, call
        if (typeof this.expectation === "function") {
            return await this.expectation();
        }
        // if expectation is object, walk
        return await this.walk(this.expectation);
    }

    async walk(expectation: Expectation): Promise<object> {
        const entries = Object.entries(expectation);
        const resolvedEntries: { [key: string]: any } = {};
        // walk through each key
        for (let [key, value] of entries) {
            if (value instanceof Query) {
                resolvedEntries[key] = await value.resolve();
            }
        }

        return resolvedEntries;
    }
}

const specialtyQuery = new Query(() => ["heart", "brain"])

const doctorQuery = new Query({
    specialty: specialtyQuery,
    name: new Query(() => "Sean"),
})
const dateQuery = new Query(async () => new Date())

const query = new Query({
    doctor: doctorQuery,
    date: dateQuery,
})

console.log(
    await query.join(
        new Query(
            {time: 
                new Query(async () => new Date())
            }
        )
    ).resolve());
