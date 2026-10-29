# Current modeled weather integration

Open weather.html alongside index.html. Existing dashboard, app.js, synthetic logs, simulator, and policy brief remain unchanged. This separate page intentionally prevents weather-model data from being confused with onsite WBGT readings.

Enter user-verified latitude/longitude and authorize the external request. No installation coordinates are preconfigured. Coordinate requests go directly from the browser to api.open-meteo.com; provider sees network metadata and coordinates. Do not use restricted sensor locations. Coordinates/data are not persisted by this adapter.

Displays provider current temperature_2m (°C), relative_humidity_2m (%), wind_speed_10m (m/s), cloud_cover (%), valid time, retrieval time, requested location, and returned grid location. Uses /v1/forecast current parameters, UTC Unix timestamps, and best-match defaults. These are modeled current conditions, not an onsite real-time sensor feed or measured WBGT.

Visible-tab refresh target: 15 minutes. Per-tab minimum request interval: one minute. Request timeout: 15 seconds. No guaranteed background logging. Prototype age warning: 60 minutes, not a military freshness policy. Missing fields remain unavailable; failed requests clear values. Stop clears values and disables scheduled requests until another explicit location selection.

No WBGT calculation, flag publication, alert, durable record, provider failover, authentication, or server quota enforcement is added. No operational decisions may rely on this prototype. Review provider licensing, rate limits, privacy, and organizational authorization before deployment. Attribution links are included.

Validation performed: API field/unit design checked against Open-Meteo documentation. Not performed: live endpoint response test for Camp Chabelley (no verified coordinates supplied), automated JavaScript/browser tests, CORS verification, deployment verification, or approval of provider suitability. Do not claim those tests passed.

Vercel remains owner-managed. Existing feature branch is not merged into main by this change. If Git auto-deployment is already configured externally, this branch push may trigger that configuration; no Vercel API changes are requested.
