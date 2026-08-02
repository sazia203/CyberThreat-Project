import json
import os

# ফাইল পাথ নির্দেশ করা
RAW_FILE_PATH = os.path.join('dataset', 'raw', 'cisa_kev.json')
PROCESSED_FILE_PATH = os.path.join('dataset', 'processed', 'clean_vulnerabilities.json')

def optimize_and_process_data():
    if not os.path.exists(RAW_FILE_PATH):
        print(f"❌ Error: Raw file not found at {RAW_FILE_PATH}")
        return

    print("🔄 Processing and optimizing CISA KEV data...")

    with open(RAW_FILE_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    vulnerabilities = data.get('vulnerabilities', [])
    
    seen_cves = set()
    cleaned_data = []

    for item in vulnerabilities:
        cve_id = item.get('cveID')
        
        # ১. ডুপ্লিকেট এবং ইনভ্যালিড ডাটা বাদ দেওয়া
        if not cve_id or cve_id in seen_cves:
            continue
        
        seen_cves.add(cve_id)

        # ২. প্রয়োজনীয় ফিল্ডগুলো ক্লিনভাবে এক্সট্র্যাক্ট করা
        vulnerability_entry = {
            'cveId': cve_id,
            'vendorProduct': f"{item.get('vendorProject', 'Unknown')} - {item.get('product', 'Unknown')}",
            'vulnerabilityName': item.get('vulnerabilityName', 'N/A'),
            'desc': item.get('shortDescription', 'No description available'),
            'action': item.get('requiredAction', 'N/A'),
            'dateAdded': item.get('dateAdded', '')
        }
        
        cleaned_data.append(vulnerability_entry)

    # আউটপুট ফোল্ডার নিশ্চিত করা
    os.makedirs(os.path.dirname(PROCESSED_FILE_PATH), exist_ok=True)

    # ৩. ক্লিন ডাটা JSON ফাইলে সেভ করা
    with open(PROCESSED_FILE_PATH, 'w', encoding='utf-8') as f:
        json.dump(cleaned_data, f, indent=2)

    print(f"✅ Success! Processed {len(cleaned_data)} unique vulnerabilities.")
    print(f"📂 Saved to: {PROCESSED_FILE_PATH}")

if __name__ == '__main__':
    optimize_and_process_data()