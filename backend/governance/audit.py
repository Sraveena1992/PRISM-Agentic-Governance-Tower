import os
import json
import hashlib
from datetime import datetime

AUDIT_LOG_FILE = os.path.join(os.path.dirname(__file__), "../../data/audit_trail.jsonl")

class PersistentAuditStore:
    def __init__(self, log_file=AUDIT_LOG_FILE):
        self.log_file = log_file
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w') as f:
                pass  # Initialize file if not exists

    def _get_last_hash(self):
        """Fetch hash of previous entry for tamper-proof chain"""
        last_hash = "0" * 64
        if not os.path.exists(self.log_file) or os.path.getsize(self.log_file) == 0:
            return last_hash
        
        with open(self.log_file, 'r') as f:
            lines = f.readlines()
            if lines:
                last_record = json.loads(lines[-1])
                last_hash = last_record.get("current_hash", last_hash)
        return last_hash

    def log_event(self, audit_id: str, action: str, details: dict):
        """Appends audit event with SHA-256 Merkle-style chain hashing"""
        previous_hash = self._get_last_hash()
        timestamp = datetime.utcnow().isoformat()
        
        payload = {
            "audit_id": audit_id,
            "timestamp": timestamp,
            "action": action,
            "details": details,
            "previous_hash": previous_hash
        }
        
        # Compute SHA-256 hash of payload + previous_hash
        raw_bytes = json.dumps(payload, sort_keys=True).encode('utf-8')
        current_hash = hashlib.sha256(raw_bytes).hexdigest()
        
        payload["current_hash"] = current_hash
        
        with open(self.log_file, 'a') as f:
            f.write(json.dumps(payload) + "\n")
            
        return payload

    def get_audit(self, audit_id: str):
        if not os.path.exists(self.log_file):
            return None
        with open(self.log_file, 'r') as f:
            for line in f:
                record = json.loads(line)
                if record.get("audit_id") == audit_id:
                    return record
        return None

audit_store = PersistentAuditStore()
