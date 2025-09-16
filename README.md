\# 🚀 LiteLLM-Ollama Management Tools



> \*\*Effortlessly manage your Ollama models in LiteLLM proxy with these powerful Python utilities\*\*



\[!\[Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/)

\[!\[License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

\[!\[LiteLLM](https://img.shields.io/badge/LiteLLM-Compatible-orange.svg)](https://litellm.ai/)

\[!\[Ollama](https://img.shields.io/badge/Ollama-Compatible-red.svg)](https://ollama.ai/)



\## ✨ Features



\- 🔄 \*\*Bulk Model Management\*\*: Add all your Ollama models to LiteLLM with a single command

\- 🧹 \*\*Duplicate Cleanup\*\*: Automatically detect and remove duplicate models

\- 🎯 \*\*Smart Detection\*\*: Only add new models, skip existing ones

\- 🔍 \*\*Dry Run Mode\*\*: Preview changes before executing them

\- 💪 \*\*Force Mode\*\*: Override duplicate detection when needed

\- 🎨 \*\*Beautiful CLI\*\*: Rich output with emojis and progress indicators

\- 🛡️ \*\*Error Handling\*\*: Robust error handling and detailed feedback



\## 📋 Table of Contents



\- \[🚀 LiteLLM-Ollama Management Tools](#-litellm-ollama-management-tools)

&nbsp; - \[✨ Features](#-features)

&nbsp; - \[📋 Table of Contents](#-table-of-contents)

&nbsp; - \[🏗️ Prerequisites](#️-prerequisites)

&nbsp; - \[⚡ Quick Start](#-quick-start)

&nbsp; - \[📚 Scripts Overview](#-scripts-overview)

&nbsp;   - \[🧹 cleanup\\\_duplicates.py](#-cleanup\_duplicatespy)

&nbsp;   - \[➕ add\\\_new\\\_models.py](#-add\_new\_modelspy)

&nbsp; - \[🔧 Usage Examples](#-usage-examples)

&nbsp;   - \[Adding Models from Ollama](#adding-models-from-ollama)

&nbsp;   - \[Cleaning Up Duplicates](#cleaning-up-duplicates)

&nbsp;   - \[Real-world Workflow](#real-world-workflow)

&nbsp; - \[⚙️ Command Line Options](#️-command-line-options)

&nbsp;   - \[Common Options](#common-options)

&nbsp;   - \[add\\\_new\\\_models.py Specific](#add\_new\_modelspy-specific)

&nbsp;   - \[cleanup\\\_duplicates.py Specific](#cleanup\_duplicatespy-specific)

&nbsp; - \[🎯 Use Cases](#-use-cases)

&nbsp; - \[🔍 Troubleshooting](#-troubleshooting)

&nbsp; - \[📖 API Reference](#-api-reference)

&nbsp; - \[🤝 Contributing](#-contributing)

&nbsp; - \[📄 License](#-license)



\## 🏗️ Prerequisites



\- \*\*Python 3.7+\*\* installed on your system

\- \*\*Ollama server\*\* running and accessible

\- \*\*LiteLLM proxy\*\* running with API access

\- \*\*LiteLLM API key/Master key\*\* for authentication



\### Required Python Packages



```bash

pip install requests

```



\## ⚡ Quick Start



1\. \*\*Clone or download\*\* the scripts to your local machine



2\. \*\*Get your LiteLLM API key\*\* from your LiteLLM proxy setup



3\. \*\*Add all your Ollama models\*\* to LiteLLM:

&nbsp;  ```bash

&nbsp;  python3 add\_new\_models.py \\

&nbsp;    --ollama-url http://192.168.1.250:11434 \\

&nbsp;    --litellm-url http://localhost:4000 \\

&nbsp;    --api-key your-litellm-api-key

&nbsp;  ```



4\. \*\*Clean up any duplicates\*\* (if needed):

&nbsp;  ```bash

&nbsp;  python3 cleanup\_duplicates.py \\

&nbsp;    --ollama-url http://192.168.1.250:11434 \\

&nbsp;    --litellm-url http://localhost:4000 \\

&nbsp;    --api-key your-litellm-api-key

&nbsp;  ```



\## 📚 Scripts Overview



\### 🧹 cleanup\_duplicates.py



\*\*Purpose\*\*: Remove duplicate models from your LiteLLM proxy



\*\*What it does\*\*:

\- Scans all models in LiteLLM proxy

\- Identifies models with identical names

\- Keeps the first occurrence, removes duplicates

\- Provides detailed reporting of actions taken



\*\*Perfect for\*\*: Cleaning up after manual additions or bulk imports that created duplicates



\### ➕ add\_new\_models.py



\*\*Purpose\*\*: Intelligently add Ollama models to LiteLLM proxy



\*\*What it does\*\*:

\- Fetches all available models from your Ollama server

\- Checks existing models in LiteLLM proxy

\- Adds only new models (unless forced)

\- Provides comprehensive progress reporting



\*\*Perfect for\*\*: Initial setup or adding new models after downloading them to Ollama



\## 🔧 Usage Examples



\### Adding Models from Ollama



```bash

\# Preview what would be added (safe to run)

python3 add\_new\_models.py \\

&nbsp; --ollama-url http://192.168.1.250:11434 \\

&nbsp; --litellm-url http://localhost:4000 \\

&nbsp; --api-key sk-1234567890abcdef \\

&nbsp; --dry-run



\# Add only new models (recommended)

python3 add\_new\_models.py \\

&nbsp; --ollama-url http://192.168.1.250:11434 \\

&nbsp; --litellm-url http://localhost:4000 \\

&nbsp; --api-key sk-1234567890abcdef



\# Force add all models (creates duplicates)

python3 add\_new\_models.py \\

&nbsp; --ollama-url http://192.168.1.250:11434 \\

&nbsp; --litellm-url http://localhost:4000 \\

&nbsp; --api-key sk-1234567890abcdef \\

&nbsp; --force

```



\### Cleaning Up Duplicates



```bash

\# Preview what would be cleaned (safe to run)

python3 cleanup\_duplicates.py \\

&nbsp; --ollama-url http://192.168.1.250:11434 \\

&nbsp; --litellm-url http://localhost:4000 \\

&nbsp; --api-key sk-1234567890abcdef \\

&nbsp; --dry-run



\# Actually remove duplicates

python3 cleanup\_duplicates.py \\

&nbsp; --ollama-url http://192.168.1.250:11434 \\

&nbsp; --litellm-url http://localhost:4000 \\

&nbsp; --api-key sk-1234567890abcdef

```



\### Real-world Workflow



```bash

\# 1. First, see what's currently in Ollama

curl http://192.168.1.250:11434/api/tags | jq '.models\[].name'



\# 2. Preview what would be added to LiteLLM

python3 add\_new\_models.py --ollama-url http://192.168.1.250:11434 --litellm-url http://localhost:4000 --api-key YOUR\_KEY --dry-run



\# 3. Add the new models

python3 add\_new\_models.py --ollama-url http://192.168.1.250:11434 --litellm-url http://localhost:4000 --api-key YOUR\_KEY



\# 4. If you accidentally created duplicates, clean them up

python3 cleanup\_duplicates.py --ollama-url http://192.168.1.250:11434 --litellm-url http://localhost:4000 --api-key YOUR\_KEY --dry-run

python3 cleanup\_duplicates.py --ollama-url http://192.168.1.250:11434 --litellm-url http://localhost:4000 --api-key YOUR\_KEY

```



\## ⚙️ Command Line Options



\### Common Options



| Option | Required | Description | Example |

|--------|----------|-------------|---------|

| `--ollama-url` | ✅ | URL of your Ollama server | `http://192.168.1.250:11434` |

| `--litellm-url` | ✅ | URL of your LiteLLM proxy | `http://localhost:4000` |

| `--api-key` | ✅ | LiteLLM API key or master key | `sk-1234567890abcdef` |

| `--dry-run` | ❌ | Preview changes without executing | `--dry-run` |



\### add\_new\_models.py Specific



| Option | Description | Use Case |

|--------|-------------|----------|

| `--force` | Add all models even if they exist | When you want to intentionally create duplicates |



\### cleanup\_duplicates.py Specific



> No additional options - focused on one task: cleaning duplicates safely



\## 🎯 Use Cases



| Scenario | Recommended Approach |

|----------|---------------------|

| \*\*First-time setup\*\* | Use `add\_new\_models.py` to bulk-add all your Ollama models |

| \*\*Regular maintenance\*\* | Use `add\_new\_models.py` after downloading new models to Ollama |

| \*\*After manual additions\*\* | Use `cleanup\_duplicates.py` to remove any duplicates |

| \*\*Migration/Backup restore\*\* | Use `--force` with `add\_new\_models.py`, then `cleanup\_duplicates.py` |

| \*\*Testing changes\*\* | Always use `--dry-run` first to preview changes |



\## 🔍 Troubleshooting



\### Common Issues



\*\*❌ "Failed to get models: 401"\*\*

```bash

\# Check your API key

curl -H "Authorization: Bearer YOUR\_KEY" http://localhost:4000/model/info

```



\*\*❌ "Error connecting to Ollama"\*\*

```bash

\# Test Ollama connection

curl http://192.168.1.250:11434/api/tags

```



\*\*❌ "No models found in Ollama"\*\*

```bash

\# Check if Ollama has models

ollama list

```



\### Debug Mode



Add verbose output to see exactly what's happening:

```bash

\# Check the raw response structure

python3 -c "

import requests

response = requests.get('http://localhost:4000/model/info', headers={'Authorization': 'Bearer YOUR\_KEY'})

print(response.status\_code)

print(response.text\[:500])

"

```



\### Network Issues



\- Ensure all services are running and accessible

\- Check firewalls and network connectivity

\- Verify URLs don't have typos (common mistake!)



\## 📖 API Reference



\### LiteLLM Endpoints Used



\- `GET /model/info` - Retrieve existing models

\- `POST /model/new` - Add new model

\- `DELETE /model/delete` - Remove model by ID



\### Ollama Endpoints Used



\- `GET /api/tags` - List available models



\### Model Configuration Format



```json

{

&nbsp; "model\_name": "llama2:latest",

&nbsp; "litellm\_params": {

&nbsp;   "model": "ollama/llama2:latest",

&nbsp;   "api\_base": "http://192.168.1.250:11434"

&nbsp; }

}

```



\## 🤝 Contributing



We welcome contributions! Here's how you can help:



1\. \*\*🐛 Report bugs\*\* - Open an issue with details

2\. \*\*💡 Suggest features\*\* - Share your ideas

3\. \*\*🔧 Submit PRs\*\* - Fix bugs or add features

4\. \*\*📚 Improve docs\*\* - Help make this README even better



\### Development Setup



```bash

\# Clone the repository

git clone <your-repo-url>



\# Create a virtual environment

python3 -m venv venv

source venv/bin/activate  # On Windows: venv\\Scripts\\activate



\# Install dependencies

pip install requests



\# Run tests

python3 add\_new\_models.py --help

python3 cleanup\_duplicates.py --help

```



\### Code Style



\- Follow PEP 8

\- Use meaningful variable names

\- Add docstrings to functions

\- Include error handling



\## 📄 License



This project is licensed under the MIT License - see the \[LICENSE](LICENSE) file for details.



---



<div align="center">



\*\*Made with ❤️ for the LiteLLM and Ollama community\*\*



⭐ \*\*Star this repo\*\* if it helped you! ⭐



\[Report Bug](../../issues) • \[Request Feature](../../issues) • \[Documentation](../../wiki)



</div>

