export default function isResponseJson(response: Response): boolean {
    const contentType = response.headers.get("Content-Type");
    return contentType?.includes("application/json") ?? false;
}