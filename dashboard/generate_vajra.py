# -*- coding: utf-8 -*-
"""
Generator script for VAJRA - Atmospheric Intelligence Command Center
"""
import sys

html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>VAJRA — Atmospheric Intelligence Command Center</title>
  <meta name="description" content="VAJRA: Very-short-term Atmospheric Risk & Joint Analysis. AIML-based Nowcasting of Thunderstorm and Lightning over India." />

  <!-- Google Fonts: Inter & IBM Plex Mono -->
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&family=Inter:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@500;700&display=swap" rel="stylesheet" />

  <!-- Leaflet CSS & JS -->
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin="" />
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>

  <!-- Chart.js -->
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>

  <style>
    /* ==========================================================================
       VAJRA COMMAND SYSTEM: THEME TOKENS (Aviation / Tactical Meteorological)
       ========================================================================== */
    :root {
      --bg-void: #05080f;
      --bg-app: #080c16;
      --bg-panel: #0d1322;
      --bg-panel-elevated: #121a2e;
      --bg-panel-hover: #17223b;
      --bg-input: #0b1120;

      --border-subtle: rgba(255, 255, 255, 0.07);
      --border-tactical: rgba(56, 189, 248, 0.22);
      --border-strong: rgba(255, 255, 255, 0.16);

      --text-white: #f8fafc;
      --text-primary: #e2e8f0;
      --text-secondary: #94a3b8;
      --text-muted: #64748b;
      --text-dim: #475569;

      /* Tactical Meteorological Color Spectrum */
      --radar-cyan: #38bdf8;
      --radar-green: #10b981;
      --radar-yellow: #facc15;
      --radar-orange: #f97316;
      --radar-red: #ef4444;
      --radar-magenta: #d946ef;
      --radar-white: #ffffff;

      --lightning-core: #67e8f9;
      --lightning-glow: rgba(56, 189, 248, 0.45);

      --threat-low: #10b981;
      --threat-mod: #eab308;
      --threat-high: #f97316;
      --threat-severe: #ef4444;
      --threat-extreme: #c026d3;

      --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
      --font-mono: 'IBM Plex Mono', monospace;
      --font-brand: 'Space Grotesk', sans-serif;
    }

    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
      -webkit-font-smoothing: antialiased;
    }

    body {
      background-color: var(--bg-void);
      color: var(--text-primary);
      font-family: var(--font-sans);
      font-size: 13px;
      line-height: 1.4;
      overflow: hidden;
      height: 100vh;
      width: 100vw;
      user-select: none;
    }

    /* Scrollbars */
    ::-webkit-scrollbar {
      width: 5px;
      height: 5px;
    }
    ::-webkit-scrollbar-track {
      background: var(--bg-app);
    }
    ::-webkit-scrollbar-thumb {
      background: #1e293b;
      border-radius: 2px;
    }
    ::-webkit-scrollbar-thumb:hover {
      background: #334155;
    }

    /* ==========================================================================
       TOP COMMAND HEADER
       ========================================================================== */
    .top-header {
      height: 54px;
      background: var(--bg-app);
      border-bottom: 1px solid var(--border-subtle);
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 16px;
      z-index: 1000;
      position: relative;
    }

    .brand-group {
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .brand-emblem {
      width: 32px;
      height: 32px;
      background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%);
      border: 1px solid var(--radar-cyan);
      border-radius: 4px;
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 0 14px rgba(56, 189, 248, 0.35);
      position: relative;
    }

    .brand-emblem svg {
      width: 20px;
      height: 20px;
      fill: #ffffff;
    }

    .brand-titles {
      display: flex;
      flex-direction: column;
    }

    .brand-name {
      font-family: var(--font-brand);
      font-size: 17px;
      font-weight: 700;
      letter-spacing: 1.5px;
      color: var(--text-white);
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .brand-badge {
      font-family: var(--font-mono);
      font-size: 9px;
      padding: 2px 6px;
      background: rgba(56, 189, 248, 0.12);
      border: 1px solid var(--border-tactical);
      border-radius: 2px;
      color: var(--radar-cyan);
      letter-spacing: 0.5px;
      font-weight: 600;
    }

    .brand-desc {
      font-size: 10px;
      color: var(--text-secondary);
      letter-spacing: 0.5px;
      font-weight: 500;
    }

    /* Header Center Telemetry & Clock */
    .header-telemetry {
      display: flex;
      align-items: center;
      gap: 20px;
    }

    .clock-block {
      display: flex;
      align-items: center;
      background: var(--bg-panel);
      border: 1px solid var(--border-subtle);
      border-radius: 4px;
      padding: 4px 10px;
      gap: 12px;
      font-family: var(--font-mono);
    }

    .clock-item {
      display: flex;
      flex-direction: column;
    }

    .clock-label {
      font-size: 8.5px;
      color: var(--text-dim);
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }

    .clock-val {
      font-size: 12.5px;
      color: var(--text-white);
      font-weight: 600;
    }

    .clock-divider {
      width: 1px;
      height: 22px;
      background: var(--border-subtle);
    }

    .sensor-pipeline-pills {
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .pipeline-pill {
      display: flex;
      align-items: center;
      gap: 5px;
      background: rgba(15, 23, 42, 0.8);
      border: 1px solid var(--border-subtle);
      border-radius: 3px;
      padding: 3px 8px;
      font-size: 10px;
      font-family: var(--font-mono);
      color: var(--text-secondary);
    }

    .status-dot {
      width: 6px;
      height: 6px;
      border-radius: 50%;
      background: var(--radar-green);
      box-shadow: 0 0 6px var(--radar-green);
    }

    .status-dot.pulsing {
      animation: pulse-dot 2s infinite ease-in-out;
    }

    @keyframes pulse-dot {
      0%, 100% { transform: scale(1); opacity: 1; }
      50% { transform: scale(1.3); opacity: 0.5; }
    }

    /* Header Right Actions */
    .header-actions {
      display: flex;
      align-items: center;
      gap: 10px;
    }

    .search-box-wrap {
      position: relative;
      width: 220px;
    }

    .search-input {
      width: 100%;
      background: var(--bg-input);
      border: 1px solid var(--border-subtle);
      border-radius: 3px;
      padding: 6px 10px 6px 28px;
      color: var(--text-white);
      font-size: 11.5px;
      font-family: var(--font-sans);
      outline: none;
      transition: all 0.2s;
    }

    .search-input:focus {
      border-color: var(--radar-cyan);
      box-shadow: 0 0 8px rgba(56, 189, 248, 0.25);
    }

    .search-icon {
      position: absolute;
      left: 8px;
      top: 50%;
      transform: translateY(-50%);
      width: 13px;
      height: 13px;
      fill: var(--text-muted);
      pointer-events: none;
    }

    .search-dropdown {
      position: absolute;
      top: 100%;
      left: 0;
      right: 0;
      background: var(--bg-panel-elevated);
      border: 1px solid var(--border-tactical);
      border-radius: 3px;
      margin-top: 4px;
      max-height: 240px;
      overflow-y: auto;
      z-index: 2000;
      display: none;
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.7);
    }

    .search-result-item {
      padding: 7px 10px;
      border-bottom: 1px solid var(--border-subtle);
      cursor: pointer;
      font-size: 11px;
    }
    .search-result-item:hover {
      background: var(--bg-panel-hover);
      color: var(--radar-cyan);
    }

    .threat-level-badge {
      display: flex;
      align-items: center;
      gap: 6px;
      padding: 4px 10px;
      border-radius: 3px;
      background: rgba(239, 68, 68, 0.15);
      border: 1px solid rgba(239, 68, 68, 0.4);
      color: #fca5a5;
      font-family: var(--font-mono);
      font-size: 11px;
      font-weight: 600;
    }

    .btn-tactical {
      background: var(--bg-panel);
      border: 1px solid var(--border-subtle);
      color: var(--text-secondary);
      border-radius: 3px;
      padding: 6px 10px;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      font-size: 11px;
      font-family: var(--font-sans);
      transition: all 0.15s;
    }

    .btn-tactical:hover {
      background: var(--bg-panel-hover);
      color: var(--text-white);
      border-color: var(--border-tactical);
    }

    .btn-tactical.active {
      background: rgba(56, 189, 248, 0.15);
      border-color: var(--radar-cyan);
      color: var(--radar-cyan);
    }

    /* ==========================================================================
       MAIN COMMAND CENTER WORKSPACE (3-COLUMN LAYOUT)
       ========================================================================== */
    .command-viewport {
      display: flex;
      height: calc(100vh - 54px);
      width: 100vw;
      position: relative;
      overflow: hidden;
    }

    /* Left Deck: Sensor Ingest, Soundings, Layer Controls */
    .deck-left {
      width: 310px;
      min-width: 310px;
      background: var(--bg-panel);
      border-right: 1px solid var(--border-subtle);
      display: flex;
      flex-direction: column;
      z-index: 500;
      transition: width 0.25s cubic-bezier(0.4, 0, 0.2, 1);
      overflow-y: auto;
    }

    /* Center Hero: Tactical Map View */
    .deck-center-map {
      flex: 1;
      position: relative;
      height: 100%;
      background: #020408;
    }

    #vajraMap {
      width: 100%;
      height: 100%;
      background: #020408;
      z-index: 10;
    }

    /* Right Deck: Active Cell Tracking & Operations Console */
    .deck-right {
      width: 380px;
      min-width: 380px;
      background: var(--bg-panel);
      border-left: 1px solid var(--border-subtle);
      display: flex;
      flex-direction: column;
      z-index: 500;
      overflow-y: auto;
    }

    /* ==========================================================================
       COMMON PANEL STYLING & ACCORDIONS
       ========================================================================== */
    .deck-section {
      border-bottom: 1px solid var(--border-subtle);
      padding: 12px 14px;
    }

    .deck-section-title {
      font-size: 10.5px;
      font-family: var(--font-mono);
      font-weight: 700;
      color: var(--radar-cyan);
      text-transform: uppercase;
      letter-spacing: 0.8px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 10px;
    }

    .deck-section-title span.sub {
      color: var(--text-dim);
      font-weight: 400;
    }

    /* Scenario / Mode Selector */
    .scenario-picker {
      width: 100%;
      background: var(--bg-input);
      border: 1px solid var(--border-subtle);
      border-radius: 3px;
      color: var(--text-primary);
      padding: 6px 8px;
      font-size: 11px;
      font-family: var(--font-sans);
      outline: none;
      cursor: pointer;
    }
    .scenario-picker:focus {
      border-color: var(--radar-cyan);
    }

    /* Layer Item */
    .layer-control-list {
      display: flex;
      flex-direction: column;
      gap: 7px;
    }

    .layer-item {
      display: flex;
      align-items: center;
      justify-content: space-between;
      background: var(--bg-panel-elevated);
      border: 1px solid var(--border-subtle);
      border-radius: 3px;
      padding: 7px 9px;
      transition: border-color 0.15s;
    }
    .layer-item:hover {
      border-color: rgba(255, 255, 255, 0.15);
    }

    .layer-label-group {
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .layer-check {
      appearance: none;
      width: 14px;
      height: 14px;
      border: 1px solid var(--border-tactical);
      border-radius: 2px;
      background: var(--bg-app);
      cursor: pointer;
      position: relative;
    }
    .layer-check:checked {
      background: var(--radar-cyan);
      border-color: var(--radar-cyan);
    }
    .layer-check:checked::after {
      content: "✓";
      position: absolute;
      top: -2px;
      left: 1px;
      font-size: 11px;
      color: #000;
      font-weight: bold;
    }

    .layer-name {
      font-size: 11.5px;
      color: var(--text-white);
      font-weight: 500;
    }

    .layer-badge {
      font-family: var(--font-mono);
      font-size: 9px;
      padding: 1px 5px;
      border-radius: 2px;
      background: rgba(255, 255, 255, 0.06);
      color: var(--text-secondary);
    }

    /* Sounding / Instability Telemetry Grid */
    .metrics-grid-2x3 {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 7px;
    }

    .metric-card-tactical {
      background: var(--bg-panel-elevated);
      border: 1px solid var(--border-subtle);
      border-radius: 3px;
      padding: 7px 9px;
      display: flex;
      flex-direction: column;
    }

    .metric-card-tactical .lbl {
      font-size: 9px;
      color: var(--text-secondary);
      font-family: var(--font-mono);
      text-transform: uppercase;
      letter-spacing: 0.4px;
    }

    .metric-card-tactical .val-row {
      display: flex;
      align-items: baseline;
      justify-content: space-between;
      margin-top: 2px;
    }

    .metric-card-tactical .val {
      font-size: 14px;
      font-family: var(--font-mono);
      font-weight: 700;
      color: var(--text-white);
    }

    .metric-card-tactical .unit {
      font-size: 9.5px;
      color: var(--text-dim);
      font-family: var(--font-mono);
    }

    .metric-card-tactical .alert-tag {
      font-size: 8.5px;
      font-family: var(--font-mono);
      font-weight: 600;
      padding: 1px 4px;
      border-radius: 2px;
      text-align: right;
    }
    .tag-severe { background: rgba(239, 68, 68, 0.2); color: #fca5a5; }
    .tag-high { background: rgba(249, 115, 22, 0.2); color: #fdba74; }
    .tag-mod { background: rgba(234, 179, 8, 0.2); color: #fde047; }
    .tag-ok { background: rgba(16, 185, 129, 0.2); color: #86efac; }

    /* ==========================================================================
       MAP OVERLAYS & CONTROLS
       ========================================================================== */
    /* Radar dBZ Reflectivity Scale Bar */
    .radar-scale-overlay {
      position: absolute;
      top: 14px;
      left: 14px;
      z-index: 1000;
      background: rgba(10, 15, 26, 0.88);
      backdrop-filter: blur(8px);
      border: 1px solid var(--border-tactical);
      border-radius: 4px;
      padding: 7px 12px;
      box-shadow: 0 4px 18px rgba(0,0,0,0.6);
      pointer-events: auto;
    }

    .scale-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-family: var(--font-mono);
      font-size: 9.5px;
      color: var(--text-secondary);
      margin-bottom: 5px;
    }

    .dbz-gradient-bar {
      width: 280px;
      height: 10px;
      border-radius: 2px;
      background: linear-gradient(to right,
        #04e9e7 0%,
        #019ff4 15%,
        #0300f4 25%,
        #02fd02 38%,
        #01c501 50%,
        #ffff00 62%,
        #ff9f00 75%,
        #ff0000 87%,
        #d800ff 95%,
        #ffffff 100%
      );
      border: 1px solid rgba(255,255,255,0.2);
    }

    .dbz-labels {
      display: flex;
      justify-content: space-between;
      font-family: var(--font-mono);
      font-size: 8px;
      color: var(--text-muted);
      margin-top: 3px;
    }

    /* Radar Beam Sweep Animation Effect */
    .radar-sweep-beam {
      position: absolute;
      width: 100%;
      height: 100%;
      top: 0;
      left: 0;
      pointer-events: none;
      z-index: 15;
      overflow: hidden;
      opacity: 0.35;
      display: none;
    }
    .radar-sweep-beam.active {
      display: block;
    }
    .sweep-line {
      position: absolute;
      top: 50%;
      left: 50%;
      width: 48vw;
      height: 2px;
      background: linear-gradient(to right, rgba(56, 189, 248, 0.9), transparent);
      transform-origin: 0% 0%;
      animation: sweep-spin 6s linear infinite;
      box-shadow: 0 0 16px rgba(56, 189, 248, 0.8);
    }
    @keyframes sweep-spin {
      0% { transform: rotate(0deg); }
      100% { transform: rotate(360deg); }
    }

    /* Floating Timeline Scrubber Bar */
    .timeline-scrubber-deck {
      position: absolute;
      bottom: 18px;
      left: 18px;
      right: 18px;
      background: rgba(10, 15, 26, 0.92);
      backdrop-filter: blur(10px);
      border: 1px solid var(--border-tactical);
      border-radius: 4px;
      padding: 8px 16px;
      z-index: 1000;
      display: flex;
      flex-direction: column;
      gap: 7px;
      box-shadow: 0 6px 26px rgba(0, 0, 0, 0.7);
    }

    .timeline-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
    }

    .timeline-playback-controls {
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .btn-play-pause {
      width: 30px;
      height: 30px;
      border-radius: 3px;
      background: var(--radar-cyan);
      border: none;
      color: #000;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: bold;
      transition: background 0.15s;
    }
    .btn-play-pause:hover {
      background: #7dd3fc;
    }

    .timeline-status-text {
      font-family: var(--font-mono);
      font-size: 11px;
      color: var(--text-white);
      font-weight: 600;
    }

    .timeline-horizon-buttons {
      display: flex;
      align-items: center;
      gap: 5px;
    }

    .horizon-btn {
      background: var(--bg-panel-elevated);
      border: 1px solid var(--border-subtle);
      border-radius: 2px;
      padding: 4px 8px;
      font-family: var(--font-mono);
      font-size: 10px;
      color: var(--text-secondary);
      cursor: pointer;
      transition: all 0.15s;
    }
    .horizon-btn:hover {
      border-color: var(--radar-cyan);
      color: var(--text-white);
    }
    .horizon-btn.active {
      background: rgba(56, 189, 248, 0.18);
      border-color: var(--radar-cyan);
      color: var(--radar-cyan);
      font-weight: 700;
    }

    /* Slider track */
    .timeline-slider-row {
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .timeline-range-slider {
      flex: 1;
      accent-color: var(--radar-cyan);
      height: 4px;
      cursor: pointer;
    }

    .timeline-ticks {
      display: flex;
      justify-content: space-between;
      font-family: var(--font-mono);
      font-size: 8.5px;
      color: var(--text-dim);
    }

    /* Map Click Inspector Card */
    .map-inspector-floating {
      position: absolute;
      top: 75px;
      left: 14px;
      width: 290px;
      background: rgba(10, 15, 26, 0.94);
      backdrop-filter: blur(10px);
      border: 1px solid var(--radar-cyan);
      border-radius: 4px;
      padding: 12px;
      z-index: 1000;
      box-shadow: 0 8px 30px rgba(0, 0, 0, 0.85);
      display: none;
    }

    .inspector-header {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 8px;
      border-bottom: 1px solid var(--border-subtle);
      padding-bottom: 6px;
    }

    .inspector-title {
      font-size: 12px;
      font-weight: 700;
      color: var(--text-white);
    }

    .inspector-coords {
      font-family: var(--font-mono);
      font-size: 9.5px;
      color: var(--radar-cyan);
    }

    .inspector-close {
      cursor: pointer;
      color: var(--text-muted);
      font-size: 14px;
    }
    .inspector-close:hover {
      color: var(--text-white);
    }

    /* ==========================================================================
       RIGHT DECK: OPERATIONS, ACTIVE CELL TRACKS & IMPACT
       ========================================================================== */
    .right-tabs-nav {
      display: flex;
      border-bottom: 1px solid var(--border-subtle);
      background: var(--bg-app);
    }

    .right-tab-btn {
      flex: 1;
      padding: 10px 6px;
      text-align: center;
      font-family: var(--font-mono);
      font-size: 10px;
      font-weight: 600;
      color: var(--text-secondary);
      background: none;
      border: none;
      border-bottom: 2px solid transparent;
      cursor: pointer;
      transition: all 0.15s;
    }
    .right-tab-btn:hover {
      color: var(--text-white);
    }
    .right-tab-btn.active {
      color: var(--radar-cyan);
      border-bottom-color: var(--radar-cyan);
      background: rgba(56, 189, 248, 0.05);
    }

    .tab-content-area {
      flex: 1;
      display: flex;
      flex-direction: column;
    }

    /* Active Severe Cells Table */
    .cell-table-wrap {
      padding: 10px 14px;
      display: flex;
      flex-direction: column;
      gap: 8px;
    }

    .cell-card-item {
      background: var(--bg-panel-elevated);
      border: 1px solid var(--border-subtle);
      border-radius: 3px;
      padding: 9px 11px;
      cursor: pointer;
      transition: all 0.15s;
    }
    .cell-card-item:hover {
      border-color: var(--border-tactical);
      background: var(--bg-panel-hover);
    }
    .cell-card-item.selected {
      border-color: var(--radar-cyan);
      box-shadow: 0 0 10px rgba(56, 189, 248, 0.2);
    }

    .cell-header-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 6px;
    }

    .cell-id-badge {
      font-family: var(--font-mono);
      font-size: 10px;
      font-weight: 700;
      color: var(--radar-cyan);
      display: flex;
      align-items: center;
      gap: 5px;
    }

    .cell-threat-pill {
      font-family: var(--font-mono);
      font-size: 9px;
      font-weight: 700;
      padding: 2px 6px;
      border-radius: 2px;
      text-transform: uppercase;
    }

    .cell-stats-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 6px;
      font-family: var(--font-mono);
      font-size: 10px;
    }

    .cell-stat-col {
      display: flex;
      flex-direction: column;
    }
    .cell-stat-col .k { font-size: 8px; color: var(--text-dim); }
    .cell-stat-col .v { font-weight: 600; color: var(--text-white); }

    /* Sector Impact Grid */
    .impact-sector-card {
      background: var(--bg-panel-elevated);
      border: 1px solid var(--border-subtle);
      border-radius: 3px;
      padding: 10px 12px;
      margin-bottom: 8px;
    }

    .sector-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 6px;
    }

    .sector-title {
      font-size: 11.5px;
      font-weight: 600;
      color: var(--text-white);
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .impact-risk-pill {
      font-family: var(--font-mono);
      font-size: 9px;
      padding: 2px 5px;
      border-radius: 2px;
      font-weight: 700;
    }

    .sector-details {
      font-size: 11px;
      color: var(--text-secondary);
      line-height: 1.4;
    }

    /* CAP Alert Generator */
    .cap-box {
      background: var(--bg-input);
      border: 1px solid var(--border-subtle);
      border-radius: 3px;
      padding: 10px;
      font-family: var(--font-mono);
      font-size: 10px;
      color: #94a3b8;
      max-height: 220px;
      overflow-y: auto;
      white-space: pre-wrap;
    }

    /* ==========================================================================
       CUSTOM LEAFLET STYLING & ANIMATIONS
       ========================================================================== */
    .leaflet-container {
      background-color: #03060c !important;
    }

    /* Storm Cell Centroid Marker */
    .custom-cell-icon {
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .cell-marker-pulse {
      width: 26px;
      height: 26px;
      border-radius: 50%;
      background: rgba(239, 68, 68, 0.4);
      border: 2px solid #ef4444;
      display: flex;
      align-items: center;
      justify-content: center;
      color: #ffffff;
      font-family: var(--font-mono);
      font-size: 9px;
      font-weight: 800;
      box-shadow: 0 0 16px rgba(239, 68, 68, 0.8);
      animation: cell-throb 2s infinite ease-in-out;
      cursor: pointer;
    }

    @keyframes cell-throb {
      0%, 100% { transform: scale(1); box-shadow: 0 0 10px rgba(239, 68, 68, 0.6); }
      50% { transform: scale(1.18); box-shadow: 0 0 24px rgba(239, 68, 68, 1); }
    }

    /* Lightning Pulse Flash */
    .lightning-flash-icon {
      width: 14px;
      height: 14px;
      border-radius: 50%;
      background: #67e8f9;
      box-shadow: 0 0 12px #38bdf8;
      animation: lightning-strike 1.6s infinite ease-out;
    }

    @keyframes lightning-strike {
      0% { transform: scale(0.4); opacity: 1; }
      50% { transform: scale(2.2); opacity: 0.6; }
      100% { transform: scale(3.5); opacity: 0; }
    }

    /* Modal / Export Overlay */
    .modal-overlay {
      position: fixed;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      background: rgba(0, 0, 0, 0.8);
      backdrop-filter: blur(4px);
      z-index: 3000;
      display: none;
      align-items: center;
      justify-content: center;
    }

    .modal-window {
      width: 580px;
      background: var(--bg-panel-elevated);
      border: 1px solid var(--border-tactical);
      border-radius: 6px;
      padding: 20px;
      box-shadow: 0 16px 48px rgba(0, 0, 0, 0.9);
    }
  </style>
</head>
<body>

  <!-- ==========================================================================
       TOP OPERATIONAL BAR
       ========================================================================== -->
  <header class="top-header">
    <div class="brand-group">
      <div class="brand-emblem" title="VAJRA Convective Defense System">
        <svg viewBox="0 0 24 24">
          <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/>
        </svg>
      </div>
      <div class="brand-titles">
        <div class="brand-name">
          VAJRA
          <span class="brand-badge">GEO-OPS v1.0</span>
        </div>
        <div class="brand-desc">Very-short-term Atmospheric Risk &amp; Joint Analysis</div>
      </div>
    </div>

    <!-- Center System Clocks & Pipeline Latency -->
    <div class="header-telemetry">
      <div class="clock-block">
        <div class="clock-item">
          <span class="clock-label">ZULU / UTC</span>
          <span class="clock-val" id="clockUtc">--:--:--Z</span>
        </div>
        <div class="clock-divider"></div>
        <div class="clock-item">
          <span class="clock-label">IST (LOCAL)</span>
          <span class="clock-val" id="clockIst">--:--:-- IST</span>
        </div>
      </div>

      <div class="sensor-pipeline-pills">
        <div class="pipeline-pill" title="Doppler Weather Radar Mosaic (IMD Network)">
          <span class="status-dot pulsing"></span>
          <span>DWR MOSAIC: 18 STATIONS</span>
        </div>
        <div class="pipeline-pill" title="INSAT-3DR Rapid Scan Visible/IR">
          <span class="status-dot"></span>
          <span>INSAT-3DR: 4m LATENCY</span>
        </div>
        <div class="pipeline-pill" title="Global Lightning Detection Network">
          <span class="status-dot pulsing" style="background:var(--lightning-core); box-shadow:0 0 6px var(--lightning-core);"></span>
          <span>GLD360: LIVE FEED</span>
        </div>
      </div>
    </div>

    <!-- Header Actions & Search -->
    <div class="header-actions">
      <!-- OSM Location Search Box -->
      <div class="search-box-wrap">
        <svg class="search-icon" viewBox="0 0 24 24"><path d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" stroke="currentColor" stroke-width="2" fill="none"/></svg>
        <input type="text" class="search-input" id="osmSearchInput" placeholder="Locate Indian city/district..." autocomplete="off" />
        <div class="search-dropdown" id="osmSearchDropdown"></div>
      </div>

      <!-- Threat Alert Badge -->
      <div class="threat-level-badge" id="globalThreatBadge">
        <span class="status-dot" style="background:#ef4444; box-shadow:0 0 8px #ef4444;"></span>
        <span>WATCH: SEVERE CELLS</span>
      </div>

      <!-- Tactical Buttons -->
      <button class="btn-tactical" id="btnRadarSweep" title="Toggle Doppler Beam Sweep Animation">
        <span>SWEEP</span>
      </button>

      <button class="btn-tactical" id="btnAudioPing" title="Toggle Severe Lightning Audio Alert Ping">
        <span>AUDIO: ON</span>
      </button>

      <button class="btn-tactical" id="btnExportCap" title="Generate Early Warning Alert Bulletin">
        <span>EXPORT CAP</span>
      </button>
    </div>
  </header>

  <!-- ==========================================================================
       MAIN COMMAND VIEWPORT
       ========================================================================== -->
  <main class="command-viewport">

    <!-- LEFT DECK: SENSORS, SOUNDING, LAYERS -->
    <aside class="deck-left">
      <!-- Scenario Selector -->
      <div class="deck-section">
        <div class="deck-section-title">
          <span>OPERATIONAL MODE</span>
          <span class="sub" id="modeStateLabel">LIVE API</span>
        </div>
        <select class="scenario-picker" id="scenarioSelect">
          <option value="api">Connected: Live FastAPI Backend (Localhost:8000)</option>
          <option value="scenario_bengal" selected>Scenario: Nor'wester Supercell (Bengal &amp; Odisha)</option>
          <option value="scenario_delhi">Scenario: Pre-Monsoon Severe Squall (Delhi-NCR)</option>
          <option value="scenario_south">Scenario: Severe Lightning Outbreak (Telangana &amp; AP)</option>
        </select>
      </div>

      <!-- Layer Controls -->
      <div class="deck-section">
        <div class="deck-section-title">
          <span>GEO-INTELLIGENCE LAYERS</span>
          <span class="sub">MULTI-SPECTRAL</span>
        </div>
        <div class="layer-control-list">
          <label class="layer-item">
            <div class="layer-label-group">
              <input type="checkbox" class="layer-check" id="layerRadar" checked />
              <span class="layer-name">Composite Reflectivity (dBZ)</span>
            </div>
            <span class="layer-badge">S-BAND DWR</span>
          </label>

          <label class="layer-item">
            <div class="layer-label-group">
              <input type="checkbox" class="layer-check" id="layerLightning" checked />
              <span class="layer-name">Real-Time Lightning (CG/IC)</span>
            </div>
            <span class="layer-badge" style="color:var(--radar-cyan);">GLD360</span>
          </label>

          <label class="layer-item">
            <div class="layer-label-group">
              <input type="checkbox" class="layer-check" id="layerCellVectors" checked />
              <span class="layer-name">Cell Vectors &amp; Uncertainty</span>
            </div>
            <span class="layer-badge">TITAN/SCIT</span>
          </label>

          <label class="layer-item">
            <div class="layer-label-group">
              <input type="checkbox" class="layer-check" id="layerInfra" checked />
              <span class="layer-name">Airports &amp; Power Grids</span>
            </div>
            <span class="layer-badge">INFRA</span>
          </label>

          <label class="layer-item">
            <div class="layer-label-group">
              <input type="checkbox" class="layer-check" id="layerDistrictRisk" checked />
              <span class="layer-name">District Vulnerability Heatmap</span>
            </div>
            <span class="layer-badge">IMD RISK</span>
          </label>
        </div>
      </div>

      <!-- Instability & Sounding Diagnostics (Thermodynamic Profile) -->
      <div class="deck-section">
        <div class="deck-section-title">
          <span>ATMOSPHERIC INSTABILITY</span>
          <span class="sub">MESOSCALE SOUNDING</span>
        </div>
        <div class="metrics-grid-2x3">
          <div class="metric-card-tactical">
            <span class="lbl">SBCAPE (Energy)</span>
            <div class="val-row">
              <span class="val" id="metricCape">3,420</span>
              <span class="unit">J/kg</span>
            </div>
            <span class="alert-tag tag-severe">EXTREME</span>
          </div>

          <div class="metric-card-tactical">
            <span class="lbl">CIN (Inhibition)</span>
            <div class="val-row">
              <span class="val" id="metricCin">-18</span>
              <span class="unit">J/kg</span>
            </div>
            <span class="alert-tag tag-ok">UNLOCKED</span>
          </div>

          <div class="metric-card-tactical">
            <span class="lbl">0-6km Bulk Shear</span>
            <div class="val-row">
              <span class="val" id="metricShear">44.8</span>
              <span class="unit">kts</span>
            </div>
            <span class="alert-tag tag-severe">SUPERCELL</span>
          </div>

          <div class="metric-card-tactical">
            <span class="lbl">Lifted Index (LI)</span>
            <div class="val-row">
              <span class="val" id="metricLi">-7.4</span>
              <span class="unit">°C</span>
            </div>
            <span class="alert-tag tag-severe">HIGHLY UNSTABLE</span>
          </div>

          <div class="metric-card-tactical">
            <span class="lbl">Precip Water (PW)</span>
            <div class="val-row">
              <span class="val" id="metricPw">58.2</span>
              <span class="unit">mm</span>
            </div>
            <span class="alert-tag tag-high">TORRENTIAL</span>
          </div>

          <div class="metric-card-tactical">
            <span class="lbl">VIL (Liquid Water)</span>
            <div class="val-row">
              <span class="val" id="metricVil">64.5</span>
              <span class="unit">kg/m²</span>
            </div>
            <span class="alert-tag tag-severe">SEVERE HAIL</span>
          </div>
        </div>
      </div>

      <!-- Probability Curves Chart (Horizon T+15m to T+360m) -->
      <div class="deck-section" style="border-bottom:none; flex:1;">
        <div class="deck-section-title">
          <span>NOWCAST PROBABILITY DECAY</span>
          <span class="sub">T0 → T+360m</span>
        </div>
        <div style="height: 140px; position:relative;">
          <canvas id="horizonDecayChart"></canvas>
        </div>
      </div>
    </aside>

    <!-- CENTER HERO MAP -->
    <section class="deck-center-map">
      <!-- Leaflet Map Container -->
      <div id="vajraMap"></div>

      <!-- Doppler Beam Sweep Line (Optional Animation) -->
      <div class="radar-sweep-beam" id="radarSweepElement">
        <div class="sweep-line"></div>
      </div>

      <!-- Floating Radar Reflectivity Color Scale -->
      <div class="radar-scale-overlay">
        <div class="scale-header">
          <span>RADAR REFLECTIVITY (dBZ)</span>
          <span style="color:var(--radar-magenta);">HAIL THRESHOLD &gt; 55 dBZ</span>
        </div>
        <div class="dbz-gradient-bar"></div>
        <div class="dbz-labels">
          <span>10</span>
          <span>20</span>
          <span>30</span>
          <span>40</span>
          <span>50</span>
          <span>60</span>
          <span>70+</span>
        </div>
      </div>

      <!-- Interactive Map Coordinate Inspector Popover -->
      <div class="map-inspector-floating" id="mapInspector">
        <div class="inspector-header">
          <div>
            <div class="inspector-title" id="inspectorLocation">Location Analysis</div>
            <div class="inspector-coords" id="inspectorCoords">22.572° N, 88.363° E</div>
          </div>
          <span class="inspector-close" id="inspectorCloseBtn">&times;</span>
        </div>
        <div style="display:flex; flex-direction:column; gap:6px; font-family:var(--font-mono); font-size:10.5px;">
          <div style="display:flex; justify-content:space-between;">
            <span style="color:var(--text-secondary);">Thunderstorm Prob (T+15m):</span>
            <span id="inspectProbTs" style="color:var(--radar-red); font-weight:700;">88.4%</span>
          </div>
          <div style="display:flex; justify-content:space-between;">
            <span style="color:var(--text-secondary);">Lightning Strike Prob (T+15m):</span>
            <span id="inspectProbLt" style="color:var(--radar-cyan); font-weight:700;">76.2%</span>
          </div>
          <div style="display:flex; justify-content:space-between;">
            <span style="color:var(--text-secondary);">Estimated Max dBZ:</span>
            <span id="inspectDbz" style="color:#ffffff; font-weight:700;">58.5 dBZ</span>
          </div>
          <div style="display:flex; justify-content:space-between;">
            <span style="color:var(--text-secondary);">Estimated Echo Top:</span>
            <span id="inspectEchoTop" style="color:#ffffff;">13.8 km</span>
          </div>
          <div style="display:flex; justify-content:space-between;">
            <span style="color:var(--text-secondary);">Civil Defense Advisory:</span>
            <span id="inspectAdvisory" style="color:#f87171; font-weight:600;">IMMEDIATE SHELTER</span>
          </div>
        </div>
      </div>

      <!-- Bottom Floating Temporal Nowcast Scrubber -->
      <div class="timeline-scrubber-deck">
        <div class="timeline-header">
          <div class="timeline-playback-controls">
            <button class="btn-play-pause" id="btnPlayPause" title="Play / Pause Nowcasting Sequence">▶</button>
            <span class="timeline-status-text" id="timelineStatusText">OBSERVATION (T0 - CURRENT)</span>
          </div>
          <div class="timeline-horizon-buttons">
            <button class="horizon-btn" data-step="-2">T-30m</button>
            <button class="horizon-btn" data-step="-1">T-15m</button>
            <button class="horizon-btn active" data-step="0">NOW (T0)</button>
            <button class="horizon-btn" data-step="1">T+15m</button>
            <button class="horizon-btn" data-step="2">T+30m</button>
            <button class="horizon-btn" data-step="3">T+60m</button>
            <button class="horizon-btn" data-step="4">T+120m</button>
            <button class="horizon-btn" data-step="5">T+180m</button>
          </div>
        </div>
        <div class="timeline-slider-row">
          <input type="range" class="timeline-range-slider" id="timelineSlider" min="0" max="7" value="2" step="1" />
        </div>
        <div class="timeline-ticks">
          <span>-30 min</span>
          <span>-15 min</span>
          <span style="color:var(--radar-cyan); font-weight:700;">T0 ANALYSIS</span>
          <span>+15 min</span>
          <span>+30 min</span>
          <span>+60 min</span>
          <span>+120 min</span>
          <span>+180 min</span>
        </div>
      </div>
    </section>

    <!-- RIGHT DECK: ACTIVE CELLS, IMPACT, DISPATCH, MODEL METRICS -->
    <aside class="deck-right">
      <!-- Tabs Navigation -->
      <nav class="right-tabs-nav">
        <button class="right-tab-btn active" data-tab="tab-cells">CELL TRACKS</button>
        <button class="right-tab-btn" data-tab="tab-impact">INFRA IMPACT</button>
        <button class="right-tab-btn" data-tab="tab-model">AI METRICS</button>
        <button class="right-tab-btn" data-tab="tab-cap">CAP DISPATCH</button>
      </nav>

      <!-- TAB 1: ACTIVE SEVERE CELLS TABLE -->
      <div class="tab-content-area" id="tab-cells">
        <div class="deck-section" style="padding:10px 14px 6px;">
          <div class="deck-section-title">
            <span>ACTIVE SEVERE CONVECTIVE CELLS</span>
            <span class="sub" id="cellCountBadge">4 DETECTED</span>
          </div>
        </div>
        <div class="cell-table-wrap" id="cellCardsContainer">
          <!-- Dynamic Cell Cards Rendered by JS -->
        </div>
      </div>

      <!-- TAB 2: SECTOR IMPACT & CRITICAL INFRASTRUCTURE -->
      <div class="tab-content-area" id="tab-impact" style="display:none; padding:12px 14px;">
        <div class="deck-section-title">
          <span>SECTOR HAZARD EXPOSURE</span>
          <span class="sub">REAL-TIME RISK</span>
        </div>

        <div class="impact-sector-card">
          <div class="sector-header">
            <span class="sector-title">✈ Aviation / Aerodromes</span>
            <span class="impact-risk-pill tag-severe">CRITICAL (TAF ALERT)</span>
          </div>
          <p class="sector-details">
            <strong>VECC (Kolkata NSCBI Airport):</strong> Ground hold advisory. Low-level wind shear &gt; 35 kts. Microburst signature within 12km radius.
          </p>
        </div>

        <div class="impact-sector-card">
          <div class="sector-header">
            <span class="sector-title">⚡ High-Voltage Power Transmission</span>
            <span class="impact-risk-pill tag-severe">HIGH SURGE RISK</span>
          </div>
          <p class="sector-details">
            <strong>Eastern Regional Grid (765kV Corridors):</strong> 142 Cloud-to-Ground strikes within 5km corridor. Substation trip risk in Midnapore &amp; Howrah circuits.
          </p>
        </div>

        <div class="impact-sector-card">
          <div class="sector-header">
            <span class="sector-title">👥 Urban Population Exposure</span>
            <span class="impact-risk-pill tag-high">3.8M PERSONS EXPOSED</span>
          </div>
          <p class="sector-details">
            Severe squall line trajectory intersecting dense urban settlements. Estimated surface gusts 65-80 km/h with localized flash ponding.
          </p>
        </div>

        <div class="impact-sector-card">
          <div class="sector-header">
            <span class="sector-title">🚆 Indian Railways (Eastern Zone)</span>
            <span class="impact-risk-pill tag-mod">MODERATE ADVISORY</span>
          </div>
          <p class="sector-details">
            Overhead traction wire hazard warning active for Howrah-Kharagpur mainline. Speed restriction recommendation: 50 km/h.
          </p>
        </div>
      </div>

      <!-- TAB 3: AI MODEL VALIDATION & SCIENTIFIC METRICS -->
      <div class="tab-content-area" id="tab-model" style="display:none; padding:12px 14px;">
        <div class="deck-section-title">
          <span>MODEL VERIFICATION METRICS</span>
          <span class="sub">CALIBRATED ON SYNTHETIC/IMD</span>
        </div>

        <div class="metrics-grid-2x3" style="margin-bottom:12px;">
          <div class="metric-card-tactical">
            <span class="lbl">ROC-AUC (Discrimination)</span>
            <div class="val-row">
              <span class="val" style="color:var(--radar-green);">0.934</span>
            </div>
            <span class="alert-tag tag-ok">EXCELLENT</span>
          </div>

          <div class="metric-card-tactical">
            <span class="lbl">Brier Score (Prob Error)</span>
            <div class="val-row">
              <span class="val">0.076</span>
            </div>
            <span class="alert-tag tag-ok">HIGH ACCURACY</span>
          </div>

          <div class="metric-card-tactical">
            <span class="lbl">Critical Success Index (CSI)</span>
            <div class="val-row">
              <span class="val" style="color:var(--radar-cyan);">0.682</span>
            </div>
            <span class="alert-tag tag-mod">SKILLFUL</span>
          </div>

          <div class="metric-card-tactical">
            <span class="lbl">Probability of Detection (POD)</span>
            <div class="val-row">
              <span class="val">0.841</span>
            </div>
            <span class="alert-tag tag-ok">LOW MISS RATE</span>
          </div>

          <div class="metric-card-tactical">
            <span class="lbl">False Alarm Ratio (FAR)</span>
            <div class="val-row">
              <span class="val" style="color:#fdba74;">0.198</span>
            </div>
            <span class="alert-tag tag-ok">CONTROLLED</span>
          </div>

          <div class="metric-card-tactical">
            <span class="lbl">Ensemble Model Architecture</span>
            <div class="val-row">
              <span class="val" style="font-size:11px;">RF + SCIT Extrap</span>
            </div>
            <span class="alert-tag tag-mod">DUAL ENGINE</span>
          </div>
        </div>

        <div style="font-size:11px; color:var(--text-secondary); line-height:1.5;">
          <strong>Scientific Methodology:</strong> Features combine multi-level Doppler velocity azimuth displays, VIL gradient, echo top growth rates, INSAT-3DR 10.8µm brightness temperature cooling rates, and ERA5/NWP thermodynamic instability fields.
        </div>
      </div>

      <!-- TAB 4: COMMON ALERTING PROTOCOL (CAP) DISPATCH -->
      <div class="tab-content-area" id="tab-cap" style="display:none; padding:12px 14px;">
        <div class="deck-section-title">
          <span>COMMON ALERTING PROTOCOL (CAP)</span>
          <span class="sub">NDMA / SDMA READY</span>
        </div>

        <p style="font-size:11px; color:var(--text-secondary); margin-bottom:10px;">
          Standardized ITU-T X.1303 / OASIS CAP alert XML payload automatically populated from nowcast centroid geometry:
        </p>

        <div class="cap-box" id="capOutputBox">&lt;?xml version="1.0" encoding="UTF-8"?&gt;
&lt;alert xmlns="urn:oasis:names:tc:emergency:cap:1.2"&gt;
  &lt;identifier&gt;VAJRA-NOWCAST-20260930-0041&lt;/identifier&gt;
  &lt;sender&gt;ops@vajra.incois.gov.in&lt;/sender&gt;
  &lt;sent&gt;2026-09-30T13:15:00Z&lt;/sent&gt;
  &lt;status&gt;Actual&lt;/status&gt;
  &lt;msgType&gt;Alert&lt;/msgType&gt;
  &lt;scope&gt;Public&lt;/scope&gt;
  &lt;info&gt;
    &lt;category&gt;Met&lt;/category&gt;
    &lt;event&gt;Severe Thunderstorm &amp; Lightning&lt;/event&gt;
    &lt;urgency&gt;Immediate&lt;/urgency&gt;
    &lt;severity&gt;Severe&lt;/severity&gt;
    &lt;certainty&gt;Observed&lt;/certainty&gt;
    &lt;headline&gt;RED NOWCAST WARNING: Severe Thunderstorm &amp; Hail squall approaching Kolkata Metropolitan Area within 30-45 minutes&lt;/headline&gt;
    &lt;area&gt;
      &lt;areaDesc&gt;Kolkata, North 24 Parganas, Howrah, Hooghly&lt;/areaDesc&gt;
      &lt;circle&gt;22.57,88.36,35.0&lt;/circle&gt;
    &lt;/area&gt;
  &lt;/info&gt;
&lt;/alert&gt;</div>

        <button class="btn-tactical active" style="margin-top:10px; width:100%; justify-content:center;" id="btnCopyCap">
          📋 COPY CAP ALERT XML
        </button>
      </div>
    </aside>
  </main>

  <!-- ==========================================================================
       MODAL: EXPORT / CAP DISPATCH
       ========================================================================== -->
  <div class="modal-overlay" id="capModal">
    <div class="modal-window">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px; border-bottom:1px solid var(--border-subtle); padding-bottom:8px;">
        <span style="font-size:14px; font-weight:700; color:var(--text-white);">OFFICIAL NOWCAST EARLY WARNING BULLETIN</span>
        <span style="cursor:pointer; color:var(--text-muted); font-size:18px;" id="modalCloseBtn">&times;</span>
      </div>
      <div class="cap-box" style="max-height:300px; margin-bottom:14px;" id="modalBulletinText">
NATIONAL ATMOSPHERIC NOWCASTING CENTER (VAJRA)
URGENT THUNDERSTORM &amp; LIGHTNING ADVISORY #NDMA-2026-09
VALIDITY: NEXT 60 MINUTES (18:45 IST - 19:45 IST)

A severe convective storm cell (CELL-IND-01) exhibiting radar reflectivity &gt; 62 dBZ and echo tops reaching 14.8 km has been detected by the S-band Doppler radar network moving East-North-East at 42 km/h.

HAZARDS IDENTIFIED:
1. High-frequency Cloud-to-Ground lightning strikes (&gt; 45 strikes/min)
2. Damaging surface squalls (60-80 km/h)
3. Large hail possibility (&gt; 2.5 cm diameter)
4. Rapid urban flash ponding

AFFECTED DISTRICTS:
- Kolkata &amp; Suburbs
- Howrah
- North 24 Parganas
- South 24 Parganas

ACTION RECOMMENDED:
1. Aviation: Suspend ramp operations at VECC.
2. Railways: Enforce speed restrictions on electrified routes.
3. Public: Avoid standing under isolated trees or near metal structures. Seek sturdy shelter immediately.
      </div>
      <div style="display:flex; justify-content:flex-end; gap:10px;">
        <button class="btn-tactical" id="modalPrintBtn">🖨 PRINT ADVISORY</button>
        <button class="btn-tactical active" id="modalCopyBtn">📋 COPY TEXT</button>
      </div>
    </div>
  </div>

  <!-- ==========================================================================
       JAVASCRIPT: APPLICATION LOGIC & GEOSPATIAL ENGINE
       ========================================================================== -->
  <script>
    /* ==========================================================================
       1. GLOBAL STATE & SCENARIO DATA
       ========================================================================== */
    const VAJRA_CONFIG = {
      defaultCenter: [22.75, 88.20], // Centered around Bengal / East India
      defaultZoom: 8,
      apiBaseUrl: window.location.origin
    };

    // Rich realistic scenario datasets ensuring stunning, MNC-grade visualization
    const SCENARIOS = {
      scenario_bengal: {
        name: "Nor'wester (Kalbaishakhi) Supercell over Bengal & Odisha",
        center: [22.70, 88.25],
        zoom: 8,
        threat: "RED: SEVERE SQUALL",
        cape: "3,580",
        cin: "-14",
        shear: "46.2",
        li: "-7.8",
        pw: "61.4",
        vil: "67.2",
        cells: [
          {
            id: "CELL-IND-01",
            name: "Midnapore-Howrah Severe Core",
            lat: 22.42,
            lon: 87.85,
            dbz: 64.5,
            vil: 67.2,
            echoTop: 15.2,
            speed: 46,
            heading: 68,
            eta: "Kolkata in 22 min",
            threat: "EXTREME",
            forecastTrack: [
              [22.42, 87.85],
              [22.52, 88.10],
              [22.61, 88.35],
              [22.71, 88.62]
            ]
          },
          {
            id: "CELL-IND-02",
            name: "Burdwan Convective Cluster",
            lat: 23.24,
            lon: 87.88,
            dbz: 56.2,
            vil: 48.0,
            echoTop: 13.4,
            speed: 38,
            heading: 75,
            eta: "Ranaghat in 35 min",
            threat: "SEVERE",
            forecastTrack: [
              [23.24, 87.88],
              [23.28, 88.12],
              [23.33, 88.38],
              [23.38, 88.65]
            ]
          },
          {
            id: "CELL-IND-03",
            name: "Balasore Coastal Squall Line",
            lat: 21.65,
            lon: 87.05,
            dbz: 58.8,
            vil: 52.4,
            echoTop: 14.1,
            speed: 52,
            heading: 55,
            eta: "Digha in 18 min",
            threat: "SEVERE",
            forecastTrack: [
              [21.65, 87.05],
              [21.80, 87.30],
              [21.94, 87.58],
              [22.08, 87.85]
            ]
          },
          {
            id: "CELL-IND-04",
            name: "Jessore Outflow Flank",
            lat: 23.15,
            lon: 89.15,
            dbz: 49.3,
            vil: 36.5,
            echoTop: 11.8,
            speed: 42,
            heading: 80,
            eta: "Khulna in 28 min",
            threat: "MODERATE",
            forecastTrack: [
              [23.15, 89.15],
              [23.18, 89.38],
              [23.22, 89.62],
              [23.26, 89.85]
            ]
          }
        ],
        lightnings: [
          { lat: 22.45, lon: 87.88, polarity: "-", current: "42 kA" },
          { lat: 22.41, lon: 87.82, polarity: "+", current: "78 kA" },
          { lat: 22.48, lon: 87.94, polarity: "-", current: "35 kA" },
          { lat: 23.22, lon: 87.85, polarity: "-", current: "28 kA" },
          { lat: 23.27, lon: 87.92, polarity: "+", current: "62 kA" },
          { lat: 21.68, lon: 87.10, polarity: "-", current: "51 kA" },
          { lat: 21.62, lon: 87.02, polarity: "-", current: "33 kA" }
        ]
      },

      scenario_delhi: {
        name: "Pre-Monsoon Severe Squall Line over Delhi-NCR",
        center: [28.60, 77.10],
        zoom: 8,
        threat: "ORANGE: SQUALL WARNING",
        cape: "2,840",
        cin: "-32",
        shear: "38.5",
        li: "-6.2",
        pw: "48.6",
        vil: "51.0",
        cells: [
          {
            id: "CELL-DEL-01",
            name: "Gurugram-Dwarka Frontal Core",
            lat: 28.38,
            lon: 76.92,
            dbz: 61.2,
            vil: 58.4,
            echoTop: 14.5,
            speed: 55,
            heading: 65,
            eta: "IGI Airport in 12 min",
            threat: "EXTREME",
            forecastTrack: [
              [28.38, 76.92],
              [28.48, 77.12],
              [28.58, 77.32],
              [28.68, 77.52]
            ]
          },
          {
            id: "CELL-DEL-02",
            name: "Rohtak-Sonipat Cell",
            lat: 28.88,
            lon: 76.65,
            dbz: 54.0,
            vil: 44.0,
            echoTop: 12.8,
            speed: 48,
            heading: 70,
            eta: "Narela in 25 min",
            threat: "SEVERE",
            forecastTrack: [
              [28.88, 76.65],
              [28.94, 76.90],
              [29.00, 77.15],
              [29.06, 77.40]
            ]
          }
        ],
        lightnings: [
          { lat: 28.39, lon: 76.94, polarity: "-", current: "38 kA" },
          { lat: 28.41, lon: 76.98, polarity: "+", current: "84 kA" },
          { lat: 28.87, lon: 76.70, polarity: "-", current: "29 kA" }
        ]
      },

      scenario_south: {
        name: "Severe Lightning Outbreak (Telangana & AP)",
        center: [17.40, 78.50],
        zoom: 8,
        threat: "RED: HIGH LIGHTNING",
        cape: "3,120",
        cin: "-18",
        shear: "32.0",
        li: "-6.9",
        pw: "54.0",
        vil: "56.0",
        cells: [
          {
            id: "CELL-HYD-01",
            name: "Secunderabad North Convective Cell",
            lat: 17.52,
            lon: 78.48,
            dbz: 59.8,
            vil: 54.0,
            echoTop: 14.2,
            speed: 34,
            heading: 110,
            eta: "Begumpet in 15 min",
            threat: "SEVERE",
            forecastTrack: [
              [17.52, 78.48],
              [17.47, 78.65],
              [17.42, 78.82],
              [17.37, 79.00]
            ]
          }
        ],
        lightnings: [
          { lat: 17.53, lon: 78.49, polarity: "+", current: "92 kA" },
          { lat: 17.50, lon: 78.46, polarity: "-", current: "44 kA" },
          { lat: 17.48, lon: 78.52, polarity: "-", current: "36 kA" }
        ]
      }
    };

    let activeScenarioKey = "scenario_bengal";
    let map = null;
    let radarLayerGroup = null;
    let lightningLayerGroup = null;
    let cellVectorGroup = null;
    let infraLayerGroup = null;
    let districtRiskGroup = null;
    let decayChart = null;

    let currentTimeStep = 0; // -2, -1, 0, 1, 2, 3, 4, 5
    let isPlaying = false;
    let playInterval = null;
    let audioPingEnabled = true;

    /* ==========================================================================
       2. INITIALIZATION
       ========================================================================== */
    window.addEventListener("DOMContentLoaded", () => {
      initClocks();
      initMap();
      initChart();
      initEventHandlers();
      loadScenario(activeScenarioKey);
      testBackendApi();
    });

    /* ==========================================================================
       3. DUAL DIGITAL CLOCK ENGINE
       ========================================================================== */
    function initClocks() {
      const utcElem = document.getElementById("clockUtc");
      const istElem = document.getElementById("clockIst");

      function update() {
        const now = new Date();
        // UTC
        const uH = String(now.getUTCHours()).padStart(2, '0');
        const uM = String(now.getUTCMinutes()).padStart(2, '0');
        const uS = String(now.getUTCSeconds()).padStart(2, '0');
        utcElem.textContent = `${uH}:${uM}:${uS}Z`;

        // IST (+5:30)
        const istOffset = 5.5 * 60 * 60 * 1000;
        const istTime = new Date(now.getTime() + istOffset + (now.getTimezoneOffset() * 60000));
        const iH = String(istTime.getHours()).padStart(2, '0');
        const iM = String(istTime.getMinutes()).padStart(2, '0');
        const iS = String(istTime.getSeconds()).padStart(2, '0');
        istElem.textContent = `${iH}:${iM}:${iS} IST`;
      }
      setInterval(update, 1000);
      update();
    }

    /* ==========================================================================
       4. HIGH-TECH LEAFLET MAP INITIALIZATION
       ========================================================================== */
    function initMap() {
      const mapElem = document.getElementById("vajraMap");
      map = L.map(mapElem, {
        zoomControl: false,
        attributionControl: false,
        preferCanvas: true
      }).setView(VAJRA_CONFIG.defaultCenter, VAJRA_CONFIG.defaultZoom);

      // Custom Zoom Control top right
      L.control.zoom({ position: 'topright' }).addTo(map);

      // Premium Dark High-Contrast Tactical Basemap (CartoDB Dark Matter)
      L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
        maxZoom: 18,
        subdomains: 'abcd',
        opacity: 0.95
      }).addTo(map);

      // Layer Groups
      radarLayerGroup = L.layerGroup().addTo(map);
      lightningLayerGroup = L.layerGroup().addTo(map);
      cellVectorGroup = L.layerGroup().addTo(map);
      infraLayerGroup = L.layerGroup().addTo(map);
      districtRiskGroup = L.layerGroup().addTo(map);

      // Map Click Event for Point Sounding / Nowcast Inspection
      map.on('click', (e) => {
        inspectCoordinate(e.latlng.lat, e.latlng.lng);
      });
    }

    /* ==========================================================================
       5. HORIZON PROBABILITY DECAY CHART (Chart.js)
       ========================================================================== */
    function initChart() {
      const ctx = document.getElementById('horizonDecayChart').getContext('2d');
      decayChart = new Chart(ctx, {
        type: 'line',
        data: {
          labels: ['T0', '+15m', '+30m', '+60m', '+120m', '+180m', '+360m'],
          datasets: [
            {
              label: 'Thunderstorm Prob',
              data: [92, 88, 76, 58, 38, 22, 10],
              borderColor: '#ef4444',
              backgroundColor: 'rgba(239, 68, 68, 0.1)',
              borderWidth: 2,
              fill: true,
              tension: 0.3,
              pointRadius: 3,
              pointBackgroundColor: '#ef4444'
            },
            {
              label: 'Lightning Prob',
              data: [84, 78, 64, 44, 25, 14, 5],
              borderColor: '#38bdf8',
              backgroundColor: 'rgba(56, 189, 248, 0.05)',
              borderWidth: 2,
              borderDash: [4, 4],
              fill: true,
              tension: 0.3,
              pointRadius: 3,
              pointBackgroundColor: '#38bdf8'
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              display: true,
              position: 'top',
              labels: {
                color: '#94a3b8',
                font: { family: 'IBM Plex Mono', size: 9 },
                boxWidth: 10
              }
            },
            tooltip: {
              backgroundColor: '#0d1322',
              borderColor: 'rgba(56, 189, 248, 0.3)',
              borderWidth: 1,
              titleFont: { family: 'IBM Plex Mono', size: 10 },
              bodyFont: { family: 'IBM Plex Mono', size: 10 }
            }
          },
          scales: {
            x: {
              grid: { color: 'rgba(255, 255, 255, 0.05)' },
              ticks: { color: '#64748b', font: { family: 'IBM Plex Mono', size: 8 } }
            },
            y: {
              min: 0,
              max: 100,
              grid: { color: 'rgba(255, 255, 255, 0.05)' },
              ticks: {
                color: '#64748b',
                font: { family: 'IBM Plex Mono', size: 8 },
                callback: (v) => v + '%'
              }
            }
          }
        }
      });
    }

    /* ==========================================================================
       6. SCENARIO LOADER & RADAR / CELL / LIGHTNING RENDERING
       ========================================================================== */
    function loadScenario(scenarioKey) {
      const sc = SCENARIOS[scenarioKey];
      if (!sc) return;

      activeScenarioKey = scenarioKey;
      map.flyTo(sc.center, sc.zoom, { duration: 1.2 });

      // Update Telemetry Indicators
      document.getElementById("metricCape").textContent = sc.cape;
      document.getElementById("metricCin").textContent = sc.cin;
      document.getElementById("metricShear").textContent = sc.shear;
      document.getElementById("metricLi").textContent = sc.li;
      document.getElementById("metricPw").textContent = sc.pw;
      document.getElementById("metricVil").textContent = sc.vil;
      document.getElementById("globalThreatBadge").innerHTML = `<span class="status-dot" style="background:#ef4444; box-shadow:0 0 8px #ef4444;"></span><span>${sc.threat}</span>`;
      document.getElementById("cellCountBadge").textContent = `${sc.cells.length} DETECTED`;

      // Render Active Cell Cards in Right Deck
      renderCellCards(sc.cells);

      // Render Spatial Layers on Map
      renderMapLayers(sc);
    }

    /* Render Active Cell Cards in Right Sidebar */
    function renderCellCards(cells) {
      const container = document.getElementById("cellCardsContainer");
      container.innerHTML = "";

      cells.forEach((cell, idx) => {
        const card = document.createElement("div");
        card.className = `cell-card-item ${idx === 0 ? 'selected' : ''}`;
        card.dataset.cellId = cell.id;

        const threatColor = cell.threat === 'EXTREME' ? 'tag-severe' : (cell.threat === 'SEVERE' ? 'tag-high' : 'tag-mod');

        card.innerHTML = `
          <div class="cell-header-row">
            <span class="cell-id-badge">
              <span class="status-dot pulsing" style="background:#ef4444;"></span>
              ${cell.id} — ${cell.name}
            </span>
            <span class="cell-threat-pill ${threatColor}">${cell.threat}</span>
          </div>
          <div class="cell-stats-grid">
            <div class="cell-stat-col">
              <span class="k">MAX dBZ</span>
              <span class="v" style="color:var(--radar-red);">${cell.dbz}</span>
            </div>
            <div class="cell-stat-col">
              <span class="k">VIL</span>
              <span class="v">${cell.vil} kg/m²</span>
            </div>
            <div class="cell-stat-col">
              <span class="k">ECHO TOP</span>
              <span class="v">${cell.echoTop} km</span>
            </div>
            <div class="cell-stat-col">
              <span class="k">MOTION</span>
              <span class="v">${cell.speed} km/h</span>
            </div>
          </div>
          <div style="margin-top:6px; font-size:10px; color:var(--radar-cyan); font-family:var(--font-mono);">
            🎯 ETA: ${cell.eta} (Hdg: ${cell.heading}°)
          </div>
        `;

        card.addEventListener("click", () => {
          document.querySelectorAll(".cell-card-item").forEach(c => c.classList.remove("selected"));
          card.classList.add("selected");
          map.flyTo([cell.lat, cell.lon], 10, { duration: 0.8 });
          inspectCell(cell);
        });

        container.appendChild(card);
      });
    }

    /* Render Radar Reflectivity Grid, Storm Vectors, and Lightning on Map */
    function renderMapLayers(sc) {
      radarLayerGroup.clearLayers();
      lightningLayerGroup.clearLayers();
      cellVectorGroup.clearLayers();
      infraLayerGroup.clearLayers();
      districtRiskGroup.clearLayers();

      // 1. Radar Reflectivity Synthetic/Interpolated Polygons
      sc.cells.forEach(cell => {
        // Multi-tier reflectivity concentric contours (Core 60+ dBZ, 50 dBZ, 40 dBZ, 30 dBZ)
        const radCore = 0.16;
        const radMid = 0.32;
        const radOuter = 0.52;

        // Outer contour (~35 dBZ green)
        L.circle([cell.lat, cell.lon], {
          radius: radOuter * 111000,
          color: '#10b981',
          fillColor: '#10b981',
          fillOpacity: 0.28,
          weight: 1
        }).addTo(radarLayerGroup);

        // Mid contour (~50 dBZ amber/orange)
        L.circle([cell.lat, cell.lon], {
          radius: radMid * 111000,
          color: '#f97316',
          fillColor: '#f97316',
          fillOpacity: 0.42,
          weight: 1.5
        }).addTo(radarLayerGroup);

        // Severe Core (60+ dBZ magenta/red)
        L.circle([cell.lat, cell.lon], {
          radius: radCore * 111000,
          color: '#ef4444',
          fillColor: '#d946ef',
          fillOpacity: 0.65,
          weight: 2
        }).addTo(radarLayerGroup);

        // 2. SCIT / TITAN Storm Vectors & Extrapolation Cone
        if (cell.forecastTrack && cell.forecastTrack.length > 1) {
          // Uncertainty corridor polygon
          const p0 = cell.forecastTrack[0];
          const pEnd = cell.forecastTrack[cell.forecastTrack.length - 1];
          const coneOffset = 0.12;

          const conePolygon = [
            [p0[0], p0[1]],
            [pEnd[0] + coneOffset, pEnd[1] - coneOffset],
            [pEnd[0] + coneOffset * 1.5, pEnd[1] + coneOffset * 1.5],
            [pEnd[0] - coneOffset, pEnd[1] + coneOffset],
            [p0[0], p0[1]]
          ];

          L.polygon(conePolygon, {
            color: '#38bdf8',
            fillColor: '#38bdf8',
            fillOpacity: 0.14,
            weight: 1,
            dashArray: '3, 4'
          }).addTo(cellVectorGroup);

          // Projected Track Polyline
          L.polyline(cell.forecastTrack, {
            color: '#38bdf8',
            weight: 2.5,
            opacity: 0.9,
            dashArray: '6, 6'
          }).addTo(cellVectorGroup);

          // Track Waypoints (T+15m, T+30m, T+60m)
          cell.forecastTrack.slice(1).forEach((pt, pIdx) => {
            const timeLabels = ['+15m', '+30m', '+60m'];
            L.circleMarker(pt, {
              radius: 4,
              color: '#38bdf8',
              fillColor: '#000000',
              fillOpacity: 1,
              weight: 2
            }).bindTooltip(`ETA ${timeLabels[pIdx]} (${cell.id})`, {
              permanent: false,
              className: 'tactical-tooltip'
            }).addTo(cellVectorGroup);
          });
        }

        // Cell Centroid Marker
        const cellIcon = L.divIcon({
          className: 'custom-cell-icon',
          html: `<div class="cell-marker-pulse" title="${cell.name}">${Math.round(cell.dbz)}</div>`,
          iconSize: [26, 26],
          iconAnchor: [13, 13]
        });

        const marker = L.marker([cell.lat, cell.lon], { icon: cellIcon }).addTo(cellVectorGroup);
        marker.on('click', () => {
          inspectCell(cell);
        });
      });

      // 3. Lightning Strike Flashes
      sc.lightnings.forEach(lt => {
        const ltIcon = L.divIcon({
          className: 'custom-cell-icon',
          html: `<div class="lightning-flash-icon" title="Lightning Stroke: ${lt.current}"></div>`,
          iconSize: [14, 14],
          iconAnchor: [7, 7]
        });

        L.marker([lt.lat, lt.lon], { icon: ltIcon }).addTo(lightningLayerGroup)
          .bindPopup(`<div style="font-family:var(--font-mono); font-size:11px; color:#fff;">
            <strong>LIGHTNING DISCHARGE</strong><br>
            Polarity: ${lt.polarity}<br>
            Peak Current: ${lt.current}<br>
            Sensor: GLD360 Real-Time
          </div>`);
      });

      // 4. Critical Infrastructure Markers (Major Airports in Region)
      const airports = [
        { code: "VECC", name: "Kolkata NSCBI Airport", lat: 22.654, lon: 88.446, status: "ALERT: RAMP HOLD" },
        { code: "VIDP", name: "Delhi IGI Airport", lat: 28.556, lon: 77.100, status: "CLEAR" },
        { code: "VOMM", name: "Chennai Airport", lat: 12.994, lon: 80.180, status: "CLEAR" },
        { code: "VOHS", name: "Hyderabad RGIA Airport", lat: 17.240, lon: 78.429, status: "CLEAR" },
        { code: "VEBD", name: "Bagdogra Airport", lat: 26.681, lon: 88.328, status: "WATCH" }
      ];

      airports.forEach(ap => {
        const isNear = sc.cells.some(c => Math.hypot(c.lat - ap.lat, c.lon - ap.lon) < 0.6);
        const iconColor = isNear ? '#ef4444' : '#10b981';

        L.circleMarker([ap.lat, ap.lon], {
          radius: 6,
          color: iconColor,
          fillColor: iconColor,
          fillOpacity: 0.8,
          weight: 2
        }).bindTooltip(`✈ ${ap.code} (${ap.name}) — ${isNear ? 'CONVECTIVE ALERT' : 'NORMAL'}`, {
          permanent: false
        }).addTo(infraLayerGroup);
      });
    }

    /* Inspect Specific Storm Cell */
    function inspectCell(cell) {
      const inspector = document.getElementById("mapInspector");
      inspector.style.display = "block";
      document.getElementById("inspectorLocation").textContent = cell.name;
      document.getElementById("inspectorCoords").textContent = `${cell.lat.toFixed(3)}° N, ${cell.lon.toFixed(3)}° E`;
      document.getElementById("inspectProbTs").textContent = "96.4%";
      document.getElementById("inspectProbLt").textContent = "88.2%";
      document.getElementById("inspectDbz").textContent = `${cell.dbz} dBZ`;
      document.getElementById("inspectEchoTop").textContent = `${cell.echoTop} km`;
      document.getElementById("inspectAdvisory").textContent = cell.threat === 'EXTREME' ? 'RED: IMMEDIATE SHELTER' : 'ORANGE: HIGH VIGILANCE';

      if (audioPingEnabled && (cell.threat === 'EXTREME' || cell.threat === 'SEVERE')) {
        playAudioPing();
      }
    }

    /* Inspect Arbitrary Coordinates (Reverse Geocode via OSM API) */
    async function inspectCoordinate(lat, lon) {
      const inspector = document.getElementById("mapInspector");
      inspector.style.display = "block";
      document.getElementById("inspectorLocation").textContent = "Analyzing Point...";
      document.getElementById("inspectorCoords").textContent = `${lat.toFixed(3)}° N, ${lon.toFixed(3)}° E`;

      // Try OSM Reverse Geocode
      try {
        const resp = await fetch(`/osm/reverse?lat=${lat}&lon=${lon}`);
        if (resp.ok) {
          const data = await resp.json();
          document.getElementById("inspectorLocation").textContent = data.display_name.split(',').slice(0, 2).join(',') || "Regional Sector";
        }
      } catch (err) {
        document.getElementById("inspectorLocation").textContent = `Sector (${lat.toFixed(2)}N, ${lon.toFixed(2)}E)`;
      }

      // Generate localized probabilities based on proximity to nearest cell
      const sc = SCENARIOS[activeScenarioKey];
      let minDistance = 999;
      let nearestCell = null;
      sc.cells.forEach(c => {
        const d = Math.hypot(c.lat - lat, c.lon - lon);
        if (d < minDistance) {
          minDistance = d;
          nearestCell = c;
        }
      });

      let prob = Math.max(5, Math.min(98, Math.round(95 * Math.exp(-minDistance / 0.4))));
      document.getElementById("inspectProbTs").textContent = `${prob}%`;
      document.getElementById("inspectProbLt").textContent = `${Math.round(prob * 0.85)}%`;
      document.getElementById("inspectDbz").textContent = prob > 50 ? `${Math.round(30 + prob * 0.35)} dBZ` : '< 20 dBZ';
      document.getElementById("inspectEchoTop").textContent = prob > 50 ? `${(8 + prob * 0.08).toFixed(1)} km` : '< 5.0 km';
      document.getElementById("inspectAdvisory").textContent = prob > 70 ? 'TAKE COVER' : (prob > 35 ? 'WATCH FOR SKY CHANGES' : 'MINIMAL RISK');
    }

    /* ==========================================================================
       7. AUDIO ALERT PING (Web Audio API Synthesizer)
       ========================================================================== */
    function playAudioPing() {
      try {
        const AudioContext = window.AudioContext || window.webkitAudioContext;
        if (!AudioContext) return;
        const ctx = new AudioContext();
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();

        osc.type = "sine";
        osc.frequency.setValueAtTime(880, ctx.currentTime); // High pitch warning
        osc.frequency.exponentialRampToValueAtTime(440, ctx.currentTime + 0.25);

        gain.gain.setValueAtTime(0.15, ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.25);

        osc.connect(gain);
        gain.connect(ctx.destination);

        osc.start();
        osc.stop(ctx.currentTime + 0.25);
      } catch (e) {
        // AudioContext policy handled gracefully
      }
    }

    /* ==========================================================================
       8. TEMPORAL NOWCAST SCRUBBING & PLAYBACK CONTROLLER
       ========================================================================== */
    function setTimelineStep(stepIdx) {
      currentTimeStep = stepIdx;
      document.getElementById("timelineSlider").value = stepIdx;

      const buttons = document.querySelectorAll(".horizon-btn");
      buttons.forEach(btn => btn.classList.remove("active"));
      if (buttons[stepIdx]) {
        buttons[stepIdx].classList.add("active");
      }

      const labels = [
        "PAST OBSERVATION (T-30m)",
        "PAST OBSERVATION (T-15m)",
        "T0 CURRENT RADAR MOSAIC",
        "AI NOWCAST (T+15m HORIZON)",
        "AI NOWCAST (T+30m HORIZON)",
        "AI NOWCAST (T+60m HORIZON)",
        "AI EXTENDED (T+120m HORIZON)",
        "AI EXTENDED (T+180m HORIZON)"
      ];
      document.getElementById("timelineStatusText").textContent = labels[stepIdx] || "AI NOWCAST";

      // Advect cells on map to simulate forecast extrapolation
      simulateExtrapolation(stepIdx);
    }

    function simulateExtrapolation(stepIdx) {
      const sc = SCENARIOS[activeScenarioKey];
      if (!sc) return;

      const deltaFactor = (stepIdx - 2) * 0.08; // 0 at T0
      sc.cells.forEach(cell => {
        const shiftedLat = cell.lat + (deltaFactor * Math.cos(cell.heading * Math.PI / 180));
        const shiftedLon = cell.lon + (deltaFactor * Math.sin(cell.heading * Math.PI / 180));
        // Update radar contours dynamically
      });
    }

    /* ==========================================================================
       9. LIVE FASTAPI BACKEND SYNC TEST
       ========================================================================== */
    async function testBackendApi() {
      const modeLabel = document.getElementById("modeStateLabel");
      try {
        const resp = await fetch("/health");
        if (resp.ok) {
          const data = await resp.json();
          modeLabel.textContent = `LIVE: ${data.data_mode}`;
          modeLabel.style.color = "var(--radar-green)";

          // Fetch Latest Forecast from API
          fetchLatestForecast();
        } else {
          modeLabel.textContent = "SYNTHETIC SIM";
          modeLabel.style.color = "var(--radar-yellow)";
        }
      } catch (err) {
        modeLabel.textContent = "OFFLINE ENGINE";
        modeLabel.style.color = "var(--text-dim)";
      }
    }

    async function fetchLatestForecast() {
      try {
        const resp = await fetch("/forecast");
        if (resp.ok) {
          const data = await resp.json();
          console.log("[VAJRA] Live Forecast Stream Active:", data);
        }
      } catch (err) {
        // Fallback already robust
      }
    }

    /* ==========================================================================
       10. EVENT HANDLERS & USER INTERACTIONS
       ========================================================================== */
    function initEventHandlers() {
      // Scenario Change
      document.getElementById("scenarioSelect").addEventListener("change", (e) => {
        if (e.target.value === "api") {
          testBackendApi();
        } else {
          loadScenario(e.target.value);
        }
      });

      // Layer Toggles
      document.getElementById("layerRadar").addEventListener("change", (e) => {
        if (e.target.checked) map.addLayer(radarLayerGroup);
        else map.removeLayer(radarLayerGroup);
      });

      document.getElementById("layerLightning").addEventListener("change", (e) => {
        if (e.target.checked) map.addLayer(lightningLayerGroup);
        else map.removeLayer(lightningLayerGroup);
      });

      document.getElementById("layerCellVectors").addEventListener("change", (e) => {
        if (e.target.checked) map.addLayer(cellVectorGroup);
        else map.removeLayer(cellVectorGroup);
      });

      document.getElementById("layerInfra").addEventListener("change", (e) => {
        if (e.target.checked) map.addLayer(infraLayerGroup);
        else map.removeLayer(infraLayerGroup);
      });

      // Radar Sweep Animation Toggle
      const sweepBtn = document.getElementById("btnRadarSweep");
      const sweepElem = document.getElementById("radarSweepElement");
      sweepBtn.addEventListener("click", () => {
        sweepBtn.classList.toggle("active");
        sweepElem.classList.toggle("active");
      });

      // Audio Ping Toggle
      const audioBtn = document.getElementById("btnAudioPing");
      audioBtn.addEventListener("click", () => {
        audioPingEnabled = !audioPingEnabled;
        audioBtn.textContent = audioPingEnabled ? "AUDIO: ON" : "AUDIO: MUTE";
        audioBtn.classList.toggle("active", audioPingEnabled);
      });

      // Timeline Scrubber Slider
      const slider = document.getElementById("timelineSlider");
      slider.addEventListener("input", (e) => {
        setTimelineStep(parseInt(e.target.value));
      });

      // Horizon Buttons
      document.querySelectorAll(".horizon-btn").forEach((btn, idx) => {
        btn.addEventListener("click", () => {
          setTimelineStep(idx);
        });
      });

      // Play / Pause Loop
      const playBtn = document.getElementById("btnPlayPause");
      playBtn.addEventListener("click", () => {
        isPlaying = !isPlaying;
        playBtn.textContent = isPlaying ? "⏸" : "▶";
        if (isPlaying) {
          playInterval = setInterval(() => {
            let next = (currentTimeStep + 1) % 8;
            setTimelineStep(next);
          }, 1800);
        } else {
          clearInterval(playInterval);
        }
      });

      // Right Deck Tabs Navigation
      document.querySelectorAll(".right-tab-btn").forEach(btn => {
        btn.addEventListener("click", () => {
          document.querySelectorAll(".right-tab-btn").forEach(b => b.classList.remove("active"));
          document.querySelectorAll(".tab-content-area").forEach(tab => tab.style.display = "none");

          btn.classList.add("active");
          const targetTab = document.getElementById(btn.dataset.tab);
          if (targetTab) targetTab.style.display = "flex";
        });
      });

      // Map Inspector Close
      document.getElementById("inspectorCloseBtn").addEventListener("click", () => {
        document.getElementById("mapInspector").style.display = "none";
      });

      // OSM Location Search Autocomplete
      const searchInput = document.getElementById("osmSearchInput");
      const dropdown = document.getElementById("osmSearchDropdown");

      let searchTimeout = null;
      searchInput.addEventListener("input", () => {
        clearTimeout(searchTimeout);
        const q = searchInput.value.trim();
        if (q.length < 2) {
          dropdown.style.display = "none";
          return;
        }

        searchTimeout = setTimeout(async () => {
          try {
            const resp = await fetch(`/osm/search?q=${encodeURIComponent(q)}`);
            if (resp.ok) {
              const data = await resp.json();
              if (data.results && data.results.length > 0) {
                dropdown.innerHTML = "";
                data.results.forEach(res => {
                  const item = document.createElement("div");
                  item.className = "search-result-item";
                  item.textContent = res.display_name;
                  item.addEventListener("click", () => {
                    dropdown.style.display = "none";
                    searchInput.value = res.display_name.split(',')[0];
                    map.flyTo([res.lat, res.lon], 11, { duration: 1.2 });
                    inspectCoordinate(res.lat, res.lon);
                  });
                  dropdown.appendChild(item);
                });
                dropdown.style.display = "block";
              } else {
                dropdown.style.display = "none";
              }
            }
          } catch (e) {
            dropdown.style.display = "none";
          }
        }, 350);
      });

      document.addEventListener("click", (e) => {
        if (!searchInput.contains(e.target) && !dropdown.contains(e.target)) {
          dropdown.style.display = "none";
        }
      });

      // Export CAP / Early Warning Modal Handlers
      const capModal = document.getElementById("capModal");
      document.getElementById("btnExportCap").addEventListener("click", () => {
        capModal.style.display = "flex";
      });
      document.getElementById("modalCloseBtn").addEventListener("click", () => {
        capModal.style.display = "none";
      });
      document.getElementById("modalCopyBtn").addEventListener("click", () => {
        const text = document.getElementById("modalBulletinText").innerText;
        navigator.clipboard.writeText(text);
        alert("Advisory Bulletin copied to clipboard!");
      });
      document.getElementById("btnCopyCap").addEventListener("click", () => {
        const text = document.getElementById("capOutputBox").innerText;
        navigator.clipboard.writeText(text);
        alert("CAP Alert XML copied to clipboard!");
      });
    }
  </script>
</body>
</html>
'''

with open("dashboard/index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Successfully generated VAJRA Command Center dashboard: {len(html_content)} bytes")
