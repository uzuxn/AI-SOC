import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from zoneinfo import ZoneInfo
import random
from database import init_db, save_log, get_logs as get_saved_logs
from fastapi.responses import StreamingResponse
import io
import csv
from models_loader import binary_model, multiclass_model, scaler
from risk_engine import calculate_risk_score, classify_risk
from blockchain import blockchain
from schemas import LogInput

app = FastAPI(title="AI-SOC Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logs_storage = []
init_db()

@app.get("/")
def root():
    return {"message": "AI-SOC Backend Running"}


@app.get("/api/dashboard")
def get_dashboard():
    high_risk = sum(
        1 for log in logs_storage
        if log["ai_analysis"]["risk"] in ["High Risk", "Critical"]
    )

    return {
        "total_logs": len(logs_storage),
        "high_risk_alerts": high_risk,
        "events_over_time": [
            {"name": "10:00", "count": random.randint(50, 200)},
            {"name": "10:05", "count": random.randint(50, 200)},
            {"name": "10:10", "count": random.randint(50, 200)},
        ],
        "top_source_ips": [
            {"ip": log["source_ip"], "count": random.randint(1, 50)}
            for log in logs_storage[:5]
        ]
    }


@app.post("/api/ingest-log")
def ingest_log(log: LogInput):
    expected_cols = list(scaler.feature_names_in_)

    input_df = pd.DataFrame([log.features])

    for col in expected_cols:
        if col not in input_df.columns:
            input_df[col] = 0

    input_df = input_df[expected_cols]

    scaled = scaler.transform(input_df)

    binary_pred = binary_model.predict(scaled)[0]
    prob = binary_model.predict_proba(scaled)[0][1]

    attack_type = "Normal"

    if binary_pred == 1:
        multi_pred = multiclass_model.predict(scaled)[0]

        if multi_pred == -1:
            attack_type = "Anomalous Activity"
        else:
            attack_type = str(multi_pred)
        

    threat_reputation = random.uniform(0, 1)
    score = calculate_risk_score(prob, threat_reputation)
    risk_label = classify_risk(score)

    ai_result = {
        "risk": risk_label,
        "score": score,
        "attack_type": str(attack_type)
    }

    log_entry = {
        "id": len(logs_storage) + 1,
        "timestamp": datetime.now(ZoneInfo("Asia/Colombo")).isoformat(),
        "source_ip": log.source_ip,
        "event_type": log.event_type,
        "message": log.message,
        "ai_analysis": ai_result
    }

    logs_storage.insert(0, log_entry)
    save_log(log_entry)

    if risk_label in ["Suspicious", "High Risk", "Critical"]:
        blockchain.add_block(log_entry)

    return log_entry


@app.get("/api/logs")
def get_logs():
    return get_saved_logs()


@app.get("/api/blockchain")
def get_blockchain():
    return blockchain.to_dict()


@app.get("/api/download-logs")
def download_logs():
    logs = get_saved_logs()

    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow([
        "ID", "Timestamp", "Source IP", "Event Type",
        "Message", "Risk", "Score", "Attack Type"
    ])

    for log in logs:
        writer.writerow([
            log["id"],
            log["timestamp"],
            log["source_ip"],
            log["event_type"],
            log["message"],
            log["ai_analysis"]["risk"],
            log["ai_analysis"]["score"],
            log["ai_analysis"]["attack_type"]
        ])

    output.seek(0)

    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=soc_logs.csv"}
    )