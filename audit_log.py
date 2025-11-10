"""
Audit Log Module
Tracks all generation requests, policy decisions, and outcomes.
"""

import json
from datetime import datetime
from typing import Dict, List, Optional
import os


class AuditLog:
    """Audit logging for FIBO BrandGuard operations."""
    
    def __init__(self, log_file: str = "audit_log.json"):
        """
        Initialize audit log.
        
        Args:
            log_file: Path to audit log file
        """
        self.log_file = log_file
        self.entries = []
        self._load_log()
    
    def _load_log(self):
        """Load existing audit log from file."""
        if os.path.exists(self.log_file):
            try:
                with open(self.log_file, 'r') as f:
                    self.entries = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                self.entries = []
    
    def _save_log(self):
        """Save audit log to file."""
        try:
            with open(self.log_file, 'w') as f:
                json.dump(self.entries, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save audit log: {e}")
    
    def log_generation_request(
        self,
        prompt: Dict,
        policy_decision: Dict,
        user: str = "default_user"
    ) -> str:
        """
        Log a generation request.
        
        Args:
            prompt: The prompt used
            policy_decision: Policy validation results
            user: User who made the request
            
        Returns:
            Entry ID
        """
        entry_id = f"gen_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
        
        entry = {
            "id": entry_id,
            "timestamp": datetime.now().isoformat(),
            "type": "generation_request",
            "user": user,
            "prompt": prompt,
            "policy_decision": policy_decision,
            "status": "approved" if policy_decision.get("is_valid", False) else "rejected"
        }
        
        self.entries.append(entry)
        self._save_log()
        
        return entry_id
    
    def log_generation_result(
        self,
        entry_id: str,
        results: List[Dict],
        success: bool = True
    ):
        """
        Log generation results.
        
        Args:
            entry_id: ID of the generation request entry
            results: List of generation results
            success: Whether generation was successful
        """
        entry = {
            "id": f"{entry_id}_result",
            "timestamp": datetime.now().isoformat(),
            "type": "generation_result",
            "request_id": entry_id,
            "success": success,
            "num_variants": len(results),
            "results_summary": [
                {
                    "variant_id": r.get("variant_id"),
                    "status": r.get("status"),
                    "generation_time": r.get("generation_time")
                }
                for r in results
            ]
        }
        
        self.entries.append(entry)
        self._save_log()
    
    def log_policy_violation(
        self,
        prompt: Dict,
        violations: List[str],
        user: str = "default_user"
    ):
        """
        Log a policy violation.
        
        Args:
            prompt: The prompt that violated policy
            violations: List of violations
            user: User who made the request
        """
        entry = {
            "id": f"violation_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}",
            "timestamp": datetime.now().isoformat(),
            "type": "policy_violation",
            "user": user,
            "prompt": prompt,
            "violations": violations,
            "severity": "high" if len(violations) > 2 else "medium"
        }
        
        self.entries.append(entry)
        self._save_log()
    
    def get_recent_entries(self, limit: int = 10) -> List[Dict]:
        """
        Get recent audit log entries.
        
        Args:
            limit: Maximum number of entries to return
            
        Returns:
            List of recent entries
        """
        return self.entries[-limit:] if self.entries else []
    
    def get_statistics(self) -> Dict:
        """
        Get audit log statistics.
        
        Returns:
            Dictionary with statistics
        """
        total = len(self.entries)
        
        generation_requests = [e for e in self.entries if e.get("type") == "generation_request"]
        approved = [e for e in generation_requests if e.get("status") == "approved"]
        rejected = [e for e in generation_requests if e.get("status") == "rejected"]
        violations = [e for e in self.entries if e.get("type") == "policy_violation"]
        
        return {
            "total_entries": total,
            "generation_requests": len(generation_requests),
            "approved_requests": len(approved),
            "rejected_requests": len(rejected),
            "policy_violations": len(violations),
            "approval_rate": len(approved) / len(generation_requests) * 100 if generation_requests else 0
        }
    
    def clear_log(self):
        """Clear all audit log entries."""
        self.entries = []
        self._save_log()
