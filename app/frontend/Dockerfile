FROM node:24-alpine

ENV PNPM_HOME="/pnpm"
ENV PATH="$PNPM_HOME:$PATH"
RUN corepack enable

# Install git and other build tools
RUN apk add --no-cache git

WORKDIR /ClassEase-Pitch

COPY package*.json /ClassEase-Pitch/

RUN pnpm install

COPY ./ /ClassEase-Pitch/

CMD ["pnpm", "run", "dev"]
