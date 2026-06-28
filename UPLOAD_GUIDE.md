# AI Bot Training: Upload Guide

To train your chatbot with the most accurate information, use the provided CSV template. Here is how to fill it out:

### 📋 Field Definitions

| Column | Description | Example |
| :--- | :--- | :--- |
| **Brand** | The manufacturer of the device. | Apple, Samsung, Oppo |
| **Model** | The specific device name. | iPhone 15 Pro, Galaxy S24 |
| **Repair_Type** | The part or service being offered. | Screen, Battery, Charging Port |
| **Quality_Tier** | The grade of the part. | Elite (OEM), Pro (OLED), Budget |
| **Price_AUD** | Your retail price including margin. | 189 |
| **Warranty** | Your guarantee period. | 90 Days |
| **Stock_Status** | Current availability. | In Stock, 2-day lead time |
| **Description** | Key selling points or technical notes. | True Tone support, tools included |

### 🚀 How to Upload
1.  Open [PRICE_LIST_TEMPLATE.csv](PRICE_LIST_TEMPLATE.csv) in Excel or Google Sheets.
2.  Add your products following the format.
3.  Save as **CSV (Comma Separated Values)**.
4.  Upload or paste the content into the AI Builder Bot Setup Wizard.

### 💡 Pro-Tips for Training
*   **Be Consistent**: Use the same naming for tiers (e.g., don't mix "Elite" and "Original" across rows).
*   **Add "None"**: If a field doesn't apply (like tier for a charging cable), put "N/A" or "Standard".
*   **Formatting**: Do not use currency symbols ($) in the Price column; just use the number.
