# -----------------------
# Build stage
# -----------------------
FROM node:24-alpine AS builder

RUN corepack enable pnpm

# Install git and other build tools
RUN apk add --no-cache git

WORKDIR /app

COPY package*.json .

RUN pnpm install

COPY . .

ARG VITE_API_BASE_URL
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL

RUN pnpm build

# -----------------------
# Runtime stage
# -----------------------
FROM nginx:stable-alpine3.23-slim

RUN apk add --no-cache curl

# Remove default nginx config
RUN rm /etc/nginx/conf.d/default.conf

# Custom nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy built assets
COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 8080

CMD ["nginx", "-g", "daemon off;"]
