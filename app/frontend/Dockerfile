# Use an official Node.js runtime as the base
FROM node:18-alpine AS build

# Set the working directory
WORKDIR /frontend

# Copy package.json and package-lock.json
COPY frontend/package*.json ./

# Install dependencies (this will be cached unless package.json changes)
RUN npm ci --frozen-lockfile

# Copy the rest of the frontend source code
COPY frontend/ .

# Build the React app
RUN npm run build

# Expose port 5173
EXPOSE 5173

# # Serve the built files with Nginx
# FROM nginx:alpine
# # Copy built files
# COPY --from=build /frontend/dist /usr/share/nginx/html
# # Open port 80 for HTTP traffic
# EXPOSE 80

# Start Nginx server
CMD ["npm", "run", "dev"]
