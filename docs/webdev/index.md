# Web Frameworks Overview

Quick reference for backend web frameworks by language — strengths, weaknesses, and docs.

---

## Python

| Framework | Strengths | Weaknesses | Docs |
|-----------|-----------|------------|------|
| **FastAPI** | Auto OpenAPI docs, type hints via Pydantic, async-first, fast to build | Relatively young ecosystem, can get complex with large apps | [fastapi.tiangolo.com](https://fastapi.tiangolo.com) |
| **Django** | Batteries-included (ORM, admin, auth), massive ecosystem, opinionated = consistent | Heavy for small services, ORM can be a bottleneck, steep learning curve | [docs.djangoproject.com](https://docs.djangoproject.com) |
| **Flask** | Minimal and flexible, easy to learn, huge community | No async support (without extensions), easy to build inconsistent apps | [flask.palletsprojects.com](https://flask.palletsprojects.com) |
| **Tornado** | True async I/O, good for WebSockets and long-polling, battle-tested | Verbose, smaller community vs Flask/FastAPI, async patterns can be tricky | [tornadoweb.org](https://www.tornadoweb.org) |
| **Litestar** | Modern async, batteries-included like Django but lighter, great DX | Smaller community, less adoption than FastAPI | [litestar.dev](https://litestar.dev) |

**Pick FastAPI** for new projects; Django if you need admin/auth out of the box; Flask for scripts and quick APIs.

---

## JavaScript / TypeScript

| Framework | Strengths | Weaknesses | Docs |
|-----------|-----------|------------|------|
| **Express** | Minimal, ubiquitous, huge middleware ecosystem | No opinions = inconsistency at scale, callback/middleware hell | [expressjs.com](https://expressjs.com) |
| **Fastify** | Very fast, schema-based validation, good TypeScript support | Smaller ecosystem than Express | [fastify.dev](https://fastify.dev) |
| **NestJS** | Angular-style architecture, DI, great for large teams, TypeScript-first | Heavy boilerplate, opinionated, steep learning curve | [docs.nestjs.com](https://docs.nestjs.com) |
| **Hono** | Tiny, edge-runtime compatible (Cloudflare Workers, Deno), very fast | Minimal ecosystem, not suited for monolithic apps | [hono.dev](https://hono.dev) |
| **Next.js** | Full-stack React (SSR/SSG/RSC), file-based routing, Vercel ecosystem | Complex mental model, large bundle, tight Vercel coupling | [nextjs.org/docs](https://nextjs.org/docs) |

**Pick Express/Fastify** for standalone APIs; NestJS for large enterprise services; Next.js for full-stack React apps.

---

## Java

| Framework | Strengths | Weaknesses | Docs |
|-----------|-----------|------------|------|
| **Spring Boot** | Industry standard, massive ecosystem, battle-tested, cloud-native tooling | Verbose, heavy memory footprint, slow startup | [spring.io/projects/spring-boot](https://spring.io/projects/spring-boot) |
| **Quarkus** | Fast startup, low memory (GraalVM native), reactive and imperative modes | Smaller ecosystem, steeper learning curve than Spring | [quarkus.io](https://quarkus.io) |
| **Micronaut** | Compile-time DI (fast startup), GraalVM native support, cloud-native | Smaller community, fewer integrations | [micronaut.io](https://micronaut.io) |
| **Vert.x** | High-performance async/reactive, polyglot (runs on JVM) | Reactive model is hard to reason about, not beginner-friendly | [vertx.io](https://vertx.io) |

**Pick Spring Boot** unless startup time or memory is a hard constraint, then Quarkus.

---

## Go

| Framework | Strengths | Weaknesses | Docs |
|-----------|-----------|------------|------|
| **net/http** (stdlib) | Zero deps, fast, good enough for most APIs | Routing is bare-bones, no middleware chaining built-in | [pkg.go.dev/net/http](https://pkg.go.dev/net/http) |
| **Gin** | Fast router, middleware support, good DX, most popular Go web framework | Opinionated routing style, some rough edges | [gin-gonic.com](https://gin-gonic.com) |
| **Echo** | Clean API, high performance, built-in middleware | Smaller community than Gin | [echo.labstack.com](https://echo.labstack.com) |
| **Fiber** | Express-like API, very fast (built on fasthttp), easy migration from Node | Not net/http compatible, fasthttp quirks | [gofiber.io](https://gofiber.io) |
| **Chi** | Idiomatic Go, stdlib compatible, composable middleware | No extras — just routing | [github.com/go-chi/chi](https://github.com/go-chi/chi) |

**Pick Gin or Chi** for most projects; stdlib `net/http` for minimal services.

---

## Rust

| Framework | Strengths | Weaknesses | Docs |
|-----------|-----------|------------|------|
| **Axum** | Tokio-native, type-safe extractors, ergonomic, actively maintained | Compile times, complex type errors | [docs.rs/axum](https://docs.rs/axum) |
| **Actix-web** | Fastest benchmarks, mature, feature-rich | Actor model complexity (older versions), compile times | [actix.rs](https://actix.rs) |
| **Rocket** | Ergonomic macros, good DX, type-safe routing | Slower to compile, opinionated | [rocket.rs](https://rocket.rs) |
| **Warp** | Filter-based composition, async, Tokio-native | Filter combinators can be hard to read | [docs.rs/warp](https://docs.rs/warp) |

**Pick Axum** for new Rust web projects — best balance of ergonomics and performance.
