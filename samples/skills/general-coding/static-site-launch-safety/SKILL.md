---
name: static-site-launch-safety
description: Prepare, preview, deploy, or troubleshoot a static website launch with guarded handling for DNS, hosting, analytics, forms, secrets, and public publication. Use when a task moves a site from local files to a public or shared URL.
---

# Static Site Launch Safety

Use this skill when a static site task includes previewing, building, publishing,
DNS changes, hosting configuration, analytics, form handling, or launch checks.
Treat public publication and account-level changes as guarded writes.

## Workflow

1. Classify the task.
   - Local content edits, formatting, and local preview are usually low risk.
   - DNS, hosting, billing, public deployment, redirects, analytics, form
     endpoints, email capture, authentication, and secret management are guarded
     or high-risk writes.
   - Require explicit target selection before changing a public site or account.

2. Inspect the project.
   - Identify the framework or generator, build command, output directory,
     package manager, hosting provider, and deployment config.
   - Read existing launch docs, environment examples, redirects, headers, and
     protected/generated folder rules.
   - Check whether assets, screenshots, testimonials, logos, contact details, or
     legal text are approved for public use.

3. Validate locally first.
   - Run install, build, typecheck, lint, or link-check commands documented by the
     project.
   - Preview the built output, not only the development server, when possible.
   - Verify responsive layout, navigation, metadata, image paths, forms, error
     pages, and cache-sensitive assets.

4. Guard public writes.
   - Show the exact deploy target, domain, branch, and command before publishing.
   - Do not create or rotate tokens, alter DNS, enable billing features, or expose
     private preview URLs without explicit approval.
   - Keep rollback notes: previous deployment, branch, tag, provider rollback
     action, or DNS record values when available.

5. Verify after launch.
   - Check the public URL, canonical URL, redirects, cache behavior, metadata,
     robots settings, analytics opt-in behavior, form delivery, and error pages.
   - Avoid submitting real personal data through forms during tests; use synthetic
     test values.

## Reporting

State the launch target, build command, validation run, public-write approvals,
rollback notes, and any checks that were skipped because credentials or provider
access were unavailable.