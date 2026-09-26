"""
OmniCare AI — System & Hardware Configuration
Snapdragon® AI Lab Build & Present Challenge 2026
Target Hardware: Snapdragon-Powered HP PCs (HP OmniBook X 14 / HP EliteBook Ultra G1q)
"""

import os
from pydantic import BaseModel

class HardwareSpecs(BaseModel):
    soc: str = "Snapdragon X Elite (X1E-80-100)"
    npu: str = "Qualcomm Hexagon NPU (HTP v73)"
    npu_peak_tops: float = 45.0
    small_llm_speed_tok_s: float = 34.2
    target_inference_latency_ms: float = 12.4
    battery_life_hours: float = 26.0
    memory_gb: int = 16
    npu_execution_provider: str = "QNNExecutionProvider"
    npu_precision: str = "INT8 / INT4 mixed precision"
    thermal_profile: str = "HP Smart Sense Dynamic Acoustic/Thermal Governor"

class SecuritySettings(BaseModel):
    enclave_type: str = "HP Wolf Security Enclave"
    encryption_algorithm: str = "AES-256-GCM"
    audit_chaining: str = "SHA-256 Tamper-Evident Merkle Chain"
    cloud_egress: bool = False
    dpdp_act_compliant: bool = True
    abdm_fhir_version: str = "NRCeS India ABDM FHIR R4"

class ServerConfig(BaseModel):
    app_name: str = "OmniCare AI Diagnostic Workstation"
    version: str = "1.0.0"
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False
    hardware: HardwareSpecs = HardwareSpecs()
    security: SecuritySettings = SecuritySettings()

CONFIG = ServerConfig()
