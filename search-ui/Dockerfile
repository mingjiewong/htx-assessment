# Stage 1: Build the React application
FROM node:16-alpine AS build

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

# Stage 2: Serve the React application with `serve`
FROM node:16-alpine

# Install `serve` globally
RUN npm install -g serve

# Set working directory
WORKDIR /app

# Copy the build output from the previous stage
COPY --from=build /app/build ./build

# Expose port 5000 (default port for `serve`)
EXPOSE 80

# Start the application using `serve`
CMD ["serve", "-s", "build", "-l", "80"]