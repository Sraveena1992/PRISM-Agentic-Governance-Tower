import os
import json
import hashlib
from datetime import datetime
from typing import Tuple, Dict, Any, Optional

AUDIT_LOG_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data/audit_trail.jsonl"))


class AuditStore:
    def __init__(self, log_file: str = AUDIT_LOG_FILE):
        self.log_file = log_file
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w', encoding='utf-8') as f:
                pass  # Initialize empty file if not exists

    @property
    def file_path(self) -> str:
        return self.log_file

    def _get_last_hash(self) -> str:
        """Fetch current_hash of the previous entry for tamper-evident chaining."""
        default_genesis_hash = "0" * 64
        if not os.path.exists(self.log_file) or os.path.getsize(self.log_file) == 0:
            return default_genesis_hash

        with open(self.log_file, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip()]
            if lines:
                try:
                    last_record = json.loads(lines[-1])
                    return last_record.get("current_hash", default_genesis_hash)
                except json.JSONDecodeError:
                    return default_genesis_hash
        return default_genesis_hash

    def _compute_hash(self, payload_dict: Dict[str, Any]) -> str:
        """Helper to compute deterministic canonical SHA-256 hash of record payload."""
        raw_bytes = json.dumps(payload_dict, sort_keys=True, separators=(',', ':')).encode('utf-8')
        return hashlib.sha256(raw_bytes).hexdigest()

    def log_event(self, audit_id: str, action: str, details: Dict[str, Any]) -> Dict[str, Any]:
        """Appends governance audit event with cryptographically linked SHA-256 hash chain."""
        previous_hash = self._get_last_hash()
        timestamp = datetime.utcnow().isoformat() + "Z"

        payload = {
            "audit_id": audit_id,
            "timestamp": timestamp,
            "action": action,
            "details": details,
            "previous_hash": previous_hash
        }

        # Compute SHA-256 hash on canonical payload format
        current_hash = self._compute_hash(payload)
        payload["current_hash"] = current_hash

        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(payload) + "\n")

        return payload

    def get_audit(self, audit_id: str) -> Optional[Dict[str, Any]]:
        """Fetch audit record by audit_id."""
        if not os.path.exists(self.log_file):
            return None
        with open(self.log_file, 'r', encoding='utf-8') as f:
            for line in f:
                if not line.strip():
                    continue
                try:
                    record = json.loads(line)
                    if record.get("audit_id") == audit_id:
                        return record
                except json.JSONDecodeError:
                    continue
        return None

    def verify_chain(self) -> Tuple[bool, str]:
        """
        Cryptographic Integrity Recalculation Loop.
        Reads all records head-to-tail and verifies:
        1. Linkage: record[i].previous_hash == record[i-1].current_hash
        2. Recalculated Hash: sha256(payload) == record[i].current_hash
        """
        if not os.path.exists(self.log_file) or os.path.getsize(self.log_file) == 0:
            return True, "Audit log is empty. Genesis hash sequence intact."

        expected_previous_hash = "0" * 64

        with open(self.log_file, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip()]

        for idx, line in enumerate(lines):
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                return False, f"Corruption detected: Malformed JSON at record index {idx}."

            stored_current_hash = record.get("current_hash")
            stored_previous_hash = record.get("previous_hash")

            # Check 1: Chain Linkage Integrity
            if stored_previous_hash != expected_previous_hash:
                return False, (
                    f"Chain broken at record index {idx} (Audit ID: {record.get('audit_id')}). "
                    f"Expected previous hash {expected_previous_hash[:8]}..., "
                    f"found {stored_previous_hash[:8]}..."
                )

            # Reconstruct exact payload to recalculate SHA-256 hash
            payload_to_verify = {
                "audit_id": record.get("audit_id"),
                "timestamp": record.get("timestamp"),
                "action": record.get("action"),
                "details": record.get("details"),
                "previous_hash": stored_previous_hash
            }

            recalculated_hash = self._compute_hash(payload_to_verify)

            # Check 2: Hash Tampering Integrity
            if recalculated_hash != stored_current_hash:
                return False, (
                    f"Tampering detected at record index {idx} (Audit ID: {record.get('audit_id')}). "
                    f"Stored hash: {stored_current_hash[:8]}..., Recalculated hash: {recalculated_hash[:8]}..."
                )

            # Move forward in chain
            expected_previous_hash = stored_current_hash

        return True, f"Full cryptographic verification passed across {len(lines)} ledger entries."


# Export Class and Singleton Instance
PersistentAuditStore = AuditStore  # Backwards compatibility alias
audit_store = AuditStore()
