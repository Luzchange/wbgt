import json
import math
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler
from urllib.request import Request, urlopen
from urllib.parse import urlencode
from importlib.metadata import version

LAT, LON = 11.5168, 43.0614
UNITS = {'temperature_2m': '°C', 'relative_humidity_2m': '%', 'surface_pressure': 'hPa', 'wind_speed_10m': 'm/s', 'shortwave_radiation_instant': 'W/m²', 'direct_radiation_instant': 'W/m²'}

def calculate(payload, now):
    import numpy as np
    import pandas as pd
    import pvlib
    import thermofeel
    h, units = payload['hourly'], payload['hourly_units']
    times = h['time']
    if units.get('time') != 'unixtime' or any(units.get(k) != v for k, v in UNITS.items()):
        raise ValueError('Unexpected provider units')
    if not isinstance(times, list) or not times or any(isinstance(t, bool) or not isinstance(t, (int, float)) or not math.isfinite(t) for t in times):
        raise ValueError('Invalid provider timestamps')
    if any(len(h[k]) != len(times) for k in UNITS):
        raise ValueError('Unaligned provider series')
    eligible = [i for i, t in enumerate(times) if 0 <= now - t <= 5400]
    if not eligible:
        raise ValueError('No recent nonfuture hourly model record')
    i = max(eligible, key=lambda n: times[n])
    x = {}
    for k in UNITS:
        v = h[k][i]
        if isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v):
            raise ValueError('Missing or invalid model input: ' + k)
        x[k] = v
    t, rh, pressure, wind, ghi, direct = [x[k] for k in UNITS]
    if not (-90 <= t <= 65 and 0 < rh <= 100 and 100 < pressure < 1100 and 0 <= wind <= 150 and ghi >= 0 and 0 <= direct <= ghi):
        raise ValueError('Inputs outside prototype validity guards')
    stamp = pd.DatetimeIndex([pd.Timestamp(times[i], unit='s', tz='UTC')])
    pos = pvlib.solarposition.get_solarposition(stamp, LAT, LON, pressure=pressure*100, temperature=t, method='nrel_numpy')
    cosz = float(np.cos(np.deg2rad(pos['zenith'].iloc[0])))
    fraction = direct/ghi if ghi > 0 else 0.0
    result = thermofeel.calculate_wbgt_liljegren(np.array([t+273.15]), np.array([rh]), np.array([pressure]), np.array([wind]), np.array([ghi]), np.array([fraction]), np.array([cosz]), wind_scaling='liljegren')
    c = float(np.asarray(result).reshape(-1)[0])-273.15
    if not math.isfinite(c):
        raise ValueError('WBGT solver did not converge')
    return {'kind': 'modeled_wbgt_planning_only', 'wbgt_c': round(c, 2), 'wbgt_f': round(c*9/5+32, 2), 'valid_time_utc': datetime.fromtimestamp(times[i], timezone.utc).isoformat(), 'retrieved_at_utc': datetime.fromtimestamp(now, timezone.utc).isoformat(), 'age_seconds': now-times[i], 'requested_location': {'latitude': LAT, 'longitude': LON, 'label': 'Public Chabelley Airfield regional reference; not locally verified'}, 'returned_grid': {'latitude': payload.get('latitude'), 'longitude': payload.get('longitude')}, 'inputs': x, 'input_units': UNITS, 'derived': {'direct_fraction': fraction, 'cos_solar_zenith': cosz}, 'provider': 'Open-Meteo best_match hourly model output', 'algorithm': 'thermofeel Liljegren with KNMI guards and wind_scaling=liljegren', 'versions': {'thermofeel': version('thermofeel'), 'pvlib': version('pvlib')}, 'approval': 'Not approved for operational decisions', 'published_flag': None}

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            params = urlencode({'latitude': LAT, 'longitude': LON, 'hourly': ','.join(UNITS), 'wind_speed_unit': 'ms', 'temperature_unit': 'celsius', 'timezone': 'UTC', 'timeformat': 'unixtime', 'past_hours': 2, 'forecast_hours': 2})
            req = Request('https://api.open-meteo.com/v1/forecast?'+params, headers={'User-Agent': 'Chabelley-WBGT-Planning-Prototype/1.0'})
            with urlopen(req, timeout=12) as response:
                raw = response.read(1000001)
            if len(raw) > 1000000:
                raise ValueError('Provider response too large')
            result = calculate(json.loads(raw), datetime.now(timezone.utc).timestamp())
            status = 200
        except Exception:
            status = 503
            result = {'kind': 'unavailable', 'error': 'Weather inputs or model unavailable. No WBGT or flag inferred.', 'wbgt_c': None, 'wbgt_f': None}
        encoded = json.dumps(result, allow_nan=False).encode()
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Cache-Control', 'no-store')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.end_headers()
        self.wfile.write(encoded)
