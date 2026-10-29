# Automated modeled WBGT — planning prototype

New page: modeled-wbgt.html. Endpoint: GET /api/wbgt. Requires Python hosting and requirements.txt installation; plain static file hosting cannot run this endpoint. Existing pages remain unchanged. Vercel Python runtime/build and dependency installation must be verified by the owner; no deployment is performed by this commit. Do not overwrite existing Vercel configuration without inspecting it.

Public regional reference: 11.5168, 43.0614, from https://www.pilotnav.com/airport/HDCH. This is not a verified installation sensor location or local approval. Public sources differ slightly. No restricted coordinates are required.

Inputs: Open-Meteo best_match hourly temperature, RH, surface pressure (not sea-level pressure), wind at 10 m, shortwave_radiation_instant, direct_radiation_instant. All values come from the same latest nonfuture hourly record no more than 90 minutes old. The 90-minute guard is a prototype limit, not a military policy. Missing required inputs or nonconvergence yields HTTP 503 and null WBGT. No fabricated UV/radiation or wet-bulb shortcuts.

ECMWF thermofeel 2.3.0 calculate_wbgt_liljegren returns Kelvin; convert to Celsius after calculation. Pressure is hPa; wind m/s; radiation W/m². Direct beam fraction is horizontal direct/global radiation. Solar zenith uses pvlib 0.13.1 nrel_numpy at the valid time and public requested coordinates. Thermofeel applies its documented KNMI wind floor, height adjustment, direct-fraction guards and iterative solver. These differ from merely copying an approved military reference implementation; no equivalence or military authorization is claimed.

Sources: https://open-meteo.com/en/docs ; https://thermofeel.readthedocs.io/en/stable/guide/heatforce/ ; https://pypi.org/project/thermofeel/ . Provider data license and public endpoint terms are distinct; review suitability for organizational use before operation.

Automated here means the endpoint fetches actual provider model inputs and calculates WBGT without manual temperature entry; the page requests a refresh every 15 minutes while visible. It is not a durable unattended collector. No database, background cron, authenticated operations, server quota enforcement, published flags, or real alerting is added. Inputs/provenance are returned, not durably archived.

Tests NOT performed: package installation, solver execution, reference-case comparison, local sensor validation, live endpoint request, automated browser tests, deployment/build verification, load testing, security review. This commit is an implementation candidate requiring those tests. Requirements pin direct dependencies only; transitive dependency lock remains outstanding. Do not claim operational readiness. Main, deployment settings, and notifications remain unchanged. Externally configured Git previews may respond to the branch push.
