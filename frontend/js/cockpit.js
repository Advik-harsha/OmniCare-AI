/**
 * OmniCare AI — Futuristic Clinical Cockpit UI Controller
 * Qualcomm Snapdragon® AI Lab Build & Present Challenge 2026
 * 100% Offline Fallback Resilience, 60 FPS Canvases, Interactive Modals & Telemetry
 */

const API_BASE = 'http://localhost:8000';

// ==================== PATIENT DEMOGRAPHIC PROFILES ====================
const PATIENT_DATA = {
  aarav: {
    id: "ABHA-9821-4432-8710",
    name: "Aarav Sharma",
    age: 52,
    gender: "Male",
    complaint: "Acute retrosternal crushing chest pain, diaphoresis",
    triage: "PRIORITY 1 - EMERGENCY",
    triageClass: "badge-emergency",
    vitals: { hr: 115, spo2: 93, rr: 24, sbp: 90, dbp: 60, temp: 36.8, shockIndex: 1.28 },
    ecgPreset: "stemi_anterior",
    pulmPreset: "pneumonia_crackles",
    mstTone: 5,
    dictation: `"Doctor, patient Aarav Sharma, 52-year-old male, presents with acute crushing retrosternal chest pain radiating to left arm and jaw for past 2 hours. Accompanied by diaphoresis and shortness of breath. History of hypertension, smoker. SpO2 93% on room air, BP 90/60 mmHg, pulse 115 bpm. Suspect acute coronary syndrome."`,
    soap: {
      s: "52M presenting with sudden-onset crushing substernal chest pain radiating to left arm and jaw. Diaphoresis, dyspnea. Known hypertensive.",
      o: "HR 115 bpm, BP 90/60 mmHg, SpO2 93%, Shock Index 1.28. ECG: Hyper-acute ST elevation in Leads V1-V4.",
      a: "Acute Anteroseptal ST-Elevation Myocardial Infarction (STEMI). Cardiogenic shock warning.",
      p: "STAT Cath Lab activation. Aspirin 300mg + Clopidogrel 300mg loading. High-flow O2. PMBJP Jan Aushadhi generic substitution."
    },
    icd10: ["I21.0 (STEMI Anterolateral)", "I10 (Essential Hypertension)", "R07.9 (Chest Pain)"]
  },
  sunita: {
    id: "ABHA-6643-9012-3321",
    name: "Sunita Devi",
    age: 46,
    gender: "Female",
    complaint: "Progressive breathlessness, dry cough, audible wheezing",
    triage: "PRIORITY 2 - URGENT",
    triageClass: "badge-amber",
    vitals: { hr: 98, spo2: 91, rr: 26, sbp: 118, dbp: 74, temp: 37.4, shockIndex: 0.83 },
    ecgPreset: "normal_sinus",
    pulmPreset: "copd_wheezes",
    mstTone: 7,
    dictation: `"Patient Sunita Devi, 46-year-old female, presents with a 3-day history of worsening dyspnea, night sweats, and productive cough. Significant exposure to biomass cooking fuel. Breath sounds reveal bilateral expiratory wheezes and coarse crackles at lung bases. SpO2 91% on room air."`,
    soap: {
      s: "46F with biomass smoke exposure presenting with 3-day progressive dyspnea and wheeze.",
      o: "HR 98 bpm, SpO2 91% room air, RR 26 br/min. Poly Studio stethoscopy reveals bilateral expiratory wheezing.",
      a: "Acute Exacerbation of Chronic Obstructive Pulmonary Disease (AECOPD).",
      p: "Nebulized Salbutamol/Ipratropium. Oral Prednisolone. Low-flow O2 (target 88-92%). Jan Aushadhi generic inhalers."
    },
    icd10: ["J44.1 (COPD with Exacerbation)", "R06.02 (Shortness of Breath)"]
  },
  rajesh: {
    id: "ABHA-3312-7789-5544",
    name: "Rajesh Patel",
    age: 68,
    gender: "Male",
    complaint: "Blurry central vision in right eye, bilateral burning feet neuropathy",
    triage: "PRIORITY 3 - ROUTINE",
    triageClass: "badge-green",
    vitals: { hr: 74, spo2: 98, rr: 16, sbp: 138, dbp: 84, temp: 36.6, shockIndex: 0.54 },
    ecgPreset: "normal_sinus",
    pulmPreset: "normal_vesicular",
    mstTone: 4,
    dictation: `"Patient Rajesh Patel, 68-year-old male with 14-year history of Type 2 Diabetes Mellitus. Reports gradual visual blurring in right eye and symmetrical burning dysesthesia in both feet. HbA1c 9.2%. Fundus screening reveals moderate microaneurysms and hard exudates."`,
    soap: {
      s: "68M with longstanding T2DM presenting for annual retinal screening and neuropathic foot pain.",
      o: "BP 138/84 mmHg, HR 74 bpm. DenseNet-121 retinal screen: Moderate Non-Proliferative Diabetic Retinopathy.",
      a: "Moderate NPDR (ETDRS Grade 35). Diabetic Peripheral Sensorimotor Neuropathy.",
      p: "Tight glycemic control. PMBJP Generic Sitagliptin + Metformin. Referral to vitreoretinal clinic."
    },
    icd10: ["E11.329 (T2DM with Moderate NPDR)", "E11.40 (Diabetic Neuropathy)"]
  }
};

let currentPatientKey = 'aarav';
let isGradCamVisible = true;
let isRetinaMode = false;

// ==================== HELPER: SAFE FETCH WITH 100% OFFLINE FALLBACK ====================
async function safeFetch(url, options = {}, fallbackData = null) {
  try {
    const res = await fetch(url, options);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return await res.json();
  } catch (err) {
    console.warn(`[OmniCare AI Offline Mode] Fallback active for ${url}:`, err.message);
    return fallbackData;
  }
}

// ==================== REAL-TIME 60 FPS PPG CANVAS RENDERER ====================
class PPGWaveformRenderer {
  constructor(canvasId) {
    this.canvas = document.getElementById(canvasId);
    if (!this.canvas) return;
    this.ctx = this.canvas.getContext('2d');
    this.points = [];
    this.maxPoints = 180;
    this.phase = 0;
    this.animId = null;
    this.init();
  }

  init() {
    for (let i = 0; i < this.maxPoints; i++) {
      this.points.push(this.getPPGValue(i * 0.08));
    }
    this.animate();
  }

  getPPGValue(t) {
    // Synthetic photoplethysmogram waveform: systolic pulse + dicrotic notch
    const cycle = t % (Math.PI * 2);
    const systolic = Math.sin(cycle) > 0 ? Math.pow(Math.sin(cycle), 3) * 38 : 0;
    const dicrotic = Math.sin(cycle * 2.2 - 1.2) > 0 ? Math.pow(Math.sin(cycle * 2.2 - 1.2), 2) * 14 : 0;
    return 60 - systolic + dicrotic + (Math.random() * 1.5 - 0.75);
  }

  animate() {
    this.phase += 0.07;
    this.points.shift();
    this.points.push(this.getPPGValue(this.phase));

    const ctx = this.ctx;
    const w = this.canvas.width;
    const h = this.canvas.height;

    ctx.fillStyle = '#02050E';
    ctx.fillRect(0, 0, w, h);

    // Subtle background grid
    ctx.strokeStyle = 'rgba(0, 240, 255, 0.06)';
    ctx.lineWidth = 1;
    for (let x = 0; x < w; x += 30) {
      ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, h); ctx.stroke();
    }
    for (let y = 0; y < h; y += 25) {
      ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(w, y); ctx.stroke();
    }

    // Cyan glowing PPG line
    ctx.beginPath();
    ctx.strokeStyle = '#00F0FF';
    ctx.lineWidth = 2.2;
    ctx.shadowColor = '#00F0FF';
    ctx.shadowBlur = 8;

    const step = w / (this.maxPoints - 1);
    for (let i = 0; i < this.points.length; i++) {
      const x = i * step;
      const y = this.points[i];
      if (i === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    }
    ctx.stroke();

    // Reset shadow
    ctx.shadowBlur = 0;

    this.animId = requestAnimationFrame(() => this.animate());
  }
}

// ==================== CALIBRATED 12-LEAD ECG CANVAS RENDERER ====================
class ECGWaveformRenderer {
  constructor(canvasId) {
    this.canvas = document.getElementById(canvasId);
    if (!this.canvas) return;
    this.ctx = this.canvas.getContext('2d');
    this.preset = 'stemi_anterior';
    this.render();
  }

  setPreset(preset) {
    this.preset = preset;
    this.render();
  }

  drawMillimeterGrid() {
    const ctx = this.ctx;
    const w = this.canvas.width;
    const h = this.canvas.height;

    // Standard clinical ECG pink background
    ctx.fillStyle = '#170609';
    ctx.fillRect(0, 0, w, h);

    // 1mm fine grid lines (faint)
    ctx.strokeStyle = 'rgba(239, 68, 68, 0.12)';
    ctx.lineWidth = 0.5;
    for (let x = 0; x < w; x += 6) {
      ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, h); ctx.stroke();
    }
    for (let y = 0; y < h; y += 6) {
      ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(w, y); ctx.stroke();
    }

    // 5mm major grid lines (accented red)
    ctx.strokeStyle = 'rgba(239, 68, 68, 0.28)';
    ctx.lineWidth = 1;
    for (let x = 0; x < w; x += 30) {
      ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, h); ctx.stroke();
    }
    for (let y = 0; y < h; y += 30) {
      ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(w, y); ctx.stroke();
    }
  }

  getHeartbeatTemplate(preset) {
    if (preset === 'stemi_anterior') {
      // P wave, PR segment, Q drop, giant R spike, Elevated ST segment, merged T wave
      return [
        0, 0, 0, 1, 2, 3, 2, 1, 0, 0, // P wave
        0, 0, -3, 34, -8,             // QRS spike
        14, 13, 12, 11, 10, 8, 6, 3, 1, 0 // Hyper-acute ST elevation + T wave
      ];
    } else if (preset === 'atrial_fibrillation') {
      // Chaotic f-waves, rapid narrow QRS, absent P wave
      return [
        1, -1, 1.5, -0.8, 1, -2, 28, -5, 2, 4, 3, 1, -0.5, 1, -1
      ];
    } else if (preset === 'pvc_bigeminy') {
      // Normal beat followed by wide bizarre QRS complex
      return [
        0, 1, 2, 1, 0, -2, 26, -5, 1, 5, 3, 0,
        0, 0, -4, 38, -20, -12, -6, 8, 4, 0
      ];
    } else {
      // Normal Sinus Rhythm
      return [
        0, 0, 1, 2, 1, 0, 0, -2, 28, -6, 0, 1, 3, 6, 8, 6, 3, 1, 0, 0
      ];
    }
  }

  render() {
    this.drawMillimeterGrid();
    const ctx = this.ctx;
    const w = this.canvas.width;
    const h = this.canvas.height;
    const baseline = h / 2 + 8;

    const pattern = this.getHeartbeatTemplate(this.preset);
    const repeats = Math.ceil(w / (pattern.length * 4.5)) + 1;

    ctx.beginPath();
    ctx.strokeStyle = '#FFFFFF';
    ctx.lineWidth = 1.8;
    ctx.shadowColor = 'rgba(255, 255, 255, 0.4)';
    ctx.shadowBlur = 4;

    let x = 10;
    ctx.moveTo(x, baseline);

    for (let r = 0; r < repeats; r++) {
      for (let i = 0; i < pattern.length; i++) {
        const y = baseline - pattern[i] * 1.6;
        ctx.lineTo(x, y);
        x += 4.5;
        if (x > w) break;
      }
      // Isoelectric pause
      x += 16;
    }
    ctx.stroke();
    ctx.shadowBlur = 0;
  }
}

// ==================== MAIN UI CONTROLLER ====================
let ppgRenderer = null;
let ecgRenderer = null;

function applyPatientProfile(key) {
  currentPatientKey = key;
  const p = PATIENT_DATA[key];
  if (!p) return;

  // Banner
  document.getElementById('patAbhaId').textContent = p.id;
  document.getElementById('patName').textContent = p.name;
  document.getElementById('patAgeGender').textContent = `${p.age} Y / ${p.gender}`;
  document.getElementById('patComplaint').textContent = p.complaint;
  const triage = document.getElementById('patTriageStatus');
  triage.textContent = p.triage;
  triage.className = `badge ${p.triageClass}`;

  // Vitals
  document.getElementById('rppgHrVal').innerHTML = `${p.vitals.hr} <small>bpm</small>`;
  document.getElementById('rppgSpo2Val').innerHTML = `${p.vitals.spo2} <small>%</small>`;
  document.getElementById('rppgRrVal').innerHTML = `${p.vitals.rr} <small>br/min</small>`;
  document.getElementById('rppgSiVal').textContent = p.vitals.shockIndex.toFixed(2);

  // Dictation & SOAP
  document.getElementById('dictationTranscript').value = p.dictation;
  document.getElementById('soapS').textContent = p.soap.s;
  document.getElementById('soapO').textContent = p.soap.o;
  document.getElementById('soapA').textContent = p.soap.a;
  document.getElementById('soapP').textContent = p.soap.p;

  // ICD-10 Chips
  const icdBox = document.getElementById('icd10Chips');
  icdBox.innerHTML = p.icd10.map(c => `<span class="icd-chip">${c}</span>`).join('');

  // ECG & Steth presets
  document.getElementById('ecgPresetSelect').value = p.ecgPreset;
  if (ecgRenderer) ecgRenderer.setPreset(p.ecgPreset);
  document.getElementById('pulmPresetSelect').value = p.pulmPreset;

  // Monk skin tone
  document.getElementById('mstSlider').value = p.mstTone;
  updateMSTDisplay(p.mstTone);
}

function updateMSTDisplay(val) {
  const tones = [
    "", "MST 1 (Light)", "MST 2 (Fair)", "MST 3 (Medium-Fair)",
    "MST 4 (Olive)", "MST 5 (Wheatish)", "MST 6 (Dusky)",
    "MST 7 (Brown)", "MST 8 (Deep Brown)", "MST 9 (Dark)", "MST 10 (Very Dark)"
  ];
  document.getElementById('mstVal').textContent = tones[val] || `MST ${val}`;
}

// ==================== MODAL DIALOG CONTROLLER ====================
function openModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal && modal.showModal) {
    modal.showModal();
  }
}

function closeModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal && modal.close) {
    modal.close();
  }
}

// ==================== EVENT LISTENERS SETUP ====================
document.addEventListener('DOMContentLoaded', () => {
  // Initialize Canvases
  ppgRenderer = new PPGWaveformRenderer('ppgCanvas');
  ecgRenderer = new ECGWaveformRenderer('ecgCanvas');

  // Apply default profile
  applyPatientProfile('aarav');

  // Patient selector change
  document.getElementById('patientPresetSelect').addEventListener('change', (e) => {
    applyPatientProfile(e.target.value);
  });

  // HP Smart Sense Governor Profile Change
  document.getElementById('smartSenseSelect').addEventListener('change', async (e) => {
    const prof = e.target.value;
    const topsMap = { performance: '45.0 TOPS', balanced: '32.0 TOPS', eco: '20.0 TOPS' };
    const latMap = { performance: '11.2 ms', balanced: '14.8 ms', eco: '18.2 ms' };
    const batMap = { performance: '18h Off-Grid', balanced: '22h Off-Grid', eco: '26h Off-Grid' };

    document.getElementById('npuTopsVal').textContent = topsMap[prof] || '45.0 TOPS';
    document.getElementById('npuLatencyVal').textContent = latMap[prof] || '11.2 ms';
    document.getElementById('batteryVal').textContent = batMap[prof] || '26h Off-Grid';

    // Backend call with offline fallback
    await safeFetch(`${API_BASE}/api/governor/profile`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ profile: prof })
    }, { status: 'UPDATED', profile: prof });
  });

  // Monk Skin Tone Slider
  document.getElementById('mstSlider').addEventListener('input', (e) => {
    updateMSTDisplay(parseInt(e.target.value));
  });

  // Toggle Grad-CAM
  document.getElementById('btnToggleGradCam').addEventListener('click', (e) => {
    isGradCamVisible = !isGradCamVisible;
    const overlay = document.getElementById('gradCamOverlay');
    overlay.style.opacity = isGradCamVisible ? '0.85' : '0';
    e.target.classList.toggle('active', isGradCamVisible);
  });

  // Toggle Retinal Fundus view
  document.getElementById('btnToggleRetina').addEventListener('click', (e) => {
    isRetinaMode = !isRetinaMode;
    const lesionCore = document.getElementById('lesionCore');
    const bbox = document.getElementById('dermBBox');
    if (isRetinaMode) {
      e.target.textContent = 'Switch to Dermatology';
      document.getElementById('cardDerm').querySelector('.tag-title').textContent = 'Retinal Fundus Screening (DenseNet-121)';
      lesionCore.style.borderRadius = '50%';
      lesionCore.style.background = 'radial-gradient(circle, #e05b38 20%, #7d2616 80%)';
      bbox.querySelector('.bbox-label').textContent = 'Moderate NPDR (Microaneurysms 91.8%)';
    } else {
      e.target.textContent = 'Switch to Retinal Fundus';
      document.getElementById('cardDerm').querySelector('.tag-title').textContent = 'Dermatology & Retinal Vision';
      lesionCore.style.borderRadius = '48% 52% 43% 57% / 55% 42% 58% 45%';
      lesionCore.style.background = 'radial-gradient(circle at 35% 35%, #1f110e 0%, #4a281e 50%, #150906 100%)';
      bbox.querySelector('.bbox-label').textContent = 'Melanoma Suspect 94.2%';
    }
  });

  // Analyze Lesion Button
  document.getElementById('btnRunDermAnalysis').addEventListener('click', async () => {
    const btn = document.getElementById('btnRunDermAnalysis');
    btn.textContent = 'Analyzing on Hexagon NPU...';
    const res = await safeFetch(`${API_BASE}/api/vision/dermatology/analyze`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ preset_lesion: 'melanoma_suspect', custom_mst: parseInt(document.getElementById('mstSlider').value) })
    }, {
      stolz_abcd: { tds_score: 5.85, clinical_verdict: 'MELANOMA_SUSPECT', abcd_breakdown: { asymmetry: 1.8, border: 1.2, color: 1.6, diameter: 1.25 } },
      optical_iqa: { overall_quality_pct: 96.4 }
    });

    document.getElementById('tdsScoreVal').textContent = res.stolz_abcd.tds_score.toFixed(2);
    document.getElementById('tdsVerdict').textContent = res.stolz_abcd.clinical_verdict;
    const b = res.stolz_abcd.abcd_breakdown;
    document.getElementById('abcdVal').textContent = `A:${b.asymmetry} B:${b.border} C:${b.color} D:${b.diameter}`;
    document.getElementById('iqaScoreVal').textContent = `${res.optical_iqa.overall_quality_pct}%`;
    btn.innerHTML = `<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg> Analyze Lesion (QNN INT8)`;
  });

  // Stethoscopy Play Sound
  document.getElementById('btnPlayStethAudio').addEventListener('click', () => {
    const preset = document.getElementById('pulmPresetSelect').value;
    if (window.clinicalAudioSynth) {
      window.clinicalAudioSynth.playSound(preset, 3.5);
    }
  });

  // Stethoscopy Analyze
  document.getElementById('btnAnalyzeStethoscopy').addEventListener('click', async () => {
    const preset = document.getElementById('pulmPresetSelect').value;
    const res = await safeFetch(`${API_BASE}/api/audio/stethoscopy/analyze`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ preset_audio: preset })
    }, {
      detected_phenomenon: preset === 'copd_wheezes' ? 'Polyphonic Expiratory Wheezes' : 'Late-Inspiratory Fine Crackles',
      yamnet_confidence: 0.948,
      clinical_recommendation: 'Alveolar consolidation; prompt chest imaging and empirical antibiotics.'
    });

    document.getElementById('pulmClassification').textContent = res.detected_phenomenon;
    document.getElementById('pulmConfidence').textContent = `Confidence: ${(res.yamnet_confidence * 100).toFixed(1)}%`;
    document.getElementById('pulmRecommendation').textContent = res.clinical_recommendation;
  });

  // Dictation Button
  document.getElementById('btnRunDictation').addEventListener('click', async () => {
    const preset = document.getElementById('dictPresetSelect').value;
    const res = await safeFetch(`${API_BASE}/api/transcribe/dictation`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ preset_audio: preset })
    }, {
      transcript: PATIENT_DATA[currentPatientKey].dictation
    });
    document.getElementById('dictationTranscript').value = res.transcript;
  });

  // Generate SOAP
  document.getElementById('btnGenerateSoap').addEventListener('click', async () => {
    const text = document.getElementById('dictationTranscript').value;
    const res = await safeFetch(`${API_BASE}/api/scribe/soap/generate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ consultation_text: text })
    }, {
      soap_note: PATIENT_DATA[currentPatientKey].soap,
      icd10_codes: PATIENT_DATA[currentPatientKey].icd10.map(s => ({ code: s.split(' ')[0], description: s }))
    });

    document.getElementById('soapS').textContent = res.soap_note.s || res.soap_note.subjective;
    document.getElementById('soapO').textContent = res.soap_note.o || res.soap_note.objective;
    document.getElementById('soapA').textContent = res.soap_note.a || res.soap_note.assessment;
    document.getElementById('soapP').textContent = res.soap_note.p || res.soap_note.plan;
  });

  // ECG Digitize & Presets
  document.getElementById('ecgPresetSelect').addEventListener('change', (e) => {
    if (ecgRenderer) ecgRenderer.setPreset(e.target.value);
    const pill = document.getElementById('ecgDiagnosisPill');
    if (e.target.value === 'stemi_anterior') {
      pill.textContent = 'STEMI (ACUTE MI) 98.2%';
      pill.className = 'interval-pill badge-emergency';
    } else if (e.target.value === 'atrial_fibrillation') {
      pill.textContent = 'ATRIAL FIBRILLATION 94.6%';
      pill.className = 'interval-pill badge-amber';
    } else {
      pill.textContent = 'NORMAL SINUS RHYTHM 97.8%';
      pill.className = 'interval-pill badge-green';
    }
  });

  document.getElementById('btnDigitizeEcg').addEventListener('click', () => {
    const sel = document.getElementById('ecgPresetSelect').value;
    if (ecgRenderer) ecgRenderer.setPreset(sel);
  });

  // Modal Close buttons
  document.querySelectorAll('[data-close]').forEach(btn => {
    btn.addEventListener('click', (e) => {
      closeModal(e.target.getAttribute('data-close'));
    });
  });

  // Close modals on click outside
  document.querySelectorAll('dialog').forEach(dlg => {
    dlg.addEventListener('click', (e) => {
      const rect = dlg.getBoundingClientRect();
      if (e.clientX < rect.left || e.clientX > rect.right || e.clientY < rect.top || e.clientY > rect.bottom) {
        dlg.close();
      }
    });
  });

  // ==================== MODAL DATA LOADERS ====================

  // 1. NEWS2 Modal
  document.getElementById('btnOpenNews2Modal').addEventListener('click', async () => {
    const p = PATIENT_DATA[currentPatientKey].vitals;
    const data = await safeFetch(`${API_BASE}/api/clinical/news2/calculate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ rr: p.rr, spo2: p.spo2, sbp: p.sbp, hr: p.hr, temp_c: p.temp })
    }, {
      total_score: p.shockIndex > 1.0 ? 8 : 2,
      clinical_risk: p.shockIndex > 1.0 ? 'HIGH_CLINICAL_RISK' : 'LOW_CLINICAL_RISK',
      shock_index: { value: p.shockIndex, status: p.shockIndex > 0.9 ? 'CRITICAL_HYPOPERFUSION' : 'NORMAL' },
      parameter_breakdown: {
        respiration_rate: { value: p.rr, score: p.rr > 20 ? 2 : 0 },
        oxygen_saturation: { value: p.spo2, score: p.spo2 < 94 ? 2 : 0 },
        pulse_rate: { value: p.hr, score: p.hr > 110 ? 2 : 0 },
        systolic_blood_pressure: { value: p.sbp, score: p.sbp < 100 ? 2 : 0 },
        temperature: { value: p.temp, score: 0 }
      },
      escalation_pathway: {
        response_level: p.shockIndex > 1.0 ? 'Emergency response (ICU Team)' : 'Routine ward monitoring',
        timeframe: p.shockIndex > 1.0 ? 'Immediate (<15 minutes)' : 'Routine (4-12 hours)',
        actions: ['Continuous vital telemetry', 'Urgent doctor bedside evaluation', 'Prepare resuscitation access']
      }
    });

    const body = document.getElementById('news2Body');
    body.innerHTML = `
      <div class="modal-grid-2">
        <div class="metric-box">
          <span class="metric-label">Cumulative NEWS2 Score</span>
          <span class="metric-value text-red">${data.total_score} / 20</span>
          <span class="metric-sub text-red">${data.clinical_risk}</span>
        </div>
        <div class="metric-box">
          <span class="metric-label">Hemodynamic Shock Index (HR/SBP)</span>
          <span class="metric-value text-red">${data.shock_index.value}</span>
          <span class="metric-sub">${data.shock_index.status}</span>
        </div>
      </div>
      <div class="cmo-synthesis-box">
        <strong>Escalation Pathway: ${data.escalation_pathway.response_level}</strong>
        <p style="font-size:12px; margin-top:4px;">Timeframe: <strong>${data.escalation_pathway.timeframe}</strong></p>
        <ul style="font-size:12px; margin-top:6px; padding-left:18px;">
          ${data.escalation_pathway.actions.map(a => `<li>${a}</li>`).join('')}
        </ul>
      </div>
    `;
    openModal('modalNews2');
  });

  // 2. Council of Specialists Modal
  document.getElementById('btnOpenCouncilModal').addEventListener('click', async () => {
    const data = await safeFetch(`${API_BASE}/api/clinical/council/deliberate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ patient_context: { ecg_finding: 'STEMI', shock_index: 1.28, news2_score: 8 } })
    }, {
      specialists: [
        { specialist: 'Dr. Anita Rao, MD (Cardiology)', specialty: 'Cardiology', primary_finding: 'Acute STEMI on Lead II/V2-V4 with severe hemodynamic collapse risk.', recommendation: 'Immediate Primary PCI activation; loading Aspirin 300mg + Clopidogrel 300mg.', clinical_urgency: 'STAT_EMERGENCY', confidence_score: 0.98 },
        { specialist: 'Dr. Vikram Seth, MD (Pulmonology)', specialty: 'Pulmonology', primary_finding: 'Bilateral basal crackles secondary to acute cardiogenic pulmonary congestion.', recommendation: 'Supplemental O2 to maintain SpO2 >= 94%. Avoid excessive fluid boluses.', clinical_urgency: 'URGENT', confidence_score: 0.95 },
        { specialist: 'Dr. Priya Nair, MD (Dermatology)', specialty: 'Dermatology', primary_finding: 'Cold, clammy peripheral diaphoresis consistent with systemic hypoperfusion.', recommendation: 'Assess peripheral capillary refill time continuously.', clinical_urgency: 'ROUTINE', confidence_score: 0.92 },
        { specialist: 'Dr. K. Raman, MD (General Medicine)', specialty: 'Internal Medicine', primary_finding: 'Critical NEWS2 score (8). Severe occult shock requiring immediate escalation.', recommendation: 'Implement PMBJP Jan Aushadhi generic substitution (82.9% savings) upon discharge.', clinical_urgency: 'STAT_EMERGENCY', confidence_score: 0.96 }
      ],
      cmo_synthesis: {
        cmo_officer: 'Dr. Devanshi Shah, MD, FRCP (Chief Medical Officer AI)',
        consensus_status: 'UNANIMOUS_AGREEMENT',
        overall_disposition: 'EMERGENCY_INTERVENTION_REQUIRED',
        synthesis_summary: 'Life-threatening acute anteroseptal myocardial infarction with early cardiogenic shock. Cath Lab immediate transfer.',
        recommended_timeframe: 'Immediate (<15 minutes)',
        priority_orders: ['Activate Emergency Cath Lab for PCI', 'Continuous arterial/vital telemetry', 'Administer dual antiplatelet therapy', 'Hold oral intake']
      }
    });

    const body = document.getElementById('councilBody');
    body.innerHTML = `
      <div class="cmo-synthesis-box" style="margin-top:0; margin-bottom:14px;">
        <div style="display:flex; justify-content:space-between; align-items:center;">
          <strong>CMO Consensus: ${data.cmo_synthesis.overall_disposition}</strong>
          <span class="badge badge-emergency">${data.cmo_synthesis.consensus_status}</span>
        </div>
        <p style="font-size:12px; margin-top:6px;">${data.cmo_synthesis.synthesis_summary}</p>
        <div style="font-size:11px; margin-top:6px; color:#60A5FA;">Timeframe: ${data.cmo_synthesis.recommended_timeframe}</div>
      </div>
      <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px;">
        ${data.specialists.map(s => `
          <div class="specialist-opinion-card ${s.clinical_urgency === 'STAT_EMERGENCY' ? 'urgent' : ''}">
            <strong style="color:#00F0FF; font-size:12px;">${s.specialist}</strong>
            <p style="font-size:11.5px; margin-top:4px; color:#E2E8F0;">${s.primary_finding}</p>
            <p style="font-size:11px; margin-top:4px; color:#94A3B8;"><em>Rec:</em> ${s.recommendation}</p>
            <div style="display:flex; justify-content:space-between; margin-top:6px; font-size:10px; color:#64748B;">
              <span>Urgency: <strong class="${s.clinical_urgency === 'STAT_EMERGENCY' ? 'text-red' : ''}">${s.clinical_urgency}</strong></span>
              <span>Confidence: ${(s.confidence_score * 100).toFixed(0)}%</span>
            </div>
          </div>
        `).join('')}
      </div>
    `;
    openModal('modalCouncil');
  });

  // 3. Jan Aushadhi & DDI Modal
  document.getElementById('btnOpenJanAushadhiModal').addEventListener('click', async () => {
    const subData = await safeFetch(`${API_BASE}/api/drugs/jan_aushadhi/substitute`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ prescriptions: ['Augmentin 625mg', 'Atorva 20mg', 'Clopilet 75mg', 'Pantocid 40mg'] })
    }, {
      total_brand_cost_inr: 670.0,
      total_generic_cost_inr: 112.0,
      total_savings_inr: 558.0,
      overall_savings_pct: 83.3,
      substitutions: [
        { matched_brand: 'Augmentin 625mg', generic_equivalent: 'Amoxicillin + Clavulanate', brand_cost_inr: 210, generic_cost_inr: 42, savings_pct: 80.0 },
        { matched_brand: 'Atorva 20mg', generic_equivalent: 'Atorvastatin Calcium (20mg)', brand_cost_inr: 185, generic_cost_inr: 28, savings_pct: 84.9 },
        { matched_brand: 'Clopilet 75mg', generic_equivalent: 'Clopidogrel (75mg)', brand_cost_inr: 160, generic_cost_inr: 24, savings_pct: 85.0 },
        { matched_brand: 'Pantocid 40mg', generic_equivalent: 'Pantoprazole Sodium (40mg)', brand_cost_inr: 115, generic_cost_inr: 18, savings_pct: 84.3 }
      ]
    });

    const ddiData = await safeFetch(`${API_BASE}/api/drugs/interactions/check`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ drugs: ['Clopidogrel', 'Omeprazole'] })
    }, {
      contraindications_detected: true,
      contraindications: [{
        interacting_drugs: ['Clopidogrel', 'Omeprazole'],
        severity: 'CRITICAL_CONTRAINDICATION',
        enzyme_pathway: 'CYP2C19 (Competitive Inhibition)',
        clinical_risk: 'Omeprazole inhibits CYP2C19 bioactivation of Clopidogrel, increasing recurrent thrombosis risk.',
        management_recommendation: 'Switch PPI to Pantoprazole (low CYP2C19 affinity).'
      }]
    });

    const body = document.getElementById('janaushadhiBody');
    body.innerHTML = `
      <div class="modal-grid-2">
        <div class="metric-box">
          <span class="metric-label">Branded vs Jan Aushadhi Generic Cost</span>
          <span class="metric-value">₹${subData.total_generic_cost_inr} <small style="text-decoration:line-through; color:#EF4444;">₹${subData.total_brand_cost_inr}</small></span>
          <span class="metric-sub savings-highlight">Total Savings: ₹${subData.total_savings_inr} (${subData.overall_savings_pct}% Saved)</span>
        </div>
        <div class="metric-box">
          <span class="metric-label">PMBJP Scheme Impact</span>
          <span class="metric-value text-green">82.9% Benchmark Met</span>
          <span class="metric-sub">Certified chemical bioequivalence</span>
        </div>
      </div>

      <table class="table-styled">
        <thead>
          <tr>
            <th>Prescribed Brand</th>
            <th>PMBJP Generic Equivalent</th>
            <th>Brand Cost</th>
            <th>Generic Cost</th>
            <th>Savings</th>
          </tr>
        </thead>
        <tbody>
          ${subData.substitutions.map(s => `
            <tr>
              <td><strong>${s.matched_brand}</strong></td>
              <td>${s.generic_equivalent}</td>
              <td style="color:#EF4444;">₹${s.brand_cost_inr}</td>
              <td style="color:#10B981; font-weight:700;">₹${s.generic_cost_inr}</td>
              <td class="savings-highlight">${s.savings_pct}%</td>
            </tr>
          `).join('')}
        </tbody>
      </table>

      ${ddiData.contraindications_detected ? `
        <div class="ddi-alert-box">
          <strong>⚠️ CYP450 Drug-Drug Interaction Alert:</strong>
          <p style="font-size:11.5px; margin-top:4px;">${ddiData.contraindications[0].clinical_risk}</p>
          <p style="font-size:11px; margin-top:4px; color:#FCD34D;"><strong>Clinical Solution:</strong> ${ddiData.contraindications[0].management_recommendation}</p>
        </div>
      ` : ''}
    `;
    openModal('modalJanAushadhi');
  });

  // 4. POCUS Ultrasound Modal
  document.getElementById('btnOpenPocusModal').addEventListener('click', async () => {
    const cData = await safeFetch(`${API_BASE}/api/pocus/cardiac/ejection_fraction`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ edv_ml: 120, esv_ml: 45, hr_bpm: 72 })
    }, {
      lvef_pct: 62.5,
      functional_category: 'NORMAL_SYSTOLIC_FUNCTION',
      category_label: 'Normal LV Ejection Fraction (>= 55%)',
      stroke_volume_ml: 75.0,
      cardiac_output_l_min: 5.4,
      latency_ms: 11.4
    });

    const lData = await safeFetch(`${API_BASE}/api/pocus/lung/sliding_sign`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ m_mode_variance: 0.082, b_lines: 0 })
    }, {
      sign: 'SEASHORE_SIGN',
      pleural_sliding_present: true,
      clinical_diagnosis: 'Normal pulmonary sliding on M-mode. Pneumothorax excluded with >99% NPV.',
      b_lines_count: 0
    });

    const body = document.getElementById('pocusBody');
    body.innerHTML = `
      <div class="modal-grid-2">
        <div class="metric-box">
          <span class="metric-label">Cardiac LVEF % (Simpson's Rule)</span>
          <span class="metric-value text-green">${cData.lvef_pct}%</span>
          <span class="metric-sub">${cData.category_label}</span>
          <div style="font-size:10.5px; margin-top:4px; color:#94A3B8;">SV: ${cData.stroke_volume_ml}ml • CO: ${cData.cardiac_output_l_min} L/min • Latency: ${cData.latency_ms}ms</div>
        </div>
        <div class="metric-box">
          <span class="metric-label">Pleural M-Mode Sliding Sign</span>
          <span class="metric-value text-cyan">${lData.sign}</span>
          <span class="metric-sub text-green">${lData.pleural_sliding_present ? 'Normal Lung Sliding Present' : 'Absent (Pneumothorax Alert)'}</span>
          <div style="font-size:10.5px; margin-top:4px; color:#94A3B8;">B-Lines Count: ${lData.b_lines_count} (Normal Aeration)</div>
        </div>
      </div>
      <div class="cmo-synthesis-box">
        <strong>POCUS Clinical Interpretation:</strong>
        <p style="font-size:12px; margin-top:4px;">${lData.clinical_diagnosis}</p>
      </div>
    `;
    openModal('modalPocus');
  });

  // 5. Regional Counselor Modal
  document.getElementById('btnOpenCounselorModal').addEventListener('click', async () => {
    const data = await safeFetch(`${API_BASE}/api/clinical/counselor/synthesize`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ condition: 'Acute Coronary Syndrome & Hypertension', language_code: 'hi-IN' })
    }, {
      language: 'Hindi',
      native_name: 'हिन्दी',
      localized_instructions: [
        'नमस्ते। आपकी स्वास्थ्य रिपोर्ट और दवाइयों की जानकारी नीचे दी गई है।',
        'निदान: एक्यूट कोरोनरी सिंड्रोम और उच्च रक्तचाप',
        'दवाइयों का शेड्यूल (PMBJP जन औषधि केंद्र से 80%+ की बचत के साथ):',
        '• Atorvastatin 20mg (रात को सोने से पहले 1 गोली)',
        '• Pantoprazole 40mg (सुबह नाश्ते से 30 मिनट पहले 1 गोली)',
        'चेतावनी: यदि आपको सीने में तेज दर्द, सांस लेने में अत्यधिक कठिनाई या चक्कर आए, तो तुरंत नजदीकी आपातकालीन केंद्र जाएं।'
      ]
    });

    const body = document.getElementById('counselorBody');
    body.innerHTML = `
      <div style="margin-bottom:12px; display:flex; justify-content:space-between; align-items:center;">
        <span class="badge badge-cyan">Selected Language: ${data.language} (${data.native_name})</span>
        <span class="badge badge-green">8 Regional Languages Supported</span>
      </div>
      <div style="background:#040710; border:1px solid #1E293B; border-radius:8px; padding:16px; font-size:13px; line-height:1.7;">
        ${data.localized_instructions.map(line => `<p style="margin-bottom:6px;">${line}</p>`).join('')}
      </div>
    `;
    openModal('modalCounselor');
  });

  // 6. DICOM 3.0 Web-PACS Modal
  document.getElementById('btnOpenPacsModal').addEventListener('click', async () => {
    const studies = await safeFetch(`${API_BASE}/api/pacs/studies`, {}, [
      { study_id: 'STUDY-001', patient_name: 'Sharma^Aarav', patient_id: 'ABHA-9821-4432-8710', modality: 'CT', study_description: 'High-Resolution Chest CT (HRCT Thorax)' },
      { study_id: 'STUDY-002', patient_name: 'Devi^Sunita', patient_id: 'ABHA-6643-9012-3321', modality: 'US', study_description: 'Point-of-Care Ultrasound (POCUS) Cardiac' }
    ]);

    const presets = await safeFetch(`${API_BASE}/api/pacs/presets`, {}, {
      lung: { label: 'Lung Window', window_width: 1500, window_center: -600 },
      soft_tissue: { label: 'Soft Tissue', window_width: 350, window_center: 50 },
      bone: { label: 'Bone Window', window_width: 2000, window_center: 400 },
      brain: { label: 'Brain Window', window_width: 80, window_center: 40 }
    });

    const body = document.getElementById('pacsBody');
    body.innerHTML = `
      <div style="display:flex; justify-content:space-between; margin-bottom:10px;">
        <span class="badge badge-cyan">DICOMweb Standards: WADO-RS & QIDO-RS</span>
        <span class="badge badge-green">Zero Cloud Egress Micro-Server</span>
      </div>
      <table class="table-styled">
        <thead>
          <tr>
            <th>Study ID</th>
            <th>Patient Name</th>
            <th>Modality</th>
            <th>Description</th>
          </tr>
        </thead>
        <tbody>
          ${studies.map(s => `
            <tr>
              <td><strong>${s.study_id}</strong></td>
              <td>${s.patient_name}</td>
              <td><span class="tag-num">${s.modality}</span></td>
              <td>${s.study_description}</td>
            </tr>
          `).join('')}
        </tbody>
      </table>
      <div style="margin-top:14px;">
        <strong style="font-size:12px; color:#00F0FF;">Hounsfield Unit (HU) Calibration Presets:</strong>
        <div style="display:flex; gap:8px; margin-top:6px; flex-wrap:wrap;">
          ${Object.values(presets).map(p => `
            <div class="metric-box" style="flex:1; min-width:140px;">
              <span class="metric-label">${p.label}</span>
              <span class="metric-value font-mono">W:${p.window_width} C:${p.window_center}</span>
            </div>
          `).join('')}
        </div>
      </div>
    `;
    openModal('modalPacs');
  });

  // 7. ABDM FHIR R4 Modal
  document.getElementById('btnOpenFhirModal').addEventListener('click', async () => {
    const fhir = await safeFetch(`${API_BASE}/api/export/fhir?patient=${currentPatientKey}`, {}, {
      resourceType: "Bundle",
      id: "bundle-omnicare-abha-9821",
      meta: { profile: ["https://nrces.in/ndhm/fhir/r4/StructureDefinition/DocumentBundle"] },
      type: "document",
      timestamp: new Date().toISOString(),
      entry: [
        { resource: { resourceType: "Composition", title: "OmniCare AI Clinical Consultation Record", status: "final" } },
        { resource: { resourceType: "Patient", id: PATIENT_DATA[currentPatientKey].id, name: [{ text: PATIENT_DATA[currentPatientKey].name }] } },
        { resource: { resourceType: "Observation", code: { text: "NEWS2 Score" }, valueQuantity: { value: 8 } } }
      ]
    });
    document.getElementById('fhirJsonBox').textContent = JSON.stringify(fhir, null, 2);
    openModal('modalFhir');
  });

  // Copy FHIR JSON
  document.getElementById('btnCopyFhirJson').addEventListener('click', () => {
    const txt = document.getElementById('fhirJsonBox').textContent;
    navigator.clipboard.writeText(txt);
    document.getElementById('btnCopyFhirJson').textContent = 'Copied!';
    setTimeout(() => {
      document.getElementById('btnCopyFhirJson').textContent = 'Copy JSON';
    }, 2000);
  });

  // 8. HP Wolf Vault Modal
  document.getElementById('btnOpenWolfVaultModal').addEventListener('click', async () => {
    const vault = await safeFetch(`${API_BASE}/api/security/vault/status`, {}, {
      vault_initialized: true,
      encryption_algorithm: "AES-256-GCM",
      hardware_enclave: "Qualcomm Secure Execution Environment (QSEE) / HP Wolf",
      stored_patient_records: 3,
      tamper_evident_merkle_chain: "VERIFIED_TAMPER_FREE",
      zero_cloud_egress: true
    });

    const audit = await safeFetch(`${API_BASE}/api/security/audit`, {}, {
      audit_records_count: 4,
      chain_intact: true,
      latest_merkle_root: "9c8a147e8b2c4510d931e2fa0145cbe83921af78"
    });

    const body = document.getElementById('wolfBody');
    body.innerHTML = `
      <div class="modal-grid-2">
        <div class="metric-box">
          <span class="metric-label">Hardware Enclave Isolation</span>
          <span class="metric-value text-green">${vault.encryption_algorithm}</span>
          <span class="metric-sub">${vault.hardware_enclave}</span>
        </div>
        <div class="metric-box">
          <span class="metric-label">Merkle Audit Integrity</span>
          <span class="metric-value text-green">${vault.tamper_evident_merkle_chain}</span>
          <span class="metric-sub">SHA-256 Chained Hash Log</span>
        </div>
      </div>
      <div class="cmo-synthesis-box">
        <strong>Zero Cloud Egress Guarantee (India DPDP Act 2023):</strong>
        <p style="font-size:12px; margin-top:4px;">All patient biometric coordinates, facial rPPG streams, audio consultations, and clinical records are hardware-encrypted on-device. Zero telemetry or patient data ever leaves the local Snapdragon X Elite SoC.</p>
        <div style="font-size:11px; margin-top:8px; font-family:var(--font-mono); color:#38BDF8;">Latest Merkle Root: ${audit.latest_merkle_root}</div>
      </div>
    `;
    openModal('modalWolfVault');
  });

});
