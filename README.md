
# 🕸️ WP-Vikrant Mirror v1.0
> **An advanced, recursive site-mirroring engine designed for deep WordPress fingerprinting and asset extraction.**

[![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python)](https://www.python.org/)
[![Backend](https://img.shields.io/badge/Engine-CURL%20%2F%20BeautifulSoup4-red)](#)
[![Security](https://img.shields.io/badge/Security-Deep%20Fingerprinting-orange)](#)
[![Status](https://img.shields.io/badge/Status-Operational-brightgreen)](#)

---

## 🔍 What is this Code?
**WP-Vikrant Mirror** is a high-end web scraping and reconnaissance tool tailored specifically for the WordPress ecosystem. It performs a "Deep Mirror" of a target site, recursively traversing internal links and reconstructs the local directory structure.

The script utilizes a hybrid request engine—combining the raw power of **system-level `curl`** for initial HTML retrieval (bypassing basic bot filters) and **Python `requests`** for granular asset management.

---

## 🚀 Why Use It?
Standard site downloaders often fail to map the specific logic of WordPress CMS. This tool provides:
* **Deep Fingerprinting:** Identifies WordPress-specific headers, `wp-content` paths, and meta generators to confirm target architecture.
* **Recursive Logic:** Automatically discovers all internal pages while respecting rate limits to prevent IP flagging.
* **Asset Mapping:** Scans every page for images, CSS, and JS files, ensuring the mirrored site retains its visual integrity.
* **Stealth User-Agents:** Mimics a modern Windows Chrome environment to minimize detection during the mirroring process.

---

## 💎 Importance
In web development, security auditing, and site migration:
1.  **Off-site Analysis:** Perform security audits on a local mirror without generating live traffic logs on the target server.
2.  **Asset Recovery:** Easily retrieve themes and stylesheets from legacy WordPress installations.
3.  **Educational Research:** Study how high-traffic WordPress sites structure their internal linking and asset delivery.

---

## ⚙️ How It Works
The engine follows a **Scan-Analyze-Destroy** logic flow:

1.  **Reconnaissance:** The `deep_fingerprinting` module checks for `wp-includes` and `generator` tags to validate the CMS.
2.  **Core Fetch:** `curl` is triggered via a subprocess to pull the raw HTML, ensuring redirect follows and SSL handling.
3.  **Recursive Mapping:** BeautifulSoup4 parses the DOM to extract `<img>`, `<link>`, and `<script>` tags, while simultaneously queuing new internal `<a>` links.
4.  **Local Reconstruction:** All data is saved into the `vikrant/` directory, precisely mirroring the original URL paths.

---

## 📊 Comparison: WP-Vikrant vs. Generic Tools

| Feature | `wget --mirror` | WP-Vikrant Mirror |
| :--- | :--- | :--- |
| **Detection** | High (Default headers) | **Low (Browser Simulation)** |
| **CMS Logic** | None | **WP Fingerprinting Active** |
| **Reliability** | Basic SSL support | **Enhanced `curl` Fallback** |
| **Directory Management** | Flat/Automatic | **Structured Mirroring** |
| **Rate Limiting** | Manual flags | **Automatic Throttling** |

---

## 🛠️ Installation & Setup

### 1. Prerequisites
* **Python 3.8+**
* **System CURL:** Ensure `curl` is accessible in your system PATH.
* **Dependencies:** `pip install requests beautifulsoup4`

### 2. Clone & Launch
```bash
git clone [https://github.com/vikrant-project/WP-Vikrant-Mirror.git](https://github.com/vikrant-project/WP-Vikrant-Mirror.git)
cd WP-Vikrant-Mirror
python3 wp_vikrant.py
```

### 3. Usage
1.  Execute the script.
2.  Input the target URL when prompted (e.g., `https://example-blog.com`).
3.  Monitor the console for real-time asset extraction logs.
4.  Open the `vikrant/index.html` file to view your local mirror.

---

## 🎨 High-End Features
* **Rate-Limit Guard:** Integrated `time.sleep` intervals to ensure the target server isn't overwhelmed.
* **Recursive Visited Queue:** Prevents infinite loops by tracking every URL in a unique hash set.
* **Silent Error Handling:** Gracefully handles 404s or connection timeouts during bulk asset downloads.

---
**Disclaimer:** This tool is for authorized research, backup, and educational purposes only. Mirroring sites without permission may violate Terms of Service. The developer is not responsible for misuse.
