"""
OmniCare AI — ABDM Store-and-Forward Offline Sync Engine
Enables transactional offline queuing for field clinics, rural health camps, and off-grid triage stations.
"""

import time
import uuid
from typing import List, Dict, Any

class OfflineSyncEngine:
    def __init__(self):
        self.queue: List[Dict[str, Any]] = []
        self.synced_history: List[Dict[str, Any]] = []
        self.online_mode: bool = False

    def enqueue_transaction(self, tx_type: str, patient_id: str, payload: dict) -> dict:
        tx_id = f"TX-{uuid.uuid4().hex[:8].upper()}"
        item = {
            "tx_id": tx_id,
            "tx_type": tx_type,
            "patient_id": patient_id,
            "payload_summary": f"{tx_type} for {patient_id}",
            "queued_at": time.time(),
            "status": "QUEUED_OFFLINE",
            "retry_count": 0
        }
        self.queue.append(item)
        return item

    def get_queue_status(self) -> dict:
        return {
            "online_mode": self.online_mode,
            "pending_count": len(self.queue),
            "synced_count": len(self.synced_history),
            "pending_transactions": self.queue[-10:],
            "latest_sync_timestamp": self.synced_history[-1]["synced_at"] if self.synced_history else None
        }

    def trigger_sync(self) -> dict:
        """Simulates atomic store-and-forward batch transaction synchronization."""
        count = len(self.queue)
        for item in self.queue:
            item["status"] = "SYNCED_COMPLIANT"
            item["synced_at"] = time.time()
            self.synced_history.append(item)
        self.queue.clear()
        return {
            "status": "SUCCESS",
            "synced_items_count": count,
            "timestamp": time.time()
        }

_sync_engine = OfflineSyncEngine()

def get_sync_engine() -> OfflineSyncEngine:
    return _sync_engine
