# Incoming Request Processing Workflow POC

An automated, AI-driven **Incoming Customer Support Request Processing Engine** designed to ingest, classify, extract entities from, and execute multi-branch remediation workflows for incoming customer emails and tickets.

Built using Hugging Face's `Tobi-Bueck/customer-support-tickets` dataset (61.8k real support tickets), Scikit-Learn machine learning classifiers, regex entity extractors, a RAG FAQ knowledge engine, and an interactive Streamlit UI dashboard.

**Author & Lead Engineer**: Yashasvi Verma

---

## 🏗️ Architecture & Workflow Design

The pipeline processes incoming customer tickets through 6 automated stages:

```
[ Incoming Request (Form / Batch File / Simulated Inbox) ]
                          │
                          ▼
        [ 1. Preprocessing & Text Merging ]
                          │
                          ▼
       [ 2. Multi-Model Inference Engine ]
    ( Queue / Intent + Priority + Ticket Type )
                          │
                          ▼
       [ 3. Entity & Keyword Extraction ]
     ( Email, Account ID, Seats, Product, Deadline )
                          │
                          ▼
        [ 4. Multi-Branch Workflow Routing ]
 ( Complaint / Incident / Service Request / Inquiry )
                          │
                          ▼
      [ 5. Remediation & Action Execution ]
   ( Draft Response + Team Routing + SLA Timer )
                          │
                          ▼
    [ 6. Persistence & Audit Logging (SQLite) ]
```

---

## 🤖 Classification Logic & Confidence Scoring

1. **Queue (Intent) Classification**: TF-IDF vectorization (10,000 max features, English stop-words) + Linear SVM / Random Forest hyperparameter-tuned champion model classifying requests into 8+ queue departments (e.g., `Technical Support`, `Billing and Payments`, `Customer Service`, `Sales`).
2. **Priority (Urgency) Classification**: TF-IDF + Classifier categorizing urgency into `Low`, `Medium`, or `High / Critical`.
3. **Ticket Type Classification**: Classifier predicting operational types (`Incident`, `Request`, `Problem`, `Change`).
4. **Confidence Threshold & Escalation Override**: Overall confidence score is calculated across models. If confidence drops below 0.35 or contains high-risk outage signals, the system flags a `⚠️ LOW CONFIDENCE / HUMAN REVIEW ALERT` for manual operator review.

---

## 🛠️ Remediation Strategies by Request Branch

| Branch | Classification Condition | Remediation Strategy & Executed Actions | SLA Follow-Up |
| :--- | :--- | :--- | :--- |
| **Complaint / Escalation** | High Urgency, Damaged Product, Refund Request, or Complaint Tag | 1) Draft formal apology email with refund & replacement policy.<br>2) Escalate ticket to Senior Support Manager.<br>3) Log case in CRM DB with High Priority flag.<br>4) Set 2-Hour SLA follow-up reminder. | **2-Hour Manager Follow-up** |
| **Technical Incident** | Server Outage, System Down, Critical Incident | 1) Flag Urgent (Critical/High priority).<br>2) Dispatch emergency alerts to Supervisor & Tech Analysts via Slack/Email.<br>3) Draft urgent acknowledgement email.<br>4) PAUSE automated resolution (Mandate human engineer intervention). | **Immediate Alert (Target: 1 Hour)** |
| **Service Request** | License Upgrade, Software Install, Account Provisioning | 1) Extract details (Software, User count/seats, Deadline).<br>2) Route request ticket to IT Support / Sales team.<br>3) Generate auto-acknowledgement email.<br>4) Set 24-Hour SLA provisioning timer. | **24-Hour Provisioning SLA** |
| **General Inquiry** | Hours of Operation, General Questions, Info Requests | 1) Match query against Knowledge Base FAQ.<br>2) Auto-generate factual response.<br>3) Dispatch outbound email reply.<br>4) Mark ticket as RESOLVED in system. | **Auto-Closed** |

---

## 🛠️ Tools & Technologies Used

- **Core Engine & Language**: Python 3.14
- **Web App UI**: Streamlit
- **Machine Learning**: Scikit-learn (TF-IDF Vectorizer, LinearSVC, RandomForestClassifier, LabelEncoder, GridSearchCV)
- **Data Manipulation**: Pandas, NumPy
- **Persistence & Logging**: SQLite3, JSON, Python `logging` module
- **Dataset**: Hugging Face `Tobi-Bueck/customer-support-tickets` (61.8k records)

---

## 📂 End-to-End Examples per Branch Type

### Example 1: Complaint / Escalation Branch
- **Input Subject**: `Broken item – need refund`
- **Input Body**: `I received a damaged gadget yesterday, and customer service hasn't responded. This is unacceptable!`
- **Classification**: Queue: `Customer Service` | Priority: `High` | Type: `Request` (Confidence: 44.8%)
- **Branch**: `Complaint / Escalation` | **Status**: `Escalated to Management`
- **Extracted Entities**: `urgency_signals: ["unacceptable"]`
- **Actions Executed**:
  1. Drafted formal apology email with refund & replacement info.
  2. Escalated ticket to Senior Support Manager.
  3. Logged case in CRM database with High Priority tag.
  4. Set 2-Hour SLA follow-up reminder.
- **Drafted Response**:
  > *Dear Valued Customer, We sincerely apologize for the experience you encountered. Your issue has been escalated with HIGH PRIORITY to our Senior Support Management team...*

---

### Example 2: Technical Outage Incident Branch
- **Input Subject**: `System Outage – URGENT`
- **Input Body**: `Our servers are down and customers can't login. This is critical!`
- **Classification**: Queue: `Technical Support` | Priority: `High` | Type: `Incident` (Confidence: 48.6%)
- **Branch**: `Technical Incident` | **Status**: `In Progress (Incident Active)`
- **Extracted Entities**: `urgency_signals: ["outage", "down", "critical", "urgent"]`
- **Actions Executed**:
  1. Urgent flag assigned (Critical/High priority).
  2. Emergency alert dispatched to Supervisor and Technical Analysts via Slack/Email.
  3. Urgent acknowledgement email drafted and queued.
  4. Automated resolution PAUSED (Human-in-the-loop mandated).
- **Drafted Response**:
  > *URGENT TICKET ACKNOWLEDGEMENT: We have received your incident report regarding system issues/outage. Our technical operations and engineering teams have been alerted immediately...*

---

### Example 3: Service Request Branch
- **Input Subject**: `Install new software license`
- **Input Body**: `Hello, I need to upgrade to Premium Edition for 10 more users by next Monday.`
- **Classification**: Queue: `Technical Support` | Priority: `Medium` | Type: `Request` (Confidence: 48.5%)
- **Branch**: `Service Request` | **Status**: `Routed to Operations`
- **Extracted Entities**: `software_or_product: "Premium Edition"`, `deadline: "next Monday"`
- **Actions Executed**:
  1. Extracted details: Software='Premium Edition', Seats='N/A', Deadline='next Monday'.
  2. Routed request ticket to [Technical Support] team.
  3. Auto-acknowledgement email generated and sent to customer.
  4. 24-Hour SLA provisioning timer created.
- **Drafted Response**:
  > *Hello, Thank you for submitting your service request. We have captured your request details (Software: Premium Edition, Target Timeline: next Monday). Your request has been routed...*

---

### Example 4: General Inquiry Branch
- **Input Subject**: `Hours of operation`
- **Input Body**: `Hi, just wanted to know if you're open on weekends.`
- **Classification**: Queue: `Customer Support` | Priority: `Low` | Type: `Request` (Confidence: 48.7%)
- **Branch**: `General Inquiry` | **Status**: `Resolved`
- **Extracted Entities**: None
- **Actions Executed**:
  1. Query matched against Knowledge Base FAQ: 'Hours of Operation'.
  2. Auto-generated factual reply.
  3. Outbound email dispatched to customer.
  4. Ticket marked as RESOLVED in system.
- **Drafted Response**:
  > *Hi there, Our customer support and operational hours are Monday to Friday, 8:00 AM – 8:00 PM EST. On weekends, our automated service handles requests, and emergency technical support remains active 24/7.*

---

## 🚀 Quickstart & How to Run

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run Initialization & Model Training**:
   ```bash
   python app/main.py
   ```

3. **Run 5-Scenario Pipeline Validation**:
   ```bash
   python validate_pipeline.py
   ```

4. **Launch Interactive Streamlit Web UI**:
   ```bash
   streamlit run app/dashboard.py
   ```
