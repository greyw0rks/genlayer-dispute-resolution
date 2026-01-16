# GenLayer Dispute Resolution System

> AI-powered dispute resolution on blockchain. Build your first Intelligent Contract in 45 minutes.

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/license/mit/)
[![GenLayer](https://img.shields.io/badge/GenLayer-Intelligent%20Contracts-blue)](https://genlayer.com)
[![Python](https://img.shields.io/badge/Python-3.11+-yellow)](https://www.python.org/)

## 🎯 What This Is

A complete tutorial and working implementation of a dispute resolution system built on GenLayer blockchain. Two parties submit evidence, AI validators analyze both sides, and consensus determines the winner - all on-chain.

**What makes this special:**
- AI makes subjective decisions on blockchain
- Multiple LLM validators reach consensus
- Natural language evidence processing
- Completely trustless and decentralized

## 🚀 Quick Start

**Try it now (no installation):**

1. Go to [GenLayer Studio](https://studio.genlayer.com)
2. Copy the contract from `contracts/dispute_resolution.py`
3. Paste into Studio and click "Deploy"
4. Test the contract using the UI

**Total time: 5 minutes**

## 📚 Repository Structure

```
genlayer-dispute-resolution/
├── README.md                          # This file
├── LICENSE                            # MIT License
├── contracts/
│   └── dispute_resolution.py          # Main contract
├── tests/
│   └── test_dispute_resolution.py     # Test suite
├── deploy/
│   └── deploy.ts                      # Deployment script
│   ├── QUICKSTART.md                  # 5-minute guide
│   ├── CHEATSHEET.md                  # Quick reference
│   ├── TROUBLESHOOTING.md            # Common issues
│   └── STUDIO_GUIDE.md               # UI 

## 💡 The Problem

Traditional smart contracts can only execute deterministic code. They cannot:
- Read the web
- Understand natural language  
- Make subjective judgments
- Handle ambiguous situations

## ✨ The Solution

GenLayer's Intelligent Contracts can:
- ✅ Fetch web data directly
- ✅ Call AI models (GPT-4, Claude, Llama)
- ✅ Make judgment calls
- ✅ Reach consensus on non-deterministic operations

## 🎮 Demo

**Real AI Decision:**

```json
{
  "winner": "defendant",
  "reasoning": "Bob provided specific evidence of scope changes that accounts for the delay and incomplete features. In contract law, substantial changes void original deadlines unless formally agreed."
}
```

## 🛠️ Tech Stack

- **Blockchain:** GenLayer
- **Language:** Python 3.11+
- **Storage:** TreeMap
- **AI:** Multi-LLM Optimistic Democracy
- **Frontend:** Next.js + genlayer-js

## 🎯 Use Cases

- Insurance Claims
- Freelance Escrow
- Content Moderation
- Prediction Markets
- DAO Governance

## 📖 Documentation


- [Quick Start](docs/QUICKSTART.md) - Get running fast
- [Cheat Sheet](docs/CHEATSHEET.md) - Quick reference
- [Troubleshooting](docs/TROUBLESHOOTING.md) - Fix issues

## 🔗 Resources

- [GenLayer Docs](https://docs.genlayer.com)
- [GenLayer Studio](https://studio.genlayer.com)
- [Discord](https://discord.gg/8Jm4v89VAu)

## 📝 License

MIT License - see LICENSE file

---

**Built with GenLayer** | [Get Started](docs/QUICKSTART.md) | [Deploy Now](https://studio.genlayer.com)
