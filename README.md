# Camp Chabelley WBGT — Perplexity prototype

DEMONSTRATION ONLY. Not approved for operational decisions. Use synthetic data only.

## Run
Open index.html in a modern browser, or serve the repository root with `python -m http.server 8000`. No build step or dependencies.

## Implemented
Responsive dashboard, manual synthetic drafts, Celsius/Fahrenheit conversion, EAT observation entry, browser-local persistence when available, JSON export, manually advanced red/black incident simulation, separate reviewer/safety acknowledgments, and proposed 5/10-minute red escalation with 30-minute reminders after simulated publication. Black-specific deadlines are unconfigured.

Local drafts and simulation events are mutable and are not approved records or protected audit logs. Simulation state resets on reload. No messages are sent.

## Not implemented
Authentication, server authorization, PostgreSQL, correction lineage, protected audit, real publication, approved policy rules, durable workers, notification providers, validated models, forecasts, stale-data workflow, downgrade workflow, and delivery fallback.

## Testing
Automated browser execution, JavaScript tests, accessibility verification, and deployment have not been performed for this commit. Do not claim operational readiness.

## GitHub and Vercel
This feature branch preserves main for review. The owner connects Vercel manually. For this static version serve the root with no build command. No Vercel changes are authorized by this commit. A private repository does not establish private hosting. Never enter operational or sensitive data.

## Implementation direction
Continue development in Perplexity using PERPLEXITY_PROMPT.md and the complete master specification previously supplied to the owner. This short brief does not replace that full specification.
