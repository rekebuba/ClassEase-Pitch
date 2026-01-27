FROM node:24-alpine

RUN corepack enable pnpm

# Install git and other build tools
RUN apk add --no-cache git

WORKDIR /frontend

COPY package*.json .

RUN pnpm install

COPY . .

CMD ["pnpm", "run", "dev"]
