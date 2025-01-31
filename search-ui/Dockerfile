# Stage 1: Build the React application
FROM docker.io/node:16-alpine AS build

# Set working directory
WORKDIR /app

# Copy package.json
COPY package.json ./

# Install dependencies
RUN npm install --legacy-peer-deps

# Copy the rest of the application code
COPY . ./

# Build the application
RUN npm run build

# Stage 2: Serve the React application with Nginx
FROM docker.io/nginx:1.26.2-alpine

# Remove the default Nginx static assets
RUN rm -rf /usr/share/nginx/html/*

# Copy the build output to replace the default Nginx static assets
COPY --from=build /app/build /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]