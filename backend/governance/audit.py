import os, json, hashlib, uuid
from datetime import datetime
from typing import Dict, Any, List

class AuditStore:
    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.file_path = os.path.join(base_dir, "../audit/audit_chain.json")
        self.file_path = os.path.abspath(self.file_path)
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as f:
                json.dump([], f)

    def _load(self) -> List[Dict]:
        try:
            with open(self.file_path, 'r') as f:
                data = json.load(f)
                return data if isinstance(data, list) else data.get("trail", [])
        except:
            return []

    def _save(self, data: List[Dict]):
        with open(self.file_path, 'w') as f:
            json.dump(data, f, indent=2)

    def _hash(self, record: Dict) -> str:
        # Canonical JSON without current_hash itself
        copy = {k: v for k, v in record.items() if k!= "current_hash"}
        s = json.dumps(copy, sort_keys=True, default=str)
        return hashlib.sha256(s.encode()).hexdigest()

    def log_event(self, audit_id: str, action: str, details: Dict) -> Dict:
        chain = self._load()
        prev_hash = chain[-1].get("current_hash", "GENESIS") if chain else "GENESIS"
        entry = {
            "id": audit_id,
            "audit_id": audit_id,
            "action": action,
            "vendor_id": details.get("vendor_id", "UNKNOWN"),
            "details": details,
            "timestamp": datetime.utcnow().isoformat(),
            "previous_hash": prev_hash,
            "decision": details.get("governance", {}).get("decision", "REVIEW"),
            "risk_score": details.get("governance", {}).get("risk_score", 0.5)
        }
        entry["current_hash"] = self._hash(entry)
        chain.append(entry)
        self._save(chain)
        return entry

    def add_record(self, record: Dict) -> Dict:
        chain = self._load()
        prev_hash = chain[-1].get("current_hash", "GENESIS") if chain else "GENESIS"
        audit_id = record.get("audit_id", f"AUD-{uuid.uuid4().hex[:6].upper()}")
        entry = {
            "id": audit_id,
            "audit_id": audit_id,
            "vendor_id": record.get("vendor_id", "UNKNOWN"),
            "decision": record.get("decision", "REVIEW"),
            "risk_score": record.get("risk_score", 0.5),
            "action": record.get("action", "NO_ACTION"),
            "timestamp": datetime.utcnow().isoformat(),
            "previous_hash": prev_hash,
            **record
        }
        entry["current_hash"] = self._hash(entry)
        chain.append(entry)
        self._save(chain)
        return entry

    def get_full_trail(self):
        chain = self._load()
        return {"trail": chain, "count": len(chain)}

    def get_trail(self):
        return self.get_full_trail()

    def get_all(self):
        return self._load()

    def get_by_id(self, audit_id: str):
        for r in self._load():
            if r.get("audit_id") == audit_id or r.get("id") == audit_id:
                return r
        return None

    # --- P0 #2 FINAL FIX: REAL VERIFICATION ---
    def verify_chain(self):
        chain = self._load()
        if not chain:
            return {"is_valid": True, "verified": True, "count": 0, "records_checked": 0, "message": "Empty chain valid", "chain_status": "INTACT"}

        for i, record in enumerate(chain):
            stored_hash = record.get("current_hash")
            # CHECK 1: Recompute hash of record itself
            expected_hash = self._hash(record)
            if stored_hash!= expected_hash:
                return {
                    "is_valid": False, "verified": False,
                    "count": len(chain), "records_checked": len(chain),
                    "chain_status": "TAMPERED",
                    "message": f"TAMPERED at index {i}: Record mutation detected. Expected {expected_hash[:8]}... got {stored_hash[:8]}...",
                    "tampered_index": i
                }
            # CHECK 2: Linkage
            if i > 0:
                if record.get("previous_hash")!= chain[i-1].get("current_hash"):
                    return {
                        "is_valid": False, "verified": False,
                        "count": len(chain), "records_checked": len(chain),
                        "chain_status": "TAMPERED",
                        "message": f"TAMPERED at index {i}: previous_hash linkage broken",
                        "tampered_index": i
                    }

        return {
            "is_valid": True, "verified": True,
            "count": len(chain), "records_checked": len(chain),
            "chain_status": "INTACT",
            "algorithm": "SHA-256",
            "message": "Full cryptographic verification passed - SHA-256 chain INTACT"
        }

audit_store = AuditStore()
