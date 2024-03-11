FROM oven/bun:latest

WORKDIR /app
COPY package.json .
COPY bun.lockb .
COPY src src
COPY *.env .

RUN bun install --production
CMD ["bun", "run", "dev"]