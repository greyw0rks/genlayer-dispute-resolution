# ⚖️ GenLayer Dispute Resolution

AI-powered dispute resolution using GenLayer's Intelligent Contracts. Multiple AI validators analyze evidence and reach consensus on fair outcomes.

![GenLayer](https://img.shields.io/badge/GenLayer-Intelligent%20Contracts-gold)
![Python](https://img.shields.io/badge/Python-Smart%20Contract-blue)
![License](https://img.shields.io/badge/License-MIT-green)

## What This Does

Traditional blockchain can only execute deterministic code. GenLayer changes this with AI-powered Intelligent Contracts that can make subjective judgments.

This dApp lets two parties submit evidence for a dispute. Multiple AI validators (using GPT-4, Claude, Gemini) independently analyze both sides and reach consensus on who has the stronger case.

## Live Demo

🌐 **[Try it now](https://dispute-online.vercel.app/)**

## Quick Start

### 1. Deploy Contract

```bash
# Open GenLayer Studio
https://studio.genlayer.com

# Copy contracts/dispute_resolution.py
# Deploy and save contract address
```

### 2. Run Frontend

```bash
cd frontend
python -m http.server 8000
# Open http://localhost:8000
```

Frontend runs in demo mode by default.

## How It Works

```python
# 1. Create dispute
create_case("Alice", "Bob")

# 2. Both sides submit evidence
submit_evidence(0, "plaintiff", "I hired Bob for $5000...")
submit_evidence(0, "defendant", "Alice changed requirements 15 times...")

# 3. AI analyzes (30-90 seconds)
resolve_case(0)

# 4. View verdict
get_case(0)
# Returns: winner, reasoning, all evidence
```

## Why It Takes 30-90 Seconds

GenLayer uses **Optimistic Democracy**:

1. Leader validator analyzes with their LLM
2. Four other validators verify with different LLMs (GPT-4, Claude, Gemini, etc.)
3. All must reach consensus on fairness
4. If disagreement, more validators added

This prevents manipulation and ensures fair AI decisions.

## Features

✅ Multiple cases support  
✅ Evidence submission from both parties  
✅ AI analysis through multi-validator consensus  
✅ Detailed reasoning for decisions  
✅ Transparent on-chain results  
✅ Beautiful web interface  

## Technology Stack

**Smart Contract:**
- Python (GenLayer SDK)
- TreeMap storage
- Non-deterministic AI execution
- Equivalence Principle consensus

**Frontend:**
- Pure HTML/CSS/JavaScript
- No framework dependencies
- Elegant serif typography
- Responsive design

## Architecture

```
User → Frontend → GenLayer JS SDK → GenLayer Node API
                        ↓
              Intelligent Contract (Python)
                        ↓
                   GenVM Execution
                        ↓
      Multiple Validators (Different LLMs)
                        ↓
          Optimistic Democracy Consensus
```

## API Reference

### Write Methods

**create_case(plaintiff: str, defendant: str)**
- Creates new dispute case
- Returns case ID (auto-incremented)

**submit_evidence(case_id: int, party: str, evidence: str)**
- party: "plaintiff" or "defendant"
- Updates status when both submit

**resolve_case(case_id: int)**
- Triggers AI analysis
- Takes 30-90 seconds for consensus
- Sets winner and reasoning

### View Methods

**get_case(case_id: int) → dict**
- Returns complete case details

**get_all_cases() → dict**
- Returns all cases with summary

**get_case_count() → int**
- Total number of cases

## Use Cases

**Contract Disputes:**
- Freelance work quality
- Project delivery timelines
- Scope changes

**Product Returns:**
- Item not as described
- Defect claims
- Service quality

**Service Disagreements:**
- Work completion
- Quality standards
- Payment disputes

## Example Evidence

**Good Evidence:**
```
I hired Bob on March 1st to build an e-commerce website for $5000 
with delivery by June 1st. Contract clearly specified shopping cart, 
payment processing, and admin panel. Bob delivered on August 15th 
(2.5 months late) with broken payment processing and missing admin 
panel. I have email records proving the original agreement.
```

**Poor Evidence:**
```
Bob did bad work and I'm not paying him.
```

Be specific, include dates, reference documentation.

## Project Structure

```
genlayer-dispute-dapp-final/
├── contracts/
│   └── dispute_resolution.py    # GenLayer Intelligent Contract
├── frontend/
│   └── index.html                # Web interface
├── docs/
│   ├── DEPLOYMENT.md             # Deployment guide
│   ├── API.md                    # Full API reference
│   └── EXAMPLES.md               # Test cases
├── .github/
│   └── workflows/
│       └── deploy.yml            # CI/CD
├── README.md                     # This file
└── LICENSE                       # MIT License
```

## Development

### Prerequisites

- Python 3.10+
- Web browser
- GenLayer Studio account

### Local Testing

```bash
# Test contract in GenLayer Studio
https://studio.genlayer.com

# Run frontend locally
cd frontend
python -m http.server 8000
```

### Integration

```javascript
// Add GenLayer JS SDK
<script src="https://unpkg.com/genlayer-js@latest/dist/index.js"></script>

// Connect to contract
const CONTRACT_ADDRESS = 'your_contract_address';
const client = new GenLayerClient({
    endpoint: 'https://studio.genlayer.com/api'
});
const contract = client.getContract(CONTRACT_ADDRESS);

// Use contract
await contract.write.create_case("Alice", "Bob");
const result = await contract.read.get_case(0);
```

## Deployment

### Deploy to Vercel

```bash
npm install -g vercel
cd frontend
vercel
```

### Deploy to Netlify

Drag `frontend` folder to netlify.com

### Deploy to GitHub Pages

1. Push to GitHub
2. Settings → Pages → Deploy from main branch

## Performance

| Operation | Time | Why |
|-----------|------|-----|
| create_case | 5-10s | Blockchain transaction |
| submit_evidence | 5-10s | Blockchain transaction |
| resolve_case | 30-90s | Multi-validator AI consensus |
| get_case | <1s | Read-only view |

## Security

**Data Privacy:**
- All evidence is public on blockchain
- Don't submit sensitive information
- Consider anonymizing details

**Trust Model:**

You trust:
- GenLayer validator network
- Multiple AI providers (OpenAI, Anthropic, Google)
- Consensus mechanism

You don't trust:
- Single AI model
- Single validator
- Contract deployer

## Contributing

Pull requests welcome! Areas for improvement:

- Evidence file uploads
- Case categories
- Appeal mechanism
- Community voting
- Analytics dashboard
- Multi-language support

## Resources

- [GenLayer Docs](https://docs.genlayer.com)
- [GenLayer Studio](https://studio.genlayer.com)
- [Discord Community](https://discord.gg/8Jm4v89VAu)
- [Example Contracts](https://docs.genlayer.com/developers/intelligent-contracts/examples)

## License

MIT License - see [LICENSE](LICENSE) file

## Support

**Issues:**
- Check [docs/](docs/) folder first
- Search existing GitHub issues
- Create new issue with details

**Questions:**
- [GenLayer Discord](https://discord.gg/8Jm4v89VAu)
- [GitHub Discussions](https://github.com/greyw0rks/genlayer-dispute-resolution/discussions)

## Acknowledgments

Built on GenLayer, the first blockchain with AI-native Intelligent Contracts capable of subjective decision-making through multi-validator consensus.

---

**Star this repo if you find it useful!** ⭐

Built with ⚖️ on GenLayer
