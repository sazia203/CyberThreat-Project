const express = require('express');
const cors = require('cors');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = 5000;

// CORS এবং JSON মিডেলওয়্যার অন করা
app.use(cors());
app.use(express.json());

// টেক্সট ফাইল থেকে ডাটা রিড করার API রুট
app.get('/api/vulnerabilities', (req, res) => {
    const filePath = path.join(__dirname, 'dataset', 'processed', 'clean_vulnerabilities.txt');

    // ফাইলটি আছে কিনা চেক করা
    if (!fs.existsSync(filePath)) {
        return res.status(404).json({ error: "ডাটা ফাইলটি পাওয়া যায়নি! আগে পাইথন কোড রান করুন।" });
    }

    // টেক্সট ফাইলটি রিড করা
    fs.readFile(filePath, 'utf8', (err, data) => {
        if (err) {
            return res.status(500).json({ error: "ফাইল রিড করতে সমস্যা হয়েছে।" });
        }

        // টেক্সট ডাটাকে সুন্দরভাবে অবজেক্টে রূপান্তর করা
        const blocks = data.split('--------------------------------------------------');
        const vulnerabilities = [];

        blocks.forEach(block => {
            const lines = block.trim().split('\n');
            if (lines.length >= 3) {
                const cveId = lines[0].replace('CVE ID: ', '').trim();
                const vendorProduct = lines[1].replace('Vendor/Product: ', '').trim();
                const desc = lines[2].replace('Description: ', '').trim();

                vulnerabilities.push({ cveId, vendorProduct, desc });
            }
        });

        // ফ্রন্টএন্ডে ডাটা পাঠানো
        res.json(vulnerabilities);
    });
});

// সার্ভার চালু করা
app.listen(PORT, () => {
    console.log(`🚀 সার্ভার রেডি! চলছে এই লিংকে: http://localhost:${PORT}`);
});