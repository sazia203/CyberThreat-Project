const express = require('express');
const cors = require('cors');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = 5000;

app.use(cors());

// অপটিমাইজড JSON ফাইলের পাথ
const DATA_FILE = path.join(__dirname, 'dataset', 'processed', 'clean_vulnerabilities.json');

app.get('/api/vulnerabilities', (expressReq, expressRes) => {
    fs.readFile(DATA_FILE, 'utf8', (err, data) => {
        if (err) {
            console.error("Error reading JSON file:", err);
            return expressRes.status(500).json({ error: "Failed to read dataset" });
        }
        try {
            const vulnerabilities = JSON.parse(data);
            expressRes.json(vulnerabilities);
        } catch (parseErr) {
            console.error("Error parsing JSON:", parseErr);
            expressRes.status(500).json({ error: "Invalid JSON format" });
        }
    });
});

app.listen(PORT, () => {
    console.log(`🚀 Server is running on http://localhost:${PORT}`);
});