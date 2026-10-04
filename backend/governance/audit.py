import os
import json
import hashlib
from datetime import datetime
from typing import Dict, Any, Optional

AUDIT_LOG_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data/audit_trail.jsonl"))

DEFAULT_DEMO_AUDITS = {
    "AUDIT-20261003-151202": {
        "audit_id": "AUDIT-20261003-151202",
        "timestamp": "2026-10-03T15:12:02.506017Z",
        "action": "GOVERNANCE_EVALUATION_APPROVED",
        "details": {
            "audit_id": "AUDIT-20261003-151202",
            "vendor_id": "VEND-APPROVED-001",
            "pipeline_stages_completed": 5,
            "risk_score": 0.2,
            "decision": "APPROVED",
            "requires_human_approval": False,
            "gate_reason": "Low risk profile; auto-approval policy met",
            "retrieved_policies": [
                {"id": "POLICY-004", "text": "Financial fraud history blocks vendor", "similarity_score": 0.4213, "retriever": "TF-IDF Vector + Cosine Matrix"},
                {"id": "POLICY-002", "text": "GST fraud flag leads to high risk and human approval required", "similarity_score": 0.2831, "retriever": "TF-IDF Vector + Cosine Matrix"},
                {"id": "POLICY-005", "text": "Low ESG rating 35 triggers fail-closed gate", "similarity_score": 0.1326, "retriever": "TF-IDF Vector + Cosine Matrix"}
            ],
            "fail_closed_active": True,
            "timestamp": "2026-10-03T15:12:02.505989Z"
        },
        "previous_hash": "0"*64,
        "current_hash": "4744c2c009c4df6fc47d546e4492405cb07eeb6ee2a4fadf93d5b2d92bc6ed28"
    }
}

class AuditStore:
    def __init__(self, log_file: str = AUDIT_LOG_FILE):
        self.log_file = log_file
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
        self._memory_cache: Dict[str, Dict[str, Any]] = {}
        
        # P0 FIX: File is canonical, not memory
        # If file empty, write demo audits INTO FILE
        if not os.path.exists(self.log_file) or os.path.getsize(self.log_file) == 0:
            with open(self.log_file, 'w', encoding='utf-8') as f:
                for record in DEFAULT_DEMO_AUDITS.values():
                    f.write(json.dumps(record) + "\n")
        
        self._load_cache_from_file()

    @property
    def file_path(self) -> str:
        return self.log_file

    def _load_cache_from_file(self):
        if not os.path.exists(self.log_file):
            return
        try:
            with open(self.log_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if not line.strip(): continue
                    record = json.loads(line)
                    if record.get("audit_id"):
                        self._memory_cache[record["audit_id"]] = record
        except Exception:
            pass

    def _get_last_hash(self) -> str:
        default_genesis_hash = "0" * 64
        if not os.path.exists(self.log_file) or os.path.getsize(self.log_file) == 0:
            return default_genesis_hash
        try:
            with open(self.log_file, 'r', encoding='utf-8') as f:
                lines = [l.strip() for l in f if l.strip()]
                if lines:
                    last = json.loads(lines[-1])
                    return last.get("current_hash", default_genesis_hash)
        except Exception:
            pass
        return default_genesis_hash

    def _compute_hash(self, payload_dict: Dict[str, Any]) -> str:
        raw_bytes = json.dumps(payload_dict, sort_keys=True, separators=(',', ':')).encode('utf-8')
        return hashlib.sha256(raw_bytes).hexdigest()

    def log_event(self, audit_id: str, action: str, details: Dict[str, Any]) -> Dict[str, Any]:
        previous_hash = self._get_last_hash()
        timestamp = datetime.utcnow().isoformat() + "Z"
        payload = {
            "audit_id": audit_id,
            "timestamp": timestamp,
            "action": action,
            "details": details,
            "previous_hash": previous_hash
        }
        payload["current_hash"] = self._compute_hash(payload)
        self._memory_cache[audit_id] = payload
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(payload) + "\n")
        except Exception as e:
            print(f"File write warning: {e}")
        return payload

    def get_audit(self, audit_id: str) -> Optional[Dict[str, Any]]:
        return self._memory_cache.get(audit_id)

    # P0 FIX: Return DICT with proper contract
    def verify_chain(self) -> Dict[str, Any]:
        if not os.path.exists(self.log_file) or os.path.getsize(self.log_file) == 0:
            return {"is_valid": True, "count": 0, "message": "Empty chain - Genesis intact", "chain_status": "INTACT"}

        expected_prev = "0"*64
        lines = []
        with open(self.log_file, 'r', encoding='utf-8') as f:
            lines = [l.strip() for l in f if l.strip()]

        for idx, line in enumerate(lines):
            try:
                record = json.loads(line)
            except:
                return {"is_valid": False, "count": len(lines), "message": f"Corrupt JSON at {idx}", "chain_status": "TAMPERED"}

            if record.get("previous_hash") != expected_prev:
                return {"is_valid": False, "count": len(lines), "message": f"Chain broken at {idx} ({record.get('audit_id')}) Expected {expected_prev[:8]}.. found {record.get('previous_hash','')[:8]}..", "chain_status": "TAMPERED"}

            payload_to_verify = {
                "audit_id": record.get("audit_id"),
                "timestamp": record.get("timestamp"),
                "action": record.get("action"),
                "details": record.get("details"),
                "previous_hash": record.get("previous_hash")
            }
            recalculated = self._compute_hash(payload_to_verify)
            if recalculated != record.get("current_hash"):
                return {"is_valid": False, "count": len(lines), "message": f"Tampering at {record.get('audit_id')} Stored {record.get('current_hash','')[:8]}.. != {recalculated[:8]}..", "chain_status": "TAMPERED"}

            expected_prev = record.get("current_hash")

        return {"is_valid": True, "count": len(lines), "message": "Full cryptographic verification passed", "chain_status": "INTACT"}

PersistentAuditStore = AuditStore
audit_store = AuditStore()
