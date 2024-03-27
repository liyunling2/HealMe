FROM oven/bun:latest

WORKDIR /app
COPY package.json .
COPY package-lock.json .
COPY bun.lockb .
# COPY src src
# COPY *.env .

RUN bun install
CMD ["bun", "run", "dev"]