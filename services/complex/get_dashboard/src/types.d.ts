// single entity instance
// primitive

// list of instances

// Query resolved into an entity tree

interface Query {
    resolve(): Promise<object>;
}

type Expectation = {
    [key: string]: Query | Expectation
} | Function;