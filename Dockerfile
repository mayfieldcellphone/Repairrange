# Stage 1: Install dependencies
FROM node:20-slim AS deps
WORKDIR /app
# Note: Copying from the subfolder
COPY repairhub-saas/package.json repairhub-saas/package-lock.json* ./
RUN npm install

# Stage 2: Build the app
FROM node:20-slim AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY repairhub-saas/ .
ENV NEXT_TELEMETRY_DISABLED 1
RUN npm run build

# Stage 3: Production runner
FROM node:20-slim AS runner
WORKDIR /app

ENV NODE_ENV production
ENV NEXT_TELEMETRY_DISABLED 1

# Copy standalone build from the correct path
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static
COPY --from=builder /app/public ./public

# Finalizing Environment
EXPOSE 3000
ENV PORT 3000
ENV HOSTNAME "0.0.0.0"

# Start the server
CMD ["node", "server.js"]
