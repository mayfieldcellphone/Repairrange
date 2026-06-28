# 🛠️ DEPLOYMENT RECOVERY INSTRUCTIONS: Project `repairhub-saas`

### **1. The Root Cause of the 48-Hour Failure**
The project was failing because the **Cloud Firestore API** was disabled in the Google Cloud Console. This caused the container to either crash or fail its health checks upon deployment to Cloud Run.

### **2. Pre-Deployment Checklist (Mandatory)**
Before attempting another `gcloud run deploy`:
*   **API Verification**: Ensure the user has clicked "Enable" at this link: [https://console.developers.google.com/apis/api/firestore.googleapis.com/overview?project=repairhub-saas](https://console.developers.google.com/apis/api/firestore.googleapis.com/overview?project=repairhub-saas).
*   **Service Account Permissions**: The Cloud Run Service Account (usually `[project-number]-compute@developer.gserviceaccount.com`) must have the **"Cloud Datastore User"** role. Without this, the app cannot write data even if the API is enabled.
*   **Database Initialization**: Verify the Firestore database has been created in **"Native Mode"** (not Datastore mode) in the Firebase console.

### **3. Codebase State**
*   The persistence logic is currently implemented in `repo_analysis/server.ts` and `repo_analysis/src/lib/firebase.ts`.
*   The UI has been refactored to a **Blue, Green, and Black** high-contrast theme.
*   The onboarding process is a **3-step Power Flow** (Identity -> Knowledge -> Launch).

### **4. Deployment Fix Command**
The next agent should run this specific verification check before deploying:
```bash
# Check if Firestore is reachable from the current environment
node repo_analysis/analyze_logs.mjs
```
If that script returns a clean table of logs, the "Bridge" is open, and you can proceed with the standard Cloud Run deployment.
