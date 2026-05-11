FROM golang:1.26-alpine AS builder
WORKDIR /app
COPY main.go .
RUN go build -o lobstertrap main.go

FROM alpine:latest
WORKDIR /app
COPY --from=builder /app/lobstertrap .
EXPOSE 8080
ENTRYPOINT ["./lobstertrap", "serve", "--port", "8080"]
