# Designing Pastebin

## What is Pastebin ?

Pastebin is a web application where users can store and share text content online. Users can paste text (code snippets, logs, configuration files, etc.), get a unique URL to share it, and set expiration times. The service is commonly used by developers to share code, debug logs, or collaborate on text-based content.

## Requirements and Goals

### Functional Requirements

* Users should be able to paste text and get a unique URL
* Users can access pastes via the unique URL
* Users can set expiration time for pastes (1 hour, 1 day, 1 week, 1 month, never)
* Users can set privacy levels (public, unlisted, private)
* Users can optionally set a custom alias for their paste
* Support for syntax highlighting for different programming languages
* User can view raw text version of pastes

### Non-Functional Requirements

* The system should be highly available (99.99%) uptime
* Low latency for paste retrieval ( < 100 ms)
* The system should be scalable to handle millions of pastes
* Data should be durable - pastes shouldn’t be lost before expiration
* The system should handle pastes up to 10 MB in size

### Extended Requirements

* Analytics on paste views
* User account and Paste Management
* Paste Editing Capabilities
* API Access for programmatic usage

## Capacity Estimation and Constraints

## System Interface Definition

## Database Schema

## High-Level System Design

## Detailed Component Design

## Data Partition and Replication

## Expiration and Cleanup

## Security and Ratelimiting

## Monitoring and Analytics