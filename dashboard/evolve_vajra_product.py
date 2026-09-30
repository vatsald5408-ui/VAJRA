# -*- coding: utf-8 -*-
"""
VAJRA Atmospheric Intelligence Platform - Product-Level Evolution
Strictly implementing the 22 core product enhancements:
1. Dynamic living atmospheric map (Radar sweep, lightning pulses, storm growth, trajectory evolution)
2. Atmospheric Pulse signature indicator (Stable -> Developing -> Intensifying -> Severe)
3. Storm Story visual narrative timeline (Formed -> Developing -> Intensifying -> Peak -> Projected)
4. What Changed? Last 15 Min contextual comparison
5. Impact Lens interactive mode (Roads, rail, airports, power grid intersections)
6. Threat Ribbon visual progression
7. Forecast Field with soft probabilistic diffusion
8. Observed <-> Forecast seamless transition
9. Forecast Time Machine with Play Evolution
10. Regional Weather Pulse (Eastern India overview)
11. Situation View vs Map View dual primary experience
12. Beautiful layer previews with live states
13. Data Health interactive inspection tray
14. Focus Mode for individual storm cells
15. Editorial Right Panel with generous typography and whitespace
16. Clean product terminology (NO repeated AI buzzwords)
"""

code = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>VAJRA — Atmospheric Intelligence Platform</title>
  <meta name="description" content="VAJRA: Atmospheric Intelligence Platform. Real-time nowcasting of severe convective storms and lightning across India." />

  <!-- Google Fonts: Plus Jakarta Sans & Inter -->
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet" />

  <!-- Leaflet CSS & JS -->
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin="" />
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>

  <style>
    /* ==========================================================================
       1. ATMOSPHERIC PRODUCT DESIGN SYSTEM
       ========================================================================== */
    :root {
      /* Deep Midnight Navy Atmosphere */
      --bg-space: #070b14;
      --bg-panel: rgba(13, 20, 36, 0.88);
      --bg-panel-solid: #0d1424;
      --bg-elevated: #152038;
      --bg-elevated-hover: #1c2b4a;
      --bg-input: #0a0f1d;

      /* Borders */
      --border-subtle: rgba(255, 255, 255, 0.08);
      --border-medium: rgba(255, 255, 255, 0.16);
      --border-active: #38bdf8;

      /* Typography */
      --text-white: #ffffff;
      --text-bright: #f8fafc;
      --text-primary: #e2e8f0;
      --text-secondary: #94a3b8;
      --text-muted: #64748b;

      /* Meteorological Spectrum */
      --radar-cyan: #06b6d4;
      --radar-green: #10b981;
      --radar-amber: #f59e0b;
      --radar-orange: #f97316;
      --radar-red: #ef4444;
      --radar-magenta: #d946ef;

      --pulse-live: #10b981;
      --ltg-glow: #38bdf8;
      --uncert-field: #a855f7;
      --impact-gold: #fbbf24;

      --font-display: 'Plus Jakarta Sans', system-ui, sans-serif;
      --font-body: 'Inter', system-ui, sans-serif;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      -webkit-font-smoothing: antialiased;
    }

    body {
      background: var(--bg-space);
      color: var(--text-primary);
      font-family: var(--font-body);
      font-size: 14px;
      line-height: 1.5;
      height: 100vh;
      width: 100vw;
      overflow: hidden;
      user-select: none;
    }

    /* Scrollbars */
    ::-webkit-scrollbar { width: 5px; height: 5px; }
    ::-webkit-scrollbar-track { background: var(--bg-space); }
    ::-webkit-scrollbar-thumb { background: #1e293b; border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: #334155; }

    /* ==========================================================================
       2. TOP PRODUCT HEADER (ELEGANT & PURPOSEFUL)
       ========================================================================== */
    .top-header {
      height: 62px;
      background: var(--bg-panel-solid);
      border-bottom: 1px solid var(--border-subtle);
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 22px;
      z-index: 1000;
      position: relative;
    }

    .brand-section {
      display: flex;
      align-items: center;
      gap: 16px;
    }

    .brand-emblem {
      width: 38px;
      height: 38px;
      border-radius: 9px;
      background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%);
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 4px 16px rgba(2, 132, 199, 0.4);
    }
    .brand-emblem svg {
      width: 22px;
      height: 22px;
      fill: #ffffff;
    }

    .brand-titles {
      display: flex;
      flex-direction: column;
    }

    .brand-name {
      font-family: var(--font-display);
      font-size: 20px;
      font-weight: 800;
      color: var(--text-white);
      letter-spacing: -0.3px;
      line-height: 1.1;
    }

    .brand-sub {
      font-size: 11.5px;
      color: var(--text-secondary);
      font-weight: 500;
    }

    /* Experience Switcher: MAP vs SITUATION */
    .view-switcher-pill {
      display: flex;
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid var(--border-subtle);
      border-radius: 7px;
      padding: 3px;
      margin-left: 10px;
    }

    .view-switch-btn {
      background: none;
      border: none;
      color: var(--text-secondary);
      font-family: var(--font-display);
      font-size: 12px;
      font-weight: 600;
      padding: 5px 14px;
      border-radius: 5px;
      cursor: pointer;
      transition: all 0.15s ease;
    }
    .view-switch-btn:hover { color: var(--text-white); }
    .view-switch-btn.active {
      background: #0284c7;
      color: #ffffff;
      box-shadow: 0 2px 8px rgba(2, 132, 199, 0.4);
    }

    /* Regional Weather Pulse (Overview Bar) */
    .regional-pulse-strip {
      display: flex;
      align-items: center;
      gap: 16px;
      background: var(--bg-elevated);
      border: 1px solid var(--border-subtle);
      border-radius: 8px;
      padding: 6px 14px;
    }

    .regional-domain-tag {
      display: flex;
      align-items: center;
      gap: 6px;
      font-family: var(--font-display);
      font-size: 12.5px;
      font-weight: 700;
      color: var(--text-white);
    }

    .live-status-dot {
      width: 7px;
      height: 7px;
      border-radius: 50%;
      background: var(--pulse-live);
      box-shadow: 0 0 8px var(--pulse-live);
      animation: pulse-live 2s infinite ease-in-out;
    }
    @keyframes pulse-live {
      0%, 100% { opacity: 1; transform: scale(1); }
      50% { opacity: 0.4; transform: scale(1.2); }
    }

    .regional-metrics-text {
      font-size: 12.5px;
      color: var(--text-secondary);
    }
    .regional-metrics-text strong {
      color: var(--text-white);
      font-weight: 600;
    }

    /* Right Tools & Data Ingest */
    .header-actions {
      display: flex;
      align-items: center;
      gap: 14px;
    }

    .data-health-pill {
      display: flex;
      align-items: center;
      gap: 8px;
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid var(--border-subtle);
      border-radius: 6px;
      padding: 6px 12px;
      font-size: 12px;
      color: var(--text-secondary);
      cursor: pointer;
      transition: all 0.15s ease;
    }
    .data-health-pill:hover {
      background: rgba(255, 255, 255, 0.09);
      color: var(--text-white);
    }
    .data-sensor-dots {
      display: flex;
      gap: 4px;
    }
    .sensor-dot {
      width: 5px;
      height: 5px;
      border-radius: 50%;
      background: var(--pulse-live);
    }

    .focus-mode-badge {
      display: flex;
      align-items: center;
      gap: 6px;
      background: rgba(239, 68, 68, 0.15);
      border: 1px solid rgba(239, 68, 68, 0.35);
      border-radius: 6px;
      padding: 6px 12px;
      font-family: var(--font-display);
      font-size: 12px;
      font-weight: 700;
      color: #fca5a5;
      cursor: pointer;
    }
    .focus-mode-badge:hover {
      background: rgba(239, 68, 68, 0.25);
    }

    /* ==========================================================================
       3. MAIN VIEWPORT
       ========================================================================== */
    .main-viewport {
      display: flex;
      height: calc(100vh - 62px);
      width: 100vw;
      position: relative;
    }

    /* ==========================================================================
       4. LEFT PANEL: HORIZONS, DATA LAYERS & ACTIVE STORMS
       ========================================================================== */
    .left-panel {
      width: 310px;
      min-width: 310px;
      background: var(--bg-panel-solid);
      border-right: 1px solid var(--border-subtle);
      display: flex;
      flex-direction: column;
      gap: 18px;
      padding: 18px;
      z-index: 500;
      overflow-y: auto;
    }

    .section-header {
      font-family: var(--font-display);
      font-size: 12px;
      font-weight: 700;
      letter-spacing: 0.6px;
      text-transform: uppercase;
      color: var(--text-secondary);
      margin-bottom: 8px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    /* Horizon Pill Grid */
    .horizon-pill-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 6px;
    }

    .horizon-btn {
      background: var(--bg-elevated);
      border: 1px solid var(--border-subtle);
      border-radius: 6px;
      padding: 8px 4px;
      text-align: center;
      font-family: var(--font-display);
      font-size: 12px;
      font-weight: 600;
      color: var(--text-secondary);
      cursor: pointer;
      transition: all 0.15s ease;
    }
    .horizon-btn:hover {
      background: var(--bg-elevated-hover);
      color: var(--text-white);
    }
    .horizon-btn.active {
      background: #0284c7;
      border-color: #38bdf8;
      color: #ffffff;
      box-shadow: 0 4px 12px rgba(2, 132, 199, 0.4);
    }

    /* Data Layers Controls */
    .layer-cards-stack {
      display: flex;
      flex-direction: column;
      gap: 6px;
    }

    .layer-item-card {
      display: flex;
      align-items: center;
      justify-content: space-between;
      background: var(--bg-elevated);
      border: 1px solid var(--border-subtle);
      border-radius: 8px;
      padding: 10px 12px;
      cursor: pointer;
      transition: all 0.15s ease;
    }
    .layer-item-card:hover {
      background: var(--bg-elevated-hover);
      border-color: var(--border-medium);
    }
    .layer-item-card.active {
      border-color: rgba(56, 189, 248, 0.35);
    }

    .layer-leading-wrap {
      display: flex;
      align-items: center;
      gap: 10px;
    }

    .layer-icon-box {
      width: 28px;
      height: 28px;
      border-radius: 6px;
      background: rgba(255, 255, 255, 0.06);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 13px;
    }

    .layer-text-wrap {
      display: flex;
      flex-direction: column;
    }

    .layer-title-text {
      font-size: 13.5px;
      font-weight: 600;
      color: var(--text-white);
      line-height: 1.2;
    }

    .layer-sub-text {
      font-size: 11px;
      color: var(--text-muted);
    }

    .layer-switch-knob {
      width: 36px;
      height: 20px;
      background: #334155;
      border-radius: 10px;
      position: relative;
      transition: background 0.2s;
    }
    .layer-switch-knob::after {
      content: "";
      position: absolute;
      top: 2px;
      left: 2px;
      width: 16px;
      height: 16px;
      border-radius: 50%;
      background: #ffffff;
      transition: transform 0.2s;
    }
    .layer-item-card.active .layer-switch-knob {
      background: #0284c7;
    }
    .layer-item-card.active .layer-switch-knob::after {
      transform: translateX(16px);
    }

    /* Active Storms Cards */
    .storms-stack {
      display: flex;
      flex-direction: column;
      gap: 8px;
    }

    .storm-card {
      background: var(--bg-elevated);
      border: 1px solid var(--border-subtle);
      border-radius: 8px;
      padding: 12px 14px;
      cursor: pointer;
      transition: all 0.15s ease;
    }
    .storm-card:hover {
      background: var(--bg-elevated-hover);
      border-color: var(--border-medium);
    }
    .storm-card.selected {
      border-color: var(--radar-red);
      background: rgba(239, 68, 68, 0.09);
      box-shadow: 0 4px 18px rgba(239, 68, 68, 0.22);
    }

    .storm-card-top {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 4px;
    }

    .storm-card-title {
      font-family: var(--font-display);
      font-size: 15px;
      font-weight: 700;
      color: var(--text-white);
    }

    .storm-card-pill {
      font-size: 11px;
      font-weight: 700;
      padding: 2px 7px;
      border-radius: 4px;
      letter-spacing: 0.3px;
    }
    .pill-severe { background: rgba(239, 68, 68, 0.25); color: #fca5a5; }
    .pill-elevated { background: rgba(245, 158, 11, 0.25); color: #fde047; }

    .storm-card-details {
      font-size: 12px;
      color: var(--text-secondary);
    }

    /* ==========================================================================
       5. CENTER HERO: LIVING ATMOSPHERIC MAP (~70% VIEWPORT)
       ========================================================================== */
    .map-center-container {
      flex: 1;
      height: 100%;
      position: relative;
      background: #050912;
    }

    #liveAtmosphericMap {
      width: 100%;
      height: 100%;
      background: #050912;
    }

    /* Dynamic Atmospheric Pulse Banner (Signature VAJRA Element) */
    .atmospheric-pulse-banner {
      position: absolute;
      top: 18px;
      left: 50%;
      transform: translateX(-50%);
      z-index: 1000;
      background: rgba(13, 20, 36, 0.94);
      backdrop-filter: blur(14px);
      border: 1px solid var(--border-medium);
      border-radius: 30px;
      padding: 6px 18px;
      display: flex;
      align-items: center;
      gap: 16px;
      box-shadow: 0 8px 28px rgba(0, 0, 0, 0.65);
    }

    .pulse-title-tag {
      font-family: var(--font-display);
      font-size: 11px;
      font-weight: 800;
      letter-spacing: 0.8px;
      text-transform: uppercase;
      color: var(--text-secondary);
    }

    .pulse-stages-ribbon {
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .pulse-stage-item {
      display: flex;
      align-items: center;
      gap: 5px;
      font-size: 12px;
      color: var(--text-muted);
      font-weight: 500;
      transition: all 0.2s ease;
    }
    .pulse-stage-item.reached {
      color: var(--text-white);
      font-weight: 700;
    }
    .pulse-stage-item.active-severe {
      color: #fca5a5;
      font-weight: 800;
      text-shadow: 0 0 10px rgba(239, 68, 68, 0.6);
    }

    .pulse-connector-line {
      width: 16px;
      height: 2px;
      background: rgba(255, 255, 255, 0.12);
    }
    .pulse-connector-line.active {
      background: var(--radar-red);
    }

    /* Observed vs Forecast Smooth Pill */
    .mode-toggle-cluster {
      position: absolute;
      top: 18px;
      left: 18px;
      z-index: 1000;
      background: rgba(13, 20, 36, 0.94);
      backdrop-filter: blur(14px);
      border: 1px solid var(--border-medium);
      border-radius: 8px;
      padding: 4px;
      display: flex;
      gap: 4px;
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.6);
    }

    .mode-tab-button {
      background: none;
      border: none;
      color: var(--text-secondary);
      font-family: var(--font-display);
      font-size: 12px;
      font-weight: 600;
      padding: 6px 14px;
      border-radius: 6px;
      cursor: pointer;
      transition: all 0.15s ease;
    }
    .mode-tab-button:hover { color: var(--text-white); }
    .mode-tab-button.active {
      background: #0284c7;
      color: #ffffff;
      box-shadow: 0 2px 8px rgba(2, 132, 199, 0.5);
    }

    /* Impact Lens Floating Button */
    .impact-lens-button {
      position: absolute;
      top: 18px;
      right: 18px;
      z-index: 1000;
      background: rgba(13, 20, 36, 0.94);
      backdrop-filter: blur(14px);
      border: 1px solid var(--border-medium);
      border-radius: 8px;
      padding: 8px 16px;
      color: var(--text-white);
      font-family: var(--font-display);
      font-size: 12.5px;
      font-weight: 700;
      display: flex;
      align-items: center;
      gap: 8px;
      cursor: pointer;
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.6);
      transition: all 0.15s ease;
    }
    .impact-lens-button:hover {
      background: var(--bg-elevated-hover);
      border-color: var(--impact-gold);
    }
    .impact-lens-button.active {
      background: rgba(251, 191, 36, 0.15);
      border-color: var(--impact-gold);
      color: #fde047;
      box-shadow: 0 0 16px rgba(251, 191, 36, 0.3);
    }

    /* Radar Reflectivity Floating Legend */
    .radar-legend-card {
      position: absolute;
      top: 72px;
      right: 18px;
      z-index: 1000;
      background: rgba(13, 20, 36, 0.92);
      backdrop-filter: blur(14px);
      border: 1px solid var(--border-subtle);
      border-radius: 8px;
      padding: 10px 14px;
      display: flex;
      flex-direction: column;
      gap: 5px;
      box-shadow: 0 8px 24px rgba(0,0,0,0.5);
    }

    .legend-title-row {
      display: flex;
      justify-content: space-between;
      font-size: 11px;
      font-weight: 600;
      color: var(--text-secondary);
    }

    .legend-ramp-strip {
      width: 220px;
      height: 8px;
      border-radius: 4px;
      background: linear-gradient(to right,
        #06b6d4 0%,
        #3b82f6 20%,
        #10b981 40%,
        #f59e0b 60%,
        #f97316 75%,
        #ef4444 88%,
        #d946ef 100%
      );
    }

    .legend-scale-marks {
      display: flex;
      justify-content: space-between;
      font-size: 9.5px;
      color: var(--text-muted);
      font-weight: 500;
    }

    /* Radar Doppler Beam Sweep Animation (Living Atmosphere) */
    .radar-beam-overlay {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      pointer-events: none;
      z-index: 15;
      overflow: hidden;
      opacity: 0.3;
      display: none;
    }
    .radar-beam-overlay.active {
      display: block;
    }
    .doppler-sweep-line {
      position: absolute;
      top: 50%;
      left: 50%;
      width: 50vw;
      height: 2px;
      background: linear-gradient(to right, rgba(56, 189, 248, 0.95), transparent);
      transform-origin: 0% 0%;
      animation: doppler-spin 7s linear infinite;
      box-shadow: 0 0 16px rgba(56, 189, 248, 0.8);
    }
    @keyframes doppler-spin {
      0% { transform: rotate(0deg); }
      100% { transform: rotate(360deg); }
    }

    /* ==========================================================================
       6. BOTTOM: FORECAST TIME MACHINE
       ========================================================================== */
    .time-machine-container {
      position: absolute;
      bottom: 24px;
      left: 32px;
      right: 32px;
      z-index: 1000;
      background: rgba(13, 20, 36, 0.95);
      backdrop-filter: blur(16px);
      border: 1px solid var(--border-medium);
      border-radius: 14px;
      padding: 14px 24px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 22px;
      box-shadow: 0 14px 40px rgba(0, 0, 0, 0.75);
    }

    .play-evolution-button {
      background: #0284c7;
      border: none;
      border-radius: 8px;
      padding: 9px 18px;
      color: #ffffff;
      font-family: var(--font-display);
      font-size: 13.5px;
      font-weight: 700;
      display: inline-flex;
      align-items: center;
      gap: 8px;
      cursor: pointer;
      box-shadow: 0 4px 14px rgba(2, 132, 199, 0.45);
      transition: all 0.15s ease;
    }
    .play-evolution-button:hover {
      background: #0369a1;
      transform: translateY(-1px);
    }

    .timeline-scrubber-track {
      flex: 1;
      display: flex;
      align-items: center;
      justify-content: space-between;
      position: relative;
    }

    .timeline-rail-bar {
      position: absolute;
      left: 14px;
      right: 14px;
      height: 4px;
      background: rgba(255, 255, 255, 0.12);
      border-radius: 2px;
      z-index: 1;
    }

    .time-step-node {
      position: relative;
      z-index: 2;
      display: flex;
      flex-direction: column;
      align-items: center;
      cursor: pointer;
      padding: 6px 12px;
      border-radius: 8px;
      transition: all 0.15s ease;
    }
    .time-step-node:hover {
      background: rgba(255, 255, 255, 0.08);
    }

    .node-pin-dot {
      width: 14px;
      height: 14px;
      border-radius: 50%;
      background: #334155;
      border: 3px solid var(--bg-panel-solid);
      margin-bottom: 6px;
      transition: all 0.15s ease;
    }

    .node-time-label {
      font-family: var(--font-display);
      font-size: 12.5px;
      font-weight: 600;
      color: var(--text-secondary);
      letter-spacing: 0.2px;
    }

    .time-step-node.active .node-pin-dot {
      background: #38bdf8;
      box-shadow: 0 0 12px #38bdf8;
      transform: scale(1.35);
    }
    .time-step-node.active .node-time-label {
      color: #ffffff;
      font-weight: 700;
    }

    /* ==========================================================================
       7. RIGHT PANEL: EDITORIAL CONTEXTUAL INTELLIGENCE
       ========================================================================== */
    .right-editorial-panel {
      width: 390px;
      min-width: 390px;
      background: var(--bg-panel-solid);
      border-left: 1px solid var(--border-subtle);
      display: flex;
      flex-direction: column;
      gap: 20px;
      padding: 22px;
      z-index: 500;
      overflow-y: auto;
    }

    /* Selected Storm Header */
    .storm-hero-header {
      display: flex;
      flex-direction: column;
      gap: 6px;
      border-bottom: 1px solid var(--border-subtle);
      padding-bottom: 16px;
    }

    .storm-hero-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .storm-hero-title {
      font-family: var(--font-display);
      font-size: 26px;
      font-weight: 800;
      color: var(--text-white);
      letter-spacing: -0.5px;
    }

    .storm-threat-tag {
      background: rgba(239, 68, 68, 0.2);
      border: 1px solid rgba(239, 68, 68, 0.4);
      color: #f87171;
      font-family: var(--font-display);
      font-size: 11px;
      font-weight: 700;
      padding: 4px 10px;
      border-radius: 6px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }

    .storm-narrative-callout {
      font-size: 14.5px;
      font-weight: 600;
      color: #fca5a5;
    }

    /* 4 Primary Hero Numbers (Large Editorial Numbers) */
    .hero-numbers-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
    }

    .hero-metric-box {
      background: var(--bg-elevated);
      border: 1px solid var(--border-subtle);
      border-radius: 10px;
      padding: 14px;
      display: flex;
      flex-direction: column;
    }

    .hero-metric-number {
      font-family: var(--font-display);
      font-size: 28px;
      font-weight: 800;
      color: var(--text-white);
      line-height: 1.1;
      letter-spacing: -0.5px;
    }
    .hero-metric-number.num-severe { color: var(--radar-red); }
    .hero-metric-number.num-cyan { color: var(--radar-cyan); }

    .hero-metric-subtext {
      font-size: 12px;
      color: var(--text-secondary);
      font-weight: 500;
      margin-top: 4px;
    }

    /* Section: STORM STORY (Visual Narrative Timeline) */
    .editorial-section {
      display: flex;
      flex-direction: column;
      gap: 10px;
    }

    .editorial-title {
      font-family: var(--font-display);
      font-size: 12px;
      font-weight: 700;
      letter-spacing: 0.5px;
      text-transform: uppercase;
      color: var(--text-secondary);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .story-timeline-track {
      display: flex;
      flex-direction: column;
      gap: 8px;
      border-left: 2px solid rgba(255, 255, 255, 0.12);
      margin-left: 6px;
      padding-left: 14px;
    }

    .story-node-item {
      display: flex;
      flex-direction: column;
      position: relative;
    }
    .story-node-item::before {
      content: "";
      position: absolute;
      left: -19px;
      top: 4px;
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: #475569;
      border: 2px solid var(--bg-panel-solid);
    }
    .story-node-item.completed::before {
      background: var(--radar-cyan);
      box-shadow: 0 0 6px var(--radar-cyan);
    }
    .story-node-item.active-now::before {
      background: var(--radar-red);
      box-shadow: 0 0 8px var(--radar-red);
    }

    .story-time-stamp {
      font-size: 11px;
      font-weight: 700;
      color: var(--text-muted);
    }
    .story-desc-text {
      font-size: 12.5px;
      font-weight: 500;
      color: var(--text-bright);
    }

    /* Section: WHAT CHANGED? · LAST 15 MIN */
    .what-changed-grid {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 8px;
    }

    .change-metric-card {
      background: var(--bg-elevated);
      border: 1px solid var(--border-subtle);
      border-radius: 8px;
      padding: 10px 12px;
      display: flex;
      flex-direction: column;
    }

    .change-key {
      font-size: 11.5px;
      color: var(--text-secondary);
      font-weight: 500;
    }

    .change-delta {
      font-family: var(--font-display);
      font-size: 16px;
      font-weight: 800;
      color: var(--radar-red);
      margin-top: 2px;
    }

    /* Section: IMPACT LENS INTERSECTIONS */
    .impact-targets-list {
      display: flex;
      flex-direction: column;
      gap: 8px;
    }

    .impact-target-card {
      background: var(--bg-elevated);
      border-left: 3px solid var(--impact-gold);
      border-radius: 0 8px 8px 0;
      padding: 10px 14px;
      display: flex;
      flex-direction: column;
      gap: 2px;
    }

    .impact-target-title {
      font-size: 13px;
      font-weight: 700;
      color: var(--text-white);
      display: flex;
      justify-content: space-between;
    }

    .impact-target-desc {
      font-size: 12px;
      color: var(--text-secondary);
      line-height: 1.35;
    }

    /* ==========================================================================
       8. SITUATION VIEW (EXECUTIVE REGIONAL OVERVIEW OVERLAY)
       ========================================================================== */
    .situation-view-overlay {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(7, 11, 20, 0.96);
      backdrop-filter: blur(16px);
      z-index: 2000;
      display: none;
      flex-direction: column;
      padding: 32px 48px;
      overflow-y: auto;
    }
    .situation-view-overlay.active {
      display: flex;
    }

    .situation-header-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 24px;
      border-bottom: 1px solid var(--border-subtle);
      padding-bottom: 16px;
    }

    .situation-main-title {
      font-family: var(--font-display);
      font-size: 28px;
      font-weight: 800;
      color: var(--text-white);
    }

    .situation-grid-layout {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 20px;
    }

    .situation-card {
      background: var(--bg-elevated);
      border: 1px solid var(--border-subtle);
      border-radius: 12px;
      padding: 20px;
      display: flex;
      flex-direction: column;
      gap: 12px;
    }

    .situation-card-title {
      font-family: var(--font-display);
      font-size: 14px;
      font-weight: 700;
      color: var(--text-white);
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }

    /* Modal / Data Health Tray */
    .data-health-modal {
      position: fixed;
      top: 72px;
      right: 22px;
      width: 320px;
      background: rgba(13, 20, 36, 0.98);
      backdrop-filter: blur(16px);
      border: 1px solid var(--border-medium);
      border-radius: 12px;
      padding: 16px;
      z-index: 3000;
      display: none;
      box-shadow: 0 16px 40px rgba(0, 0, 0, 0.8);
    }
    .data-health-modal.active {
      display: flex;
      flex-direction: column;
      gap: 10px;
    }

    /* ==========================================================================
       9. LEAFLET CUSTOM STYLING & ATMOSPHERIC PARTICLES
       ========================================================================== */
    .leaflet-container {
      background: #050912 !important;
      font-family: var(--font-body);
    }

    /* Filter for high-definition imagery */
    .leaflet-tile-pane {
      filter: brightness(0.70) contrast(1.22) saturate(1.15);
    }

    /* Storm Core Marker */
    .pulsing-storm-centroid {
      width: 34px;
      height: 34px;
      border-radius: 50%;
      background: rgba(239, 68, 68, 0.45);
      border: 2px solid #ef4444;
      display: flex;
      align-items: center;
      justify-content: center;
      color: #ffffff;
      font-family: var(--font-display);
      font-size: 12px;
      font-weight: 800;
      box-shadow: 0 0 20px rgba(239, 68, 68, 0.85);
      cursor: pointer;
      animation: centroid-pulse 2s infinite ease-in-out;
    }
    @keyframes centroid-pulse {
      0%, 100% { transform: scale(1); box-shadow: 0 0 14px rgba(239, 68, 68, 0.7); }
      50% { transform: scale(1.15); box-shadow: 0 0 28px rgba(239, 68, 68, 1); }
    }

    /* Lightning Pulse Strobe */
    .lightning-strobe-dot {
      width: 14px;
      height: 14px;
      border-radius: 50%;
      background: #67e8f9;
      box-shadow: 0 0 14px #38bdf8;
      animation: ltg-ping 1.6s infinite ease-out;
    }
    @keyframes ltg-ping {
      0% { transform: scale(0.3); opacity: 1; }
      50% { transform: scale(2.0); opacity: 0.6; }
      100% { transform: scale(3.2); opacity: 0; }
    }

    /* City Label Pill on Map */
    .city-geotag-pill {
      background: rgba(7, 11, 20, 0.88);
      border: 1px solid rgba(255, 255, 255, 0.18);
      border-radius: 4px;
      padding: 2px 7px;
      font-size: 11px;
      font-weight: 600;
      color: #ffffff;
      white-space: nowrap;
      pointer-events: none;
    }

    /* Impact Warning Callout Tag on Map */
    .impact-corridor-tag {
      background: rgba(245, 158, 11, 0.92);
      border: 1px solid #fbbf24;
      border-radius: 4px;
      padding: 3px 8px;
      font-size: 10.5px;
      font-weight: 700;
      color: #000000;
      white-space: nowrap;
      box-shadow: 0 4px 14px rgba(245, 158, 11, 0.5);
    }
  </style>
</head>
<body>

  <!-- ==========================================================================
       TOP PRODUCT HEADER
       ========================================================================== -->
  <header class="top-header">
    <div class="brand-section">
      <div class="brand-emblem">
        <svg viewBox="0 0 24 24"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/></svg>
      </div>
      <div class="brand-titles">
        <span class="brand-name">VAJRA</span>
        <span class="brand-sub">Atmospheric Intelligence Platform</span>
      </div>

      <!-- Experience Switcher: MAP vs SITUATION -->
      <div class="view-switcher-pill">
        <button class="view-switch-btn active" id="btnSwitchMap">MAP VIEW</button>
        <button class="view-switch-btn" id="btnSwitchSituation">SITUATION</button>
      </div>
    </div>

    <!-- Center: Regional Weather Pulse -->
    <div class="regional-pulse-strip">
      <div class="regional-domain-tag">
        <span class="live-status-dot"></span>
        <span>EASTERN INDIA</span>
      </div>
      <div class="regional-metrics-text">
        <strong>12</strong> Active Cells &bull; <strong>4</strong> Intensifying &bull; <strong>1</strong> High-Impact Corridor
      </div>
    </div>

    <!-- Right Header Tools -->
    <div class="header-actions">
      <!-- Data Ingest Health Pill -->
      <div class="data-health-pill" id="btnToggleDataHealth" title="Inspect Data Ingestion Pipelines">
        <span>DATA INGEST:</span>
        <div class="data-sensor-dots">
          <span class="sensor-dot" title="Radar Mosaic: Live"></span>
          <span class="sensor-dot" title="INSAT-3DR: Live"></span>
          <span class="sensor-dot" title="Lightning: Live"></span>
          <span class="sensor-dot" title="NWP Model: Synced"></span>
        </div>
      </div>

      <!-- Focus Mode Pill -->
      <div class="focus-mode-badge" id="btnFocusMode" title="Focus into selected storm centroid">
        <span>🔍 FOCUS: CELL 024</span>
      </div>
    </div>
  </header>

  <!-- ==========================================================================
       MAIN APP WORKSPACE
       ========================================================================== -->
  <main class="main-viewport">

    <!-- LEFT PANEL: FORECAST HORIZONS, LAYERS, ACTIVE STORMS -->
    <aside class="left-panel">
      <!-- Forecast Horizon Buttons -->
      <div>
        <div class="section-header">
          <span>FORECAST HORIZON</span>
          <span style="color:var(--radar-cyan); font-weight:700;" id="horizonLabelDisplay">+30 MIN</span>
        </div>
        <div class="horizon-pill-grid">
          <button class="horizon-btn" data-step="1">15 MIN</button>
          <button class="horizon-btn active" data-step="2">30 MIN</button>
          <button class="horizon-btn" data-step="3">45 MIN</button>
          <button class="horizon-btn" data-step="4">1 HR</button>
          <button class="horizon-btn" data-step="5">2 HR</button>
          <button class="horizon-btn" data-step="6">3 HR</button>
        </div>
      </div>

      <!-- Atmospheric Data Layers -->
      <div>
        <div class="section-header">
          <span>ATMOSPHERIC LAYERS</span>
        </div>
        <div class="layer-cards-stack">
          <div class="layer-item-card active" id="cardLayerRadar">
            <div class="layer-leading-wrap">
              <div class="layer-icon-box">📡</div>
              <div class="layer-text-wrap">
                <span class="layer-title-text">Radar Reflectivity</span>
                <span class="layer-sub-text">Composite dBZ &bull; LIVE</span>
              </div>
            </div>
            <div class="layer-switch-knob"></div>
          </div>

          <div class="layer-item-card active" id="cardLayerSat">
            <div class="layer-leading-wrap">
              <div class="layer-icon-box">🛰</div>
              <div class="layer-text-wrap">
                <span class="layer-title-text">Satellite Cloud Top</span>
                <span class="layer-sub-text">INSAT-3DR 10.8µm &bull; 8m ago</span>
              </div>
            </div>
            <div class="layer-switch-knob"></div>
          </div>

          <div class="layer-item-card active" id="cardLayerLtg">
            <div class="layer-leading-wrap">
              <div class="layer-icon-box">⚡</div>
              <div class="layer-text-wrap">
                <span class="layer-title-text">Lightning Discharges</span>
                <span class="layer-sub-text">Pulse density &bull; LIVE</span>
              </div>
            </div>
            <div class="layer-switch-knob"></div>
          </div>

          <div class="layer-item-card active" id="cardLayerTracks">
            <div class="layer-leading-wrap">
              <div class="layer-icon-box">↗</div>
              <div class="layer-text-wrap">
                <span class="layer-title-text">Storm Trajectories</span>
                <span class="layer-sub-text">Shadows &amp; Forecast Field</span>
              </div>
            </div>
            <div class="layer-switch-knob"></div>
          </div>

          <div class="layer-item-card active" id="cardLayerSweep">
            <div class="layer-leading-wrap">
              <div class="layer-icon-box">🌀</div>
              <div class="layer-text-wrap">
                <span class="layer-title-text">Radar Beam Scan</span>
                <span class="layer-sub-text">Doppler sweep motion</span>
              </div>
            </div>
            <div class="layer-switch-knob"></div>
          </div>
        </div>
      </div>

      <!-- Active Storms List -->
      <div style="flex:1;">
        <div class="section-header">
          <span>TRACKED STORMS</span>
          <span style="color:var(--radar-red);">3 DETECTED</span>
        </div>
        <div class="storms-stack">
          <!-- Storm Cell 024 -->
          <div class="storm-card selected" id="stormSelect024" onclick="selectStorm('024')">
            <div class="storm-card-top">
              <span class="storm-card-title">Storm Cell 024</span>
              <span class="storm-card-pill pill-severe">68 dBZ</span>
            </div>
            <div class="storm-card-details">Rapidly intensifying &bull; ENE 34 km/h</div>
          </div>

          <!-- Storm Cell 018 -->
          <div class="storm-card" id="stormSelect018" onclick="selectStorm('018')">
            <div class="storm-card-top">
              <span class="storm-card-title">Storm Cell 018</span>
              <span class="storm-card-pill pill-elevated">52 dBZ</span>
            </div>
            <div class="storm-card-details">Forward advection &bull; E 28 km/h</div>
          </div>

          <!-- Storm Cell 031 -->
          <div class="storm-card" id="stormSelect031" onclick="selectStorm('031')">
            <div class="storm-card-top">
              <span class="storm-card-title">Storm Cell 031</span>
              <span class="storm-card-pill pill-severe">59 dBZ</span>
            </div>
            <div class="storm-card-details">Coastal squall segment &bull; NE 52 km/h</div>
          </div>
        </div>
      </div>
    </aside>

    <!-- CENTER HERO: THE LIVING ATMOSPHERIC MAP (~70% VIEWPORT) -->
    <section class="map-center-container">
      <div id="liveAtmosphericMap"></div>

      <!-- Doppler Beam Sweep Animation Overlay -->
      <div class="radar-beam-overlay active" id="radarBeamScan">
        <div class="doppler-sweep-line"></div>
      </div>

      <!-- Signature Atmospheric Pulse Banner (Top Center) -->
      <div class="atmospheric-pulse-banner">
        <span class="pulse-title-tag">ATMOSPHERIC PULSE</span>
        <div class="pulse-stages-ribbon">
          <div class="pulse-stage-item reached">
            <span>● Stable</span>
          </div>
          <div class="pulse-connector-line active"></div>
          <div class="pulse-stage-item reached">
            <span>● Developing</span>
          </div>
          <div class="pulse-connector-line active"></div>
          <div class="pulse-stage-item reached">
            <span>● Intensifying</span>
          </div>
          <div class="pulse-connector-line active"></div>
          <div class="pulse-stage-item active-severe" id="pulseStageCurrent">
            <span>● Severe (68 dBZ)</span>
          </div>
        </div>
      </div>

      <!-- Mode Toggle: Observed vs Forecast -->
      <div class="mode-toggle-cluster">
        <button class="mode-tab-button" id="tabModeObserved">OBSERVED</button>
        <button class="mode-tab-button active" id="tabModeForecast">FORECAST</button>
      </div>

      <!-- Impact Lens Toggle Button -->
      <button class="impact-lens-button" id="btnImpactLens">
        <span>🔍 IMPACT LENS</span>
      </button>

      <!-- Radar Reflectivity Legend -->
      <div class="radar-legend-card">
        <div class="legend-title-row">
          <span>RADAR REFLECTIVITY</span>
          <span style="color:var(--radar-red); font-weight:700;">HAIL &gt; 55 dBZ</span>
        </div>
        <div class="legend-ramp-strip"></div>
        <div class="legend-scale-marks">
          <span>15</span>
          <span>25</span>
          <span>35</span>
          <span>45</span>
          <span>55</span>
          <span>65+ dBZ</span>
        </div>
      </div>

      <!-- BOTTOM: FORECAST TIME MACHINE -->
      <div class="time-machine-container">
        <button class="play-evolution-button" id="btnPlayEvolution">
          <span id="playStateIcon">▶</span>
          <span id="playStateLabel">PLAY EVOLUTION</span>
        </button>

        <div class="timeline-scrubber-track">
          <div class="timeline-rail-bar"></div>

          <div class="time-step-node" data-idx="0">
            <div class="node-pin-dot"></div>
            <span class="node-time-label">NOW</span>
          </div>

          <div class="time-step-node" data-idx="1">
            <div class="node-pin-dot"></div>
            <span class="node-time-label">+15m</span>
          </div>

          <div class="time-step-node active" data-idx="2">
            <div class="node-pin-dot"></div>
            <span class="node-time-label">+30m</span>
          </div>

          <div class="time-step-node" data-idx="3">
            <div class="node-pin-dot"></div>
            <span class="node-time-label">+45m</span>
          </div>

          <div class="time-step-node" data-idx="4">
            <div class="node-pin-dot"></div>
            <span class="node-time-label">+60m</span>
          </div>

          <div class="time-step-node" data-idx="5">
            <div class="node-pin-dot"></div>
            <span class="node-time-label">+90m</span>
          </div>

          <div class="time-step-node" data-idx="6">
            <div class="node-pin-dot"></div>
            <span class="node-time-label">+120m</span>
          </div>
        </div>
      </div>
    </section>

    <!-- RIGHT PANEL: EDITORIAL CONTEXTUAL INTELLIGENCE -->
    <aside class="right-editorial-panel">
      <!-- Storm Hero Header -->
      <div class="storm-hero-header">
        <div class="storm-hero-row">
          <span class="storm-hero-title" id="intelTitle">STORM CELL 024</span>
          <span class="storm-threat-tag" id="intelBadge">SEVERE</span>
        </div>
        <div class="storm-narrative-callout" id="intelNarrative">RAPIDLY INTENSIFYING</div>
      </div>

      <!-- 4 Primary Hero Numbers -->
      <div class="hero-numbers-grid">
        <div class="hero-metric-box">
          <span class="hero-metric-number num-severe" id="numDbz">68 dBZ</span>
          <span class="hero-metric-subtext">Current intensity</span>
        </div>

        <div class="hero-metric-box">
          <span class="hero-metric-number" id="numSpeed">34 km/h</span>
          <span class="hero-metric-subtext" id="numDirection">Moving southeast</span>
        </div>

        <div class="hero-metric-box">
          <span class="hero-metric-number num-cyan" id="numArrival">18–27 min</span>
          <span class="hero-metric-subtext">Arrival window</span>
        </div>

        <div class="hero-metric-box">
          <span class="hero-metric-number" id="numConfidence">87%</span>
          <span class="hero-metric-subtext">Forecast confidence</span>
        </div>
      </div>

      <!-- Section: STORM STORY (Visual Narrative Timeline) -->
      <div class="editorial-section">
        <div class="editorial-title">
          <span>STORM STORY &bull; EVOLUTION</span>
          <span style="color:var(--radar-cyan);">5 PHASES</span>
        </div>
        <div class="story-timeline-track" id="storyTrackContainer">
          <div class="story-node-item completed">
            <span class="story-time-stamp">14:10 &bull; FORMED</span>
            <span class="story-desc-text">Cell detected in Midnapore sector (38 dBZ)</span>
          </div>
          <div class="story-node-item completed">
            <span class="story-time-stamp">14:18 &bull; DEVELOPING</span>
            <span class="story-desc-text">Reflectivity increasing (+10 dBZ in 8m)</span>
          </div>
          <div class="story-node-item completed">
            <span class="story-time-stamp">14:26 &bull; LIGHTNING ACCELERATION</span>
            <span class="story-desc-text">Discharge rate spiked to 38 strokes/min</span>
          </div>
          <div class="story-node-item active-now">
            <span class="story-time-stamp">14:34 &bull; INTENSIFYING (NOW)</span>
            <span class="story-desc-text">Overshooting cloud top &bull; Severe hail core formed</span>
          </div>
          <div class="story-node-item">
            <span class="story-time-stamp">14:50 &bull; PROJECTED PEAK</span>
            <span class="story-desc-text">Direct crossing of Kolkata-Howrah urban corridor</span>
          </div>
        </div>
      </div>

      <!-- Section: WHAT CHANGED? · LAST 15 MIN -->
      <div class="editorial-section">
        <div class="editorial-title">
          <span>WHAT CHANGED? &bull; LAST 15 MIN</span>
          <span style="color:var(--radar-red);">↗ ESCALATING</span>
        </div>
        <div class="what-changed-grid">
          <div class="change-metric-card">
            <span class="change-key">Radar Intensity</span>
            <span class="change-delta">+14 dBZ</span>
          </div>
          <div class="change-metric-card">
            <span class="change-key">Lightning Activity</span>
            <span class="change-delta">+27%</span>
          </div>
          <div class="change-metric-card">
            <span class="change-key">Cloud-Top Cooling</span>
            <span class="change-delta" style="color:var(--radar-cyan);">&darr; -6.2&deg;C</span>
          </div>
          <div class="change-metric-card">
            <span class="change-key">Storm Footprint</span>
            <span class="change-delta">+18%</span>
          </div>
        </div>
      </div>

      <!-- Section: IMPACT LENS & DECISION SUPPORT -->
      <div class="editorial-section">
        <div class="editorial-title">
          <span>POTENTIAL IMPACT &bull; CORRIDOR</span>
          <span style="color:var(--impact-gold);">INTERSECT</span>
        </div>
        <div class="impact-targets-list">
          <div class="impact-target-card">
            <div class="impact-target-title">
              <span>✈ VECC Kolkata Airport</span>
              <span style="color:var(--radar-red);">ETA 22 min</span>
            </div>
            <span class="impact-target-desc">Holding patterns recommended. Microburst risk on runway 19L/01R.</span>
          </div>

          <div class="impact-target-card">
            <div class="impact-target-title">
              <span>🛣 Major Highways NH-16 &amp; NH-19</span>
              <span style="color:var(--radar-amber);">ETA 14 min</span>
            </div>
            <span class="impact-target-desc">Severe squall crossing with crosswinds exceeding 75 km/h.</span>
          </div>

          <div class="impact-target-card">
            <div class="impact-target-title">
              <span>⚡ 765kV Regional Transmission</span>
              <span style="color:var(--radar-orange);">High Risk</span>
            </div>
            <span class="impact-target-desc">Midnapore substation circuit surge hazard from intense CG flashes.</span>
          </div>

          <div class="impact-target-card">
            <div class="impact-target-title">
              <span>👥 Population Settlements</span>
              <span style="color:#ffffff;">182K Persons</span>
            </div>
            <span class="impact-target-desc">High-density wards across Howrah and Hooghly within direct storm footprint.</span>
          </div>
        </div>
      </div>
    </aside>
  </main>

  <!-- ==========================================================================
       10. SITUATION VIEW (EXECUTIVE REGIONAL OVERVIEW OVERLAY)
       ========================================================================== -->
  <div class="situation-view-overlay" id="situationOverlay">
    <div class="situation-header-row">
      <div>
        <h1 class="situation-main-title">REGIONAL SITUATION REPORT &bull; EASTERN INDIA</h1>
        <p style="color:var(--text-secondary); margin-top:4px;">Comprehensive atmospheric status for State &amp; National Disaster Authorities</p>
      </div>
      <button class="view-switch-btn active" id="btnCloseSituation" style="padding:10px 20px;">BACK TO MAP</button>
    </div>

    <div class="situation-grid-layout">
      <div class="situation-card">
        <span class="situation-card-title">🚨 Active Severe Warnings</span>
        <div style="font-size:13px; color:var(--text-secondary); display:flex; flex-direction:column; gap:8px;">
          <div><strong style="color:var(--radar-red);">RED NOWCAST:</strong> Kolkata Metropolitan &amp; Howrah districts under immediate squall &amp; lightning warning valid until 16:00 IST.</div>
          <div><strong style="color:var(--radar-amber);">ORANGE WATCH:</strong> Burdwan &amp; Nadia districts under elevated convective growth advisory.</div>
        </div>
      </div>

      <div class="situation-card">
        <span class="situation-card-title">✈ Aviation &amp; Aerodromes</span>
        <div style="font-size:13px; color:var(--text-secondary); display:flex; flex-direction:column; gap:8px;">
          <div><strong>VECC (Kolkata):</strong> Wind shear advisory active. Terminal area convective cloud tops exceeding FL450.</div>
          <div><strong>VEBD (Bagdogra):</strong> Clear &bull; Standard VFR operations.</div>
        </div>
      </div>

      <div class="situation-card">
        <span class="situation-card-title">⚡ Energy &amp; Power Grid</span>
        <div style="font-size:13px; color:var(--text-secondary); display:flex; flex-direction:column; gap:8px;">
          <div><strong>Eastern Regional Load Dispatch:</strong> 182 CG strikes registered within 10km of 765kV transmission corridors in past 30 min.</div>
        </div>
      </div>
    </div>
  </div>

  <!-- ==========================================================================
       11. DATA HEALTH TRAY MODAL
       ========================================================================== -->
  <div class="data-health-modal" id="dataHealthModal">
    <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid var(--border-subtle); padding-bottom:8px;">
      <strong style="color:#ffffff; font-size:13px;">DATA PIPELINE HEALTH</strong>
      <span style="cursor:pointer; color:var(--text-muted);" id="btnCloseHealth">&times;</span>
    </div>
    <div style="display:flex; flex-direction:column; gap:6px; font-size:12px;">
      <div style="display:flex; justify-content:space-between;">
        <span>DWR Radar Network:</span>
        <span style="color:var(--pulse-live); font-weight:bold;">18/18 LIVE (3m)</span>
      </div>
      <div style="display:flex; justify-content:space-between;">
        <span>INSAT-3DR Rapid Scan:</span>
        <span style="color:var(--pulse-live); font-weight:bold;">NOMINAL (4m)</span>
      </div>
      <div style="display:flex; justify-content:space-between;">
        <span>GLD360 Lightning Feed:</span>
        <span style="color:var(--pulse-live); font-weight:bold;">REAL-TIME (12s)</span>
      </div>
      <div style="display:flex; justify-content:space-between;">
        <span>WRF / NWP Assimilation:</span>
        <span style="color:var(--pulse-live); font-weight:bold;">06Z INGESTED</span>
      </div>
    </div>
  </div>

  <!-- ==========================================================================
       12. JAVASCRIPT: SCIENTIFIC GEOSPATIAL ENGINE & INTERACTIVITY
       ========================================================================== -->
  <script>
    /* ==========================================================================
       DATA MATRIX: STORM EVOLUTION NARRATIVES
       ========================================================================== */
    const STORM_REGISTRY = {
      '024': {
        id: 'STORM CELL 024',
        badge: 'SEVERE',
        narrative: 'RAPIDLY INTENSIFYING',
        dbz: '68 dBZ',
        speed: '34 km/h',
        direction: 'Moving southeast',
        arrival: '18–27 min',
        confidence: '87%',
        center: [22.62, 88.20],
        pulseStage: '● Severe (68 dBZ)',
        track: [
          [22.42, 87.85], // NOW
          [22.51, 88.08], // +15m
          [22.60, 88.32], // +30m
          [22.68, 88.54], // +45m
          [22.76, 88.76], // +60m
          [22.88, 89.10], // +90m
          [23.00, 89.45]  // +120m
        ],
        lightnings: [
          [22.44, 87.87], [22.41, 87.82], [22.47, 87.92],
          [22.39, 87.80], [22.45, 87.94]
        ],
        story: [
          { time: '14:10 \u2022 FORMED', desc: 'Cell detected in Midnapore sector (38 dBZ)', status: 'completed' },
          { time: '14:18 \u2022 DEVELOPING', desc: 'Reflectivity increasing (+10 dBZ in 8m)', status: 'completed' },
          { time: '14:26 \u2022 LIGHTNING ACCELERATION', desc: 'Discharge rate spiked to 38 strikes/min', status: 'completed' },
          { time: '14:34 \u2022 INTENSIFYING (NOW)', desc: 'Overshooting cloud top \u2022 Severe hail core formed', status: 'active-now' },
          { time: '14:50 \u2022 PROJECTED PEAK', desc: 'Direct crossing of Kolkata-Howrah urban corridor', status: 'pending' }
        ],
        changes: { dbz: '+14 dBZ', ltg: '+27%', temp: '\u2193 -6.2\u00b0C', area: '+18%' }
      },

      '018': {
        id: 'STORM CELL 018',
        badge: 'ELEVATED',
        narrative: 'FORWARD ADVECTION',
        dbz: '52 dBZ',
        speed: '28 km/h',
        direction: 'Moving east',
        arrival: '35–45 min',
        confidence: '82%',
        center: [23.25, 88.10],
        pulseStage: '● Developing (52 dBZ)',
        track: [
          [23.24, 87.88], [23.28, 88.14], [23.32, 88.38],
          [23.36, 88.62], [23.40, 88.86], [23.46, 89.18], [23.52, 89.50]
        ],
        lightnings: [
          [23.22, 87.85], [23.26, 87.91], [23.25, 87.89]
        ],
        story: [
          { time: '13:55 \u2022 FORMED', desc: 'Burdwan convective initiation', status: 'completed' },
          { time: '14:15 \u2022 DEVELOPING', desc: 'Cluster consolidating eastwards', status: 'completed' },
          { time: '14:34 \u2022 ADVECTION (NOW)', desc: 'Steady moderate precipitation band', status: 'active-now' },
          { time: '15:10 \u2022 PROJECTED PASSAGE', desc: 'Passing Ranaghat railway hub', status: 'pending' }
        ],
        changes: { dbz: '+3 dBZ', ltg: '+8%', temp: '\u2193 -1.8\u00b0C', area: '+5%' }
      },

      '031': {
        id: 'STORM CELL 031',
        badge: 'SEVERE',
        narrative: 'COASTAL SQUALL SEGMENT',
        dbz: '59 dBZ',
        speed: '52 km/h',
        direction: 'Moving northeast',
        arrival: '16–24 min',
        confidence: '89%',
        center: [21.80, 87.35],
        pulseStage: '● Severe (59 dBZ)',
        track: [
          [21.65, 87.05], [21.80, 87.30], [21.95, 87.55],
          [22.10, 87.80], [22.25, 88.05], [22.45, 88.40], [22.65, 88.75]
        ],
        lightnings: [
          [21.68, 87.10], [21.62, 87.02], [21.72, 87.18]
        ],
        story: [
          { time: '14:00 \u2022 FORMED', desc: 'Balasore coastal squall initiation', status: 'completed' },
          { time: '14:20 \u2022 BOWING', desc: 'Bow echo segment developing with strong gust front', status: 'completed' },
          { time: '14:34 \u2022 SEVERE (NOW)', desc: 'Approaching Digha coastal defense line', status: 'active-now' },
          { time: '15:00 \u2022 PROJECTED COASTAL CROSSING', desc: 'Haldia port & petrochem industrial zone', status: 'pending' }
        ],
        changes: { dbz: '+11 dBZ', ltg: '+34%', temp: '\u2193 -5.4\u00b0C', area: '+24%' }
      }
    };

    let activeStormId = '024';
    let currentStep = 2; // Default +30m
    let currentMode = 'forecast'; // 'observed' or 'forecast'
    let isImpactLensActive = false;
    let isPlaying = false;
    let playInterval = null;

    let map = null;
    let layerRadar = null;
    let layerSat = null;
    let layerLtg = null;
    let layerTracks = null;
    let layerImpact = null;
    let layerCities = null;

    /* ==========================================================================
       INITIALIZATION
       ========================================================================== */
    window.addEventListener('DOMContentLoaded', () => {
      initLivingMap();
      setupEventListeners();
      renderAtmosphere();
    });

    /* ==========================================================================
       MAP INITIALIZATION (HIGH RESOLUTION SATELLITE + GEOGRAPHIC HYBRID)
       ========================================================================== */
    function initLivingMap() {
      map = L.map('liveAtmosphericMap', {
        zoomControl: false,
        attributionControl: false,
        preferCanvas: true
      }).setView([22.65, 88.25], 8);

      L.control.zoom({ position: 'topright' }).addTo(map);

      // Photographic Satellite Basemap (Esri World Imagery)
      const esriSatellite = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
        maxZoom: 18,
        opacity: 0.88
      });

      // Subtle OpenStreetMap Roads / Borders Layer
      const osmOverlay = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 18,
        opacity: 0.32
      });

      esriSatellite.addTo(map);
      osmOverlay.addTo(map);

      layerRadar = L.layerGroup().addTo(map);
      layerSat = L.layerGroup().addTo(map);
      layerLtg = L.layerGroup().addTo(map);
      layerTracks = L.layerGroup().addTo(map);
      layerImpact = L.layerGroup().addTo(map);
      layerCities = L.layerGroup().addTo(map);

      // Regional City Geotags
      const cities = [
        { name: "Kolkata", lat: 22.5726, lon: 88.3639 },
        { name: "Howrah", lat: 22.5958, lon: 88.2636 },
        { name: "Kharagpur", lat: 22.3460, lon: 87.2320 },
        { name: "Burdwan", lat: 23.2324, lon: 87.8615 },
        { name: "Midnapore", lat: 22.4257, lon: 87.3199 },
        { name: "Durgapur", lat: 23.5204, lon: 87.3119 },
        { name: "Balasore", lat: 21.4934, lon: 86.9135 },
        { name: "Haldia", lat: 22.0667, lon: 88.0698 }
      ];

      cities.forEach(c => {
        const badge = L.divIcon({
          className: 'city-geotag-icon',
          html: `<div class="city-geotag-pill">${c.name}</div>`,
          iconSize: [60, 20],
          iconAnchor: [30, 10]
        });
        L.marker([c.lat, c.lon], { icon: badge, interactive: false }).addTo(layerCities);
      });
    }

    /* ==========================================================================
       ATMOSPHERIC VISUALIZATION ENGINE
       ========================================================================== */
    function renderAtmosphere() {
      layerRadar.clearLayers();
      layerLtg.clearLayers();
      layerTracks.clearLayers();
      layerImpact.clearLayers();

      const storm = STORM_REGISTRY[activeStormId];
      const track = storm.track;

      // 1. FORECAST FIELD (Soft, probabilistic diffusion broadening downwind)
      if (currentMode === 'forecast') {
        const p0 = track[0];
        const pTarget = track[currentStep] || track[track.length - 1];
        const spread = 0.08 + (currentStep * 0.06);

        // Soft outer uncertainty envelope
        const fieldPolygon = [
          [p0[0], p0[1]],
          [pTarget[0] + spread * 0.8, pTarget[1] - spread * 1.1],
          [pTarget[0] + spread * 1.2, pTarget[1] + spread * 1.1],
          [pTarget[0] - spread * 0.6, pTarget[1] + spread * 0.9],
          [p0[0], p0[1]]
        ];

        L.polygon(fieldPolygon, {
          color: '#a855f7',
          fillColor: '#a855f7',
          fillOpacity: 0.14,
          weight: 1.5,
          dashArray: '4, 6'
        }).addTo(layerTracks);
      }

      // 2. STORM TRAJECTORY (Smooth connecting path)
      L.polyline(track, {
        color: '#38bdf8',
        weight: 3,
        opacity: 0.9,
        dashArray: '6, 6'
      }).addTo(layerTracks);

      // 3. CURRENT STORM FOOTPRINT (Prominent, multi-ring Doppler dBZ cores)
      const t0 = track[0];

      // Outer precipitation footprint (35 dBZ)
      L.circle(t0, {
        radius: 22000,
        color: '#10b981',
        fillColor: '#10b981',
        fillOpacity: 0.28,
        weight: 1
      }).addTo(layerRadar);

      // Elevated convective band (50 dBZ)
      L.circle(t0, {
        radius: 13000,
        color: '#f97316',
        fillColor: '#f97316',
        fillOpacity: 0.5,
        weight: 1.5
      }).addTo(layerRadar);

      // Severe Hail Core (65+ dBZ)
      L.circle(t0, {
        radius: 6500,
        color: '#ef4444',
        fillColor: '#ef4444',
        fillOpacity: 0.8,
        weight: 2
      }).addTo(layerRadar);

      // 4. STORM SHADOWS (Progressively translucent future footprints fading downwind)
      if (currentMode === 'forecast') {
        const stepLabels = ['NOW', '+15m', '+30m', '+45m', '+60m', '+90m', '+120m'];

        for (let i = 1; i <= currentStep; i++) {
          const pt = track[i];
          if (!pt) continue;

          // Progressive translucency decay
          const opacity = Math.max(0.12, 0.48 - (i * 0.07));
          const shadowRadius = 18000 + (i * 2200);

          L.circle(pt, {
            radius: shadowRadius,
            color: '#f97316',
            fillColor: '#f97316',
            fillOpacity: opacity,
            weight: 1,
            dashArray: '3, 4'
          }).addTo(layerRadar);

          // Subtle waypoint node
          L.circleMarker(pt, {
            radius: 5,
            color: '#38bdf8',
            fillColor: '#070b14',
            fillOpacity: 1,
            weight: 2
          }).bindTooltip(`${stepLabels[i]} position (${storm.id})`, { permanent: false }).addTo(layerTracks);
        }
      }

      // 5. ACTIVE STORM CORE MARKER
      const activeCentroid = (currentMode === 'forecast' && currentStep > 0) ? track[currentStep] : t0;
      const coreIcon = L.divIcon({
        className: 'core-icon-wrap',
        html: `<div class="pulsing-storm-centroid" title="${storm.id}">${parseInt(storm.dbz)}</div>`,
        iconSize: [34, 34],
        iconAnchor: [17, 17]
      });
      L.marker(activeCentroid, { icon: coreIcon }).addTo(layerTracks);

      // 6. LIGHTNING DISCHARGES (Electric pulse density)
      storm.lightnings.forEach(lt => {
        const ltIcon = L.divIcon({
          className: 'lt-icon-wrap',
          html: '<div class="lightning-strobe-dot"></div>',
          iconSize: [14, 14],
          iconAnchor: [7, 7]
        });
        L.marker(lt, { icon: ltIcon }).addTo(layerLtg);
      });

      // 7. IMPACT LENS (Interactive Decision-Support Overlays)
      if (isImpactLensActive) {
        const criticalAssets = [
          { name: "VECC Kolkata Airport", pt: [22.654, 88.446], desc: "Runway approach crossing in 22 min" },
          { name: "NH-16 & NH-19 Highway Hub", pt: [22.48, 87.95], desc: "Direct squall crossing (75 km/h gusts)" },
          { name: "765kV Regional Substation", pt: [22.42, 87.35], desc: "High CG lightning strike corridor" }
        ];

        criticalAssets.forEach(asset => {
          // Warning Circle
          L.circle(asset.pt, {
            radius: 8000,
            color: '#fbbf24',
            fillColor: '#fbbf24',
            fillOpacity: 0.25,
            weight: 2
          }).addTo(layerImpact);

          // Impact Marker Tag
          const tag = L.divIcon({
            className: 'impact-tag-wrap',
            html: `<div class="impact-corridor-tag">⚠️ ${asset.name}</div>`,
            iconSize: [120, 24],
            iconAnchor: [60, 12]
          });
          L.marker(asset.pt, { icon: tag }).addTo(layerImpact)
            .bindPopup(`<strong>${asset.name}</strong><br>${asset.desc}`);
        });
      }
    }

    /* ==========================================================================
       SELECT STORM (INTERACTION & EDITORIAL UPDATE)
       ========================================================================== */
    function selectStorm(stormId) {
      activeStormId = stormId;
      const storm = STORM_REGISTRY[stormId];

      // Update storm cards in left rail
      document.querySelectorAll('.storm-card').forEach(c => c.classList.remove('selected'));
      const activeCard = document.getElementById(`stormSelect${stormId}`);
      if (activeCard) activeCard.classList.add('selected');

      // Update Right Editorial Panel
      document.getElementById('intelTitle').textContent = storm.id;
      document.getElementById('intelBadge').textContent = storm.badge;
      document.getElementById('intelNarrative').textContent = storm.narrative;

      document.getElementById('numDbz').textContent = storm.dbz;
      document.getElementById('numSpeed').textContent = storm.speed;
      document.getElementById('numDirection').textContent = storm.direction;
      document.getElementById('numArrival').textContent = storm.arrival;
      document.getElementById('numConfidence').textContent = storm.confidence;

      // Update Atmospheric Pulse
      document.getElementById('pulseStageCurrent').innerHTML = `<span>${storm.pulseStage}</span>`;

      // Update Storm Story Timeline
      const storyContainer = document.getElementById('storyTrackContainer');
      storyContainer.innerHTML = '';
      storm.story.forEach(node => {
        const item = document.createElement('div');
        item.className = `story-node-item ${node.status}`;
        item.innerHTML = `
          <span class="story-time-stamp">${node.time}</span>
          <span class="story-desc-text">${node.desc}</span>
        `;
        storyContainer.appendChild(item);
      });

      // Update Focus mode badge
      document.getElementById('btnFocusMode').innerHTML = `<span>🔍 FOCUS: CELL ${stormId}</span>`;

      // Fly map to storm centroid
      map.flyTo(storm.center, 8, { duration: 0.8 });

      // Re-render atmospheric features
      renderAtmosphere();
    }

    /* ==========================================================================
       TIME MACHINE & FORECAST STEPPING
       ========================================================================== */
    function setTimeStep(stepIdx) {
      currentStep = stepIdx;

      // Update Time Machine scrubber nodes
      document.querySelectorAll('.time-step-node').forEach((node, i) => {
        node.classList.toggle('active', i === stepIdx);
      });

      // Update Horizon Label
      const labels = ['NOW', '+15 MIN', '+30 MIN', '+45 MIN', '+60 MIN', '+90 MIN', '+120 MIN'];
      document.getElementById('horizonLabelDisplay').textContent = labels[stepIdx];

      // Update left horizon buttons
      const horizonBtns = document.querySelectorAll('.horizon-btn');
      horizonBtns.forEach((btn, i) => btn.classList.toggle('active', i === stepIdx));

      renderAtmosphere();
    }

    /* ==========================================================================
       EVENT LISTENERS & MICRO-INTERACTIONS
       ========================================================================== */
    function setupEventListeners() {
      // Horizon Buttons
      document.querySelectorAll('.horizon-btn').forEach(btn => {
        btn.addEventListener('click', () => {
          setTimeStep(parseInt(btn.dataset.step));
        });
      });

      // Time Machine Step Nodes
      document.querySelectorAll('.time-step-node').forEach(node => {
        node.addEventListener('click', () => {
          setTimeStep(parseInt(node.dataset.idx));
        });
      });

      // Play Evolution (The Signature 10-Second Wow Moment)
      const playBtn = document.getElementById('btnPlayEvolution');
      const playIcon = document.getElementById('playStateIcon');
      const playLabel = document.getElementById('playStateLabel');

      playBtn.addEventListener('click', () => {
        isPlaying = !isPlaying;
        if (isPlaying) {
          playIcon.textContent = '⏸';
          playLabel.textContent = 'PAUSE EVOLUTION';
          playInterval = setInterval(() => {
            let next = (currentStep + 1) % 7;
            setTimeStep(next);
          }, 1600);
        } else {
          playIcon.textContent = '▶';
          playLabel.textContent = 'PLAY EVOLUTION';
          clearInterval(playInterval);
        }
      });

      // Observed vs Forecast Mode Tabs
      document.getElementById('tabModeObserved').addEventListener('click', () => {
        currentMode = 'observed';
        document.getElementById('tabModeObserved').classList.add('active');
        document.getElementById('tabModeForecast').classList.remove('active');
        renderAtmosphere();
      });

      document.getElementById('tabModeForecast').addEventListener('click', () => {
        currentMode = 'forecast';
        document.getElementById('tabModeForecast').classList.add('active');
        document.getElementById('tabModeObserved').classList.remove('active');
        renderAtmosphere();
      });

      // Impact Lens Toggle
      const impactBtn = document.getElementById('btnImpactLens');
      impactBtn.addEventListener('click', () => {
        isImpactLensActive = !isImpactLensActive;
        impactBtn.classList.toggle('active', isImpactLensActive);
        renderAtmosphere();
      });

      // Focus Mode Button
      document.getElementById('btnFocusMode').addEventListener('click', () => {
        const storm = STORM_REGISTRY[activeStormId];
        map.flyTo(storm.center, 10, { duration: 1.2 });
      });

      // Situation View Overlay
      document.getElementById('btnSwitchSituation').addEventListener('click', () => {
        document.getElementById('situationOverlay').classList.add('active');
        document.getElementById('btnSwitchSituation').classList.add('active');
        document.getElementById('btnSwitchMap').classList.remove('active');
      });

      document.getElementById('btnSwitchMap').addEventListener('click', () => {
        document.getElementById('situationOverlay').classList.remove('active');
        document.getElementById('btnSwitchMap').classList.add('active');
        document.getElementById('btnSwitchSituation').classList.remove('active');
      });

      document.getElementById('btnCloseSituation').addEventListener('click', () => {
        document.getElementById('situationOverlay').classList.remove('active');
        document.getElementById('btnSwitchMap').classList.add('active');
        document.getElementById('btnSwitchSituation').classList.remove('active');
      });

      // Data Health Tray Modal
      const healthModal = document.getElementById('dataHealthModal');
      document.getElementById('btnToggleDataHealth').addEventListener('click', () => {
        healthModal.classList.toggle('active');
      });
      document.getElementById('btnCloseHealth').addEventListener('click', () => {
        healthModal.classList.remove('active');
      });

      // Layer Toggles
      const bindLayerCard = (id, layer) => {
        const el = document.getElementById(id);
        el.addEventListener('click', () => {
          el.classList.toggle('active');
          if (el.classList.contains('active')) map.addLayer(layer);
          else map.removeLayer(layer);
        });
      };

      bindLayerCard('cardLayerRadar', layerRadar);
      bindLayerCard('cardLayerSat', layerSat);
      bindLayerCard('cardLayerLtg', layerLtg);
      bindLayerCard('cardLayerTracks', layerTracks);

      // Doppler Beam Scan Toggle
      const sweepCard = document.getElementById('cardLayerSweep');
      const sweepOverlay = document.getElementById('radarBeamScan');
      sweepCard.addEventListener('click', () => {
        sweepCard.classList.toggle('active');
        sweepOverlay.classList.toggle('active', sweepCard.classList.contains('active'));
      });
    }
  </script>
</body>
</html>
'''

with open("dashboard/index.html", "w", encoding="utf-8") as f:
    f.write(code)

print(f"Successfully generated Product-Level VAJRA Evolution: {len(code)} bytes")
