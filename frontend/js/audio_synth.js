/**
 * OmniCare AI — Web Audio API Stethoscopy & Cardiac Acoustic Synthesizer
 * Qualcomm Snapdragon® AI Lab Build & Present Challenge 2026
 * Real-time on-device acoustic synthesis for vesicular sounds, wheezes, crackles, and heartbeats.
 */

class ClinicalAudioSynthesizer {
  constructor() {
    this.audioCtx = null;
    this.activeNodes = [];
    this.isPlaying = false;
  }

  init() {
    if (!this.audioCtx) {
      const AudioContext = window.AudioContext || window.webkitAudioContext;
      this.audioCtx = new AudioContext();
    }
    if (this.audioCtx.state === 'suspended') {
      this.audioCtx.resume();
    }
  }

  stopAll() {
    this.activeNodes.forEach(node => {
      try {
        if (node.stop) node.stop();
        node.disconnect();
      } catch (e) {
        // Ignored if already stopped
      }
    });
    this.activeNodes = [];
    this.isPlaying = false;
  }

  /**
   * Generates a buffer of bandpass-filtered noise simulating pulmonary vesicular airflow.
   */
  createNoiseBuffer(duration, filterFreq = 200, q = 1.0) {
    const bufferSize = this.audioCtx.sampleRate * duration;
    const buffer = this.audioCtx.createBuffer(1, bufferSize, this.audioCtx.sampleRate);
    const data = buffer.getChannelData(0);

    let lastOut = 0.0;
    for (let i = 0; i < bufferSize; i++) {
      const white = Math.random() * 2 - 1;
      // Simple one-pole low-pass pink filter approximation
      lastOut = (lastOut + 0.02 * white) / 1.02;
      data[i] = lastOut * 3.5;
    }
    return buffer;
  }

  /**
   * Plays simulated pulmonary sounds:
   * - 'pneumonia_crackles': Vesicular airflow + late-inspiratory high-frequency explosive pops.
   * - 'copd_wheezes': Airflow + continuous musical multi-tone sinusoids (380-450 Hz).
   * - 'croup_stridor': Harsh, high-pitched monophonic inspiratory sound (600 Hz).
   * - 'normal_vesicular': Gentle rustling airflow.
   */
  playSound(type = 'pneumonia_crackles', duration = 3.5) {
    this.init();
    this.stopAll();
    this.isPlaying = true;

    const now = this.audioCtx.currentTime;

    // Base vesicular airflow breath sound
    const noiseBuffer = this.createNoiseBuffer(duration);
    const noiseSource = this.audioCtx.createBufferSource();
    noiseSource.buffer = noiseBuffer;

    const bandpass = this.audioCtx.createBiquadFilter();
    bandpass.type = 'bandpass';
    bandpass.frequency.setValueAtTime(220, now);
    bandpass.Q.setValueAtTime(1.2, now);

    const gainNode = this.audioCtx.createGain();
    // Respiratory cycle envelope: Inspiration (rise), Expiration (fall)
    gainNode.gain.setValueAtTime(0.01, now);
    gainNode.gain.linearRampToValueAtTime(0.35, now + duration * 0.45); // Peak inspiration
    gainNode.gain.linearRampToValueAtTime(0.05, now + duration * 0.55); // Transition pause
    gainNode.gain.linearRampToValueAtTime(0.25, now + duration * 0.85); // Expiration
    gainNode.gain.linearRampToValueAtTime(0.001, now + duration);

    noiseSource.connect(bandpass);
    bandpass.connect(gainNode);
    gainNode.connect(this.audioCtx.destination);

    noiseSource.start(now);
    noiseSource.stop(now + duration);
    this.activeNodes.push(noiseSource);

    // Overlay specific acoustic pathologies
    if (type.includes('crackles')) {
      // Late-inspiratory explosive crackle spikes between 60% and 85% of inspiration
      const inspTime = duration * 0.45;
      const crackleCount = 12;
      for (let i = 0; i < crackleCount; i++) {
        const crackleStart = now + (inspTime * 0.6) + (Math.random() * (inspTime * 0.35));
        const osc = this.audioCtx.createOscillator();
        const crackleGain = this.audioCtx.createGain();

        osc.type = 'triangle';
        osc.frequency.setValueAtTime(500 + Math.random() * 350, crackleStart);

        crackleGain.gain.setValueAtTime(0.4, crackleStart);
        crackleGain.gain.exponentialRampToValueAtTime(0.001, crackleStart + 0.025); // 25ms click

        osc.connect(crackleGain);
        crackleGain.connect(this.audioCtx.destination);

        osc.start(crackleStart);
        osc.stop(crackleStart + 0.03);
        this.activeNodes.push(osc);
      }
    } else if (type.includes('wheeze')) {
      // Expiratory musical wheezing (starts at 55% of duration)
      const wheezeStart = now + duration * 0.55;
      const wheezeDur = duration * 0.35;

      const osc = this.audioCtx.createOscillator();
      const wheezeGain = this.audioCtx.createGain();

      osc.type = 'sine';
      osc.frequency.setValueAtTime(420, wheezeStart);
      osc.frequency.linearRampToValueAtTime(390, wheezeStart + wheezeDur);

      wheezeGain.gain.setValueAtTime(0.001, wheezeStart);
      wheezeGain.gain.linearRampToValueAtTime(0.28, wheezeStart + 0.1);
      wheezeGain.gain.linearRampToValueAtTime(0.28, wheezeStart + wheezeDur - 0.1);
      wheezeGain.gain.linearRampToValueAtTime(0.001, wheezeStart + wheezeDur);

      osc.connect(wheezeGain);
      wheezeGain.connect(this.audioCtx.destination);

      osc.start(wheezeStart);
      osc.stop(wheezeStart + wheezeDur);
      this.activeNodes.push(osc);
    } else if (type.includes('stridor')) {
      // Inspiratory harsh musical stridor
      const osc = this.audioCtx.createOscillator();
      const stridorGain = this.audioCtx.createGain();

      osc.type = 'sawtooth';
      osc.frequency.setValueAtTime(640, now + 0.1);

      stridorGain.gain.setValueAtTime(0.001, now);
      stridorGain.gain.linearRampToValueAtTime(0.22, now + duration * 0.25);
      stridorGain.gain.linearRampToValueAtTime(0.001, now + duration * 0.5);

      osc.connect(stridorGain);
      stridorGain.connect(this.audioCtx.destination);

      osc.start(now + 0.1);
      osc.stop(now + duration * 0.5);
      this.activeNodes.push(osc);
    }

    setTimeout(() => {
      this.isPlaying = false;
    }, duration * 1000);
  }
}

// Global instance
window.clinicalAudioSynth = new ClinicalAudioSynthesizer();
