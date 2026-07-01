---
name: provider-capability-mapping
description: Map model, API, or service capabilities by provider and endpoint before sending requests. Use when code supports multiple providers, OpenAI-compatible endpoints, hosted and local backends, or provider-specific request fields.
---

# Provider Capability Mapping

Use this skill when one UI or service routes requests to multiple providers or
OpenAI-compatible endpoints. The goal is to send only fields the selected
provider and endpoint actually support.

## Workflow

1. Identify the exact surface.
   - Determine provider, endpoint family, API version, model identifier, and
     transport path.
   - Distinguish native endpoints from compatibility endpoints even when they use
     similar request shapes.
   - Locate existing provider adapters, schemas, feature flags, and tests.

2. Build or update a capability map.
   - Record supported request fields, response fields, streaming behavior, tool
     calling support, JSON or structured-output support, image/audio support,
     sampling options, context limits, authentication requirements, and known
     omissions.
   - Prefer explicit allowlists over passing through arbitrary UI state.
   - Keep defaults separate from user preferences when a provider rejects or
     ignores a field.

3. Implement gated request construction.
   - Normalize shared inputs first, then translate into provider-specific
     payloads at the adapter boundary.
   - Omit unsupported fields instead of sending nulls or hoping compatibility
     layers ignore them.
   - Surface clear warnings or disabled UI controls when a selected provider does
     not support a feature.

4. Test strict and permissive paths.
   - Add tests for accepted fields, omitted fields, fallback behavior, and clear
     error messages.
   - Include at least one strict or minimal endpoint fixture when available.
   - Test that a field accepted by one provider is not sent to another provider
     unless the map explicitly allows it.

5. Document behavior.
   - Update command guides, provider docs, or UI help where the project normally
     explains supported backends.
   - List known unsupported features and how the app degrades.

## Guardrails

- Do not treat an OpenAI-compatible route as identical to OpenAI's current API.
- Do not leak secrets, local endpoint URLs, account IDs, or private model names in
  public examples.
- Do not silently change model choice or provider without telling the user.
- Do not overclaim capability coverage beyond what was verified.

## Reporting

State the providers and endpoints checked, the capability map changes, request
fields gated or omitted, tests run, and any provider behavior that still needs
manual verification.