/**
 * GeoSentinel Real-Time Telemetry Engine
 * Drives the live Zulu clock, orbital synchronization pass countdown,
 * dynamic EPS (Events Per Second) fluctuations, and HUD status indicators.
 */

export class TelemetryEngine {
  constructor() {
    this.ingestBaseEps = 2410;
    this.countdownSeconds = 45;
    this.listeners = [];
  }

  start() {
    this.updateClock();
    setInterval(() => this.updateClock(), 1000);
    setInterval(() => this.updateTelemetryRibbon(), 1500);
  }

  updateClock() {
    const now = new Date();
    const utcHours = String(now.getUTCHours()).padStart(2, '0');
    const utcMinutes = String(now.getUTCMinutes()).padStart(2, '0');
    const utcSeconds = String(now.getUTCSeconds()).padStart(2, '0');
    const zuluString = `T-${utcHours}:${utcMinutes}:${utcSeconds} ZULU`;

    const clockEls = document.querySelectorAll('.zulu-clock');
    clockEls.forEach(el => el.textContent = zuluString);

    // Pass countdown
    this.countdownSeconds -= 1;
    if (this.countdownSeconds <= 0) {
      this.countdownSeconds = 60;
    }
    const countdownEls = document.querySelectorAll('.pass-countdown');
    countdownEls.forEach(el => el.textContent = `T-${String(this.countdownSeconds).padStart(2, '0')}s`);
  }

  updateTelemetryRibbon() {
    // Realistic micro-fluctuations in ingestion rate
    const jitter = Math.floor(Math.random() * 41) - 20;
    const currentEps = (this.ingestBaseEps + jitter) / 1000;
    const epsEls = document.querySelectorAll('.ingest-eps');
    epsEls.forEach(el => el.textContent = `${currentEps.toFixed(2)}k EPS`);

    // Latency fluctuation (22 - 28ms)
    const latency = 22 + Math.floor(Math.random() * 7);
    const latencyEls = document.querySelectorAll('.telemetry-latency');
    latencyEls.forEach(el => el.textContent = `${latency}ms`);
  }
}
