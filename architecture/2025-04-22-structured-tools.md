# ADR 2025-04-22-structured-tools.md

## Title
Use LangChain Structured Tools with Pydantic for Agent Tool Contracts

## Status
Accepted

## Context
The default LangChain Tool interface is flexible but unreliable for argument parsing, leading to boilerplate and runtime errors. We want robust, declarative, and type-safe tool APIs for our LLM agent.

## Decision
We will use LangChain Structured Tools with Pydantic models for all agent-facing tools. This provides:

- Formal, type-checked argument schemas
- Automatic parsing and validation of user/agent input
- Elimination of manual argument-massaging code
- Clearer error messages and self-documenting APIs

## Consequences
- Tool APIs are now explicit and robust
- Agents and users get better error feedback
- Code is easier to maintain and extend
- Slight increase in dependency footprint (Pydantic)

---
