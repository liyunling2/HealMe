import { RabbitMQConnection } from "./amqp";


export async function log(obj: { data: any, message: any, status: number }, mqConnection: RabbitMQConnection) {
    console.log("Creating log")
    const message = getLogMessageObj(obj);
    await mqConnection.connect();
    const channel = await mqConnection.channel;

    await channel.basicPublish(
        "log_fanout",
        "#",
        Buffer.from(JSON.stringify(message))
    )
}

function getLogMessageObj(body: { data: any, message: any, status: number }): LogMessage {
    const message = body.message || "";
    const details = body.data || {};
    const level = getLogLevel(body.status);

    return {
        message,
        source: "createBlockedSlot complex service",
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
    if (code >= 400) return "WARN";
    return "INFO";
}