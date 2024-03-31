import { Context } from "hono";
import { RabbitMQConnection } from "./amqp";

export function loggingHandlerFactory(mqConnection: RabbitMQConnection) {
    return async function loggingHandler(c: Context, next: Function){
        console.log("Running logging handler")
        await next();
        log(c.res, mqConnection);
    }
}

async function log(res: Response, mqConnection: RabbitMQConnection) {
    
    const message = getLogMessageObj(await res.json(), res.status);
    await mqConnection.connect();
    const channel = await mqConnection.channel;

    await channel.basicPublish(
        "log_fanout",
        "#",
        Buffer.from(JSON.stringify(message))
    )
}

function getLogMessageObj(body: { data: any, message: any}, code: number): LogMessage {
    const message = body.message || "";
    const details = body.data || {};
    const level = getLogLevel(code);

    return {
        message,
        source: "manageBooking complex service",
        timestamp: new Date().toISOString(),
        details,
        level
    };
}

interface LogMessage {
    message: string;
    source: string;
    timestamp: string;
    details: any;
    level: string;
}

function getLogLevel(code: number): string {
    if (code >= 500) return "ERROR";
    if (code >= 400) return "WARN";
    return "INFO";
}