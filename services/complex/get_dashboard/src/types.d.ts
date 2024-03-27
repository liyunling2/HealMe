type Expectation = {
    [key: string]: Expectation | import('./common/Query').Query,
} | Function;

type Context = {
    [key: string]: any
}