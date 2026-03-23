# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

Conference presentation repo for **"Orchestrate Agentic AI: Context, Checklists, and No-Miss Reviews"** — a 30-minute talk by Calvin Hendryx-Parker for AllThings AI 2026. The talk covers context engineering, agentic workflows, and a live contract-review demo using coding agents.

Deployed deck: https://sixfeetup.github.io/2026_AllThingsAI_OrchestrateAgenticAI/

## Demo

The `demo/` directory contains the live demo plan and assets:
- `demo/outline.md` — demo script and flow
- `demo/assets/` — D&D Archive PDFs (OGL source material), sample contracts, prebaked outputs
- The demo scenario involves "Safe House Games" needing IP overlap analysis using coding agents

## CI/CD

GitHub Actions deploys to GitHub Pages on push to `main`.

## Hooks

- `UserPromptSubmit` hook on "end session" triggers the `/end-session` skill
