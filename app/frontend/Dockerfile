# --- Stage 1: Builder ---
FROM node:18-alpine AS builder

# Install git and other build tools
RUN apk add --no-cache git

# Set working directory
WORKDIR /app

# Copy only the necessary files for dependency resolution
COPY package.json pnpm-lock.yaml ./

# Install pnpm globally
RUN npm install -g pnpm

# Install dependencies
RUN pnpm install

# Copy the rest of the frontend source code
COPY . ./

# Build the app
RUN pnpm run build

# --- Stage 2: Runtime ---
FROM node:18-alpine

# Set working directory
WORKDIR /ClassEase-Pitch/app/frontend

# Install pnpm globally again (for runtime usage like `pnpm run dev`)
RUN npm install -g pnpm

# Copy only the built output from the builder
COPY --from=builder /app/ ./

# Expose Vite default port
EXPOSE 5173

# Start development server
CMD ["pnpm", "run", "dev"]
