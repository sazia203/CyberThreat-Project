import json
import os

# ফাইলের পাথ ঠিক করা
raw_file_path = "dataset/raw/cisa_kev.json"
output_file_path = "dataset/processed/clean_vulnerabilities.txt"

# processed ফোল্ডার না থাকলে স্বয়ংক্রিয়ভাবে তৈরি হবে
os.makedirs("dataset/processed", exist_ok=True)

print("⏳ ডাটা প্রসেসিং শুরু হচ্ছে...")

try:
    # JSON ফাইলটি রিড করা
    with open(raw_file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # শুধু প্রয়োজনীয় কলাম ফিল্টার করে টেক্সট ফাইলে রাখা
    with open(output_file_path, "w", encoding="utf-8") as out:
        for item in data.get("vulnerabilities", []):
            cve_id = item.get("cveID", "N/A")
            vendor = item.get("vendorProject", "N/A")
            product = item.get("product", "N/A")
            desc = item.get("shortDescription", "N/A")
            
            # সুন্দর ফরম্যাটে টেক্সট সাজানো
            out.write(f"CVE ID: {cve_id}\n")
            out.write(f"Vendor/Product: {vendor} - {product}\n")
            out.write(f"Description: {desc}\n")
            out.write("-" * 50 + "\n")
            
    print("✅ ডাটা গ্যাদার ও প্রসেস সফল হয়েছে!")
    print("ফাইলটি পাবেন এখানে: dataset/processed/clean_vulnerabilities.txt")

except FileNotFoundError:
    print("❌ এরর: dataset/raw/ ফোল্ডারে cisa_kev.json ফাইলটি খুঁজে পাওয়া যায়নি!")
except Exception as e:
    print(f"❌ একটি ভুল হয়েছে: {e}")