import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List

from app.utils.config import Config
from app.utils.logger import Logger


class AuditLogger:
    """
    Audit Logger for recording request handling decisions into SQLite database and JSON log file.
    """

    def __init__(self):
        self.logger = Logger.get_logger()
        self.db_path = Config.DATA_DIR / "audit_log.db"
        self.json_path = Config.LOGS_DIR / "audit_log.json"
        
        Config.DATA_DIR.mkdir(parents=True, exist_ok=True)
        Config.LOGS_DIR.mkdir(parents=True, exist_ok=True)
        
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS audit_logs (
                request_id TEXT PRIMARY KEY,
                timestamp TEXT,
                subject TEXT,
                queue TEXT,
                priority TEXT,
                ticket_type TEXT,
                confidence REAL,
                branch TEXT,
                actions TEXT,
                extracted_entities TEXT,
                response TEXT,
                status TEXT,
                sla_timer TEXT
            )
        """)
        # Add column if migrating existing database file
        try:
            cursor.execute("ALTER TABLE audit_logs ADD COLUMN sla_timer TEXT")
        except Exception:
            pass

        conn.commit()
        conn.close()

    def log_execution(self, record: Dict[str, Any]):
        request_id = record.get("request_id", f"REQ-{int(datetime.now().timestamp())}")
        timestamp = record.get("timestamp", datetime.now().isoformat())
        subject = record.get("subject", "")
        queue = record.get("queue", "")
        priority = record.get("priority", "")
        ticket_type = record.get("type", "")
        confidence = record.get("confidence", 0.0)
        branch = record.get("branch", "")
        actions = json.dumps(record.get("actions", []))
        extracted_entities = json.dumps(record.get("extracted_entities", {}))
        response = record.get("response", "")
        status = record.get("status", "Processed")
        sla_timer = record.get("sla_timer", "N/A")

        # Save to SQLite
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO audit_logs 
                (request_id, timestamp, subject, queue, priority, ticket_type, confidence, branch, actions, extracted_entities, response, status, sla_timer)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (request_id, timestamp, subject, queue, priority, ticket_type, confidence, branch, actions, extracted_entities, response, status, sla_timer))
            conn.commit()
            conn.close()
        except Exception as e:
            self.logger.error(f"Error writing to SQLite audit log: {e}")

        # Append to JSON log file
        try:
            logs = []
            if self.json_path.exists() and self.json_path.stat().st_size > 0:
                with open(self.json_path, "r", encoding="utf-8") as f:
                    logs = json.load(f)
            
            record_copy = record.copy()
            record_copy["request_id"] = request_id
            record_copy["timestamp"] = timestamp
            logs.append(record_copy)

            with open(self.json_path, "w", encoding="utf-8") as f:
                json.dump(logs, f, indent=2)
        except Exception as e:
            self.logger.error(f"Error writing to JSON audit log: {e}")

        self.logger.info(f"Logged request {request_id} under branch [{branch}] to audit history.")

    def get_recent_logs(self, limit: int = 50) -> List[Dict[str, Any]]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT request_id, timestamp, subject, queue, priority, ticket_type, confidence, branch, actions, extracted_entities, response, status, sla_timer FROM audit_logs ORDER BY timestamp DESC LIMIT ?", (limit,))
        rows = cursor.fetchall()
        conn.close()

        logs = []
        for r in rows:
            logs.append({
                "request_id": r[0],
                "timestamp": r[1],
                "subject": r[2],
                "queue": r[3],
                "priority": r[4],
                "type": r[5],
                "confidence": r[6],
                "branch": r[7],
                "actions": json.loads(r[8]) if r[8] else [],
                "extracted_entities": json.loads(r[9]) if r[9] else {},
                "response": r[10],
                "status": r[11],
                "sla_timer": r[12] if len(r) > 12 and r[12] else "N/A"
            })
        return logs
