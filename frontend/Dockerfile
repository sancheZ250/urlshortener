# Frontend Dockerfile
FROM node:18-alpine

WORKDIR /app

# Copy the package.json and package-lock.json files first to leverage Docker cache
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY . /app/

# Expose the port for Vite
EXPOSE 5173

# Start the Vite development server
CMD ["npm", "run", "dev"]
