# API Reference

Complete API documentation for the Dispute Resolution Intelligent Contract.

## Contract Overview

**Name:** DisputeResolution  
**Type:** GenLayer Intelligent Contract  
**Language:** Python (GenVM)  
**Consensus:** Optimistic Democracy  

## State Variables

```python
plaintiff: str              # Name of party bringing dispute
defendant: str              # Name of party being accused
plaintiff_evidence: str     # Plaintiff's submitted evidence
defendant_evidence: str     # Defendant's submitted evidence
status: str                 # Current case status
winner: str                 # Determined winner ("plaintiff" or "defendant")
reasoning: str              # AI's explanation of decision
```

## Status Values

| Status | Meaning |
|--------|---------|
| `empty` | No case created yet |
| `awaiting_evidence` | Case created, waiting for evidence |
| `ready_for_resolution` | Both parties submitted evidence |
| `resolved` | AI has made decision |
| `error` | Error during resolution |

## Methods

### Write Methods

Write methods modify contract state and require transactions.

---

#### create_case

Initialize a new dispute case.

**Signature:**
```python
@gl.public.write
def create_case(self, plaintiff: str, defendant: str) -> None
```

**Parameters:**
* `plaintiff` (str): Name of party bringing the dispute
* `defendant` (str): Name of party being accused

**Returns:** None

**State Changes:**
* Sets `plaintiff` and `defendant`
* Clears all evidence fields
* Sets `status` to `"awaiting_evidence"`
* Clears `winner` and `reasoning`

**Example:**
```python
# In GenLayer Studio
create_case("Alice Johnson", "Bob Smith")

# Via GenLayer JS
await contract.write.create_case("Alice Johnson", "Bob Smith");
```

**Processing Time:** 5-10 seconds

**Errors:**
* None (always succeeds with valid strings)

---

#### submit_plaintiff_evidence

Submit evidence from plaintiff.

**Signature:**
```python
@gl.public.write
def submit_plaintiff_evidence(self, evidence: str) -> None
```

**Parameters:**
* `evidence` (str): Detailed evidence supporting plaintiff's case

**Returns:** None

**State Changes:**
* Sets `plaintiff_evidence`
* If defendant evidence already submitted, sets `status` to `"ready_for_resolution"`

**Example:**
```python
submit_plaintiff_evidence(
    "I hired Bob to build a website for $5000 with delivery by June 1st. "
    "He delivered on August 15th (2.5 months late) with broken payment "
    "processing and missing admin panel. I have email records proving "
    "the original agreement and timeline."
)
```

**Processing Time:** 5-10 seconds

**Best Practices:**
* Provide specific dates and timelines
* Include documented agreements
* Reference concrete facts
* Explain chain of events
* Mention supporting documentation

---

#### submit_defendant_evidence

Submit evidence from defendant.

**Signature:**
```python
@gl.public.write
def submit_defendant_evidence(self, evidence: str) -> None
```

**Parameters:**
* `evidence` (str): Detailed evidence supporting defendant's case

**Returns:** None

**State Changes:**
* Sets `defendant_evidence`
* If plaintiff evidence already submitted, sets `status` to `"ready_for_resolution"`

**Example:**
```python
submit_defendant_evidence(
    "Alice changed requirements 15 times during development. "
    "Each change added weeks to timeline. I have email documentation "
    "of all scope changes. The payment processing issue was caused by "
    "incorrect API keys provided by Alice. Admin panel was moved to "
    "Phase 2 per our May 15 email agreement."
)
```

**Processing Time:** 5-10 seconds

**Best Practices:**
* Address plaintiff's specific claims
* Provide counter-evidence
* Include dates and documentation
* Explain your perspective
* Remain factual and professional

---

#### resolve_case

Trigger AI analysis and consensus to determine winner.

**Signature:**
```python
@gl.public.write
def resolve_case(self) -> None
```

**Parameters:** None

**Returns:** None

**State Changes:**
* Sets `winner` to `"plaintiff"` or `"defendant"`
* Sets `reasoning` with AI's explanation
* Sets `status` to `"resolved"` (or `"error"` if parsing fails)

**How It Works:**

1. **Extract Evidence:**
   ```python
   p_name = self.plaintiff
   d_name = self.defendant
   p_evidence = self.plaintiff_evidence
   d_evidence = self.defendant_evidence
   ```

2. **Non-Deterministic AI Call:**
   ```python
   def analyze_dispute() -> str:
       prompt = f"""You are an impartial AI judge...
       Plaintiff: {p_name}
       Evidence: {p_evidence}
       
       Defendant: {d_name}
       Evidence: {d_evidence}
       
       Determine who has stronger case..."""
       
       result = gl.nondet.exec_prompt(prompt)
       return result
   ```

3. **Consensus via Equivalence Principle:**
   ```python
   result = gl.eq_principle.prompt_non_comparative(
       analyze_dispute,
       task="Analyze dispute evidence and determine winner",
       criteria="Must return valid JSON with winner and reasoning"
   )
   ```

4. **Parse and Store:**
   ```python
   decision = json.loads(result)
   self.winner = decision["winner"]
   self.reasoning = decision["reasoning"]
   ```

**Processing Time:** **30-90 seconds**

This takes time because:
* Leader validator executes with their LLM (10-30s)
* Four other validators verify with different LLMs (10-30s each)
* Consensus agreement across all validators (5-10s)
* Total: 30-90 seconds

**AI Analysis Considers:**
* Strength and credibility of evidence
* Logical consistency of arguments
* Fairness and reasonableness of claims
* Patterns of good faith or bad faith
* Documentation and specificity
* Timeline coherence

**Errors:**
* `status` set to `"error"` if:
  * Evidence missing from either party
  * AI response not valid JSON
  * Parsing fails

---

### View Methods

View methods are read-only and return data instantly.

---

#### get_case

Retrieve complete case details.

**Signature:**
```python
@gl.public.view
def get_case(self) -> dict
```

**Parameters:** None

**Returns:** Dictionary with all case information

**Return Structure:**
```python
{
    "plaintiff": str,           # Plaintiff name
    "defendant": str,           # Defendant name
    "plaintiff_evidence": str,  # Plaintiff's evidence
    "defendant_evidence": str,  # Defendant's evidence
    "status": str,              # Case status
    "winner": str,              # Winner (if resolved)
    "reasoning": str            # AI's reasoning (if resolved)
}
```

**Example:**
```python
# In GenLayer Studio
get_case()

# Via GenLayer JS
const caseData = await contract.read.get_case();
console.log(caseData.winner, caseData.reasoning);
```

**Processing Time:** <1 second (instant)

**Example Response:**
```json
{
    "plaintiff": "Alice Johnson",
    "defendant": "Bob Smith",
    "plaintiff_evidence": "I hired Bob to build...",
    "defendant_evidence": "Alice changed requirements...",
    "status": "resolved",
    "winner": "plaintiff",
    "reasoning": "The plaintiff provided documented evidence of the original agreement terms. While scope changes occurred, the defendant failed to formalize these changes properly and the core deliverables were not met according to the contract."
}
```

---

## Usage Patterns

### Complete Workflow

```python
# 1. Create case
create_case("Alice", "Bob")

# 2. Verify creation
case = get_case()
# status should be "awaiting_evidence"

# 3. Submit evidence from both parties
submit_plaintiff_evidence("I hired Bob for $5000...")
submit_defendant_evidence("Alice changed requirements...")

# 4. Verify both submitted
case = get_case()
# status should be "ready_for_resolution"

# 5. Resolve (wait 30-90 seconds!)
resolve_case()

# 6. View verdict
case = get_case()
# status: "resolved"
# winner: "plaintiff" or "defendant"
# reasoning: "The plaintiff provided..."
```

### Error Handling

```javascript
try {
    await contract.write.resolve_case();
    await tx.wait(); // May take 30-90 seconds
    
    const result = await contract.read.get_case();
    if (result.status === "resolved") {
        console.log(`Winner: ${result.winner}`);
        console.log(`Reason: ${result.reasoning}`);
    } else if (result.status === "error") {
        console.error("Resolution failed");
    }
} catch (error) {
    console.error("Transaction failed:", error);
}
```

## Non-Deterministic Execution

### Key Concepts

**Storage Inaccessibility:**

Storage cannot be accessed from within non-deterministic blocks.

**Wrong:**
```python
def analyze():
    name = self.plaintiff  # Error! Storage inaccessible
    return gl.nondet.exec_prompt(f"Analyze {name}")
```

**Correct:**
```python
# Extract BEFORE defining function
p_name = self.plaintiff

def analyze():
    # Use captured variable
    return gl.nondet.exec_prompt(f"Analyze {p_name}")
```

### Equivalence Principle

`gl.eq_principle.prompt_non_comparative()` parameters:

**fn:** Function that returns AI analysis result  
**task:** What the AI should accomplish  
**criteria:** What makes a valid/equivalent output

Example:
```python
result = gl.eq_principle.prompt_non_comparative(
    analyze_dispute,
    task="Analyze dispute evidence and determine the winner based on merit",
    criteria="Must return valid JSON with winner (plaintiff/defendant) and reasoning fields"
)
```

How it works:
1. Leader executes `fn()` and proposes result
2. Validators execute `fn()` independently
3. Each validator checks if their result is "equivalent" to leader's
4. "Equivalent" = meets the task/criteria, not necessarily identical
5. If majority agrees, consensus reached
6. If disagreement, more validators added

## AI Prompt Engineering

The contract uses this prompt structure:

```python
prompt = f"""You are an impartial AI judge analyzing a dispute.

CASE DETAILS:
Plaintiff: {p_name}
Plaintiff's Evidence: {p_evidence}

Defendant: {d_name}  
Defendant's Evidence: {d_evidence}

TASK:
Analyze both sides objectively. Consider:
1. Strength and credibility of evidence
2. Logical consistency of arguments
3. Fairness and reasonableness of claims
4. Patterns of good faith or bad faith

Determine who has the stronger case.

RESPONSE FORMAT (must be valid JSON):
{{
    "winner": "plaintiff" or "defendant",
    "reasoning": "Your brief explanation (2-3 sentences)"
}}

Return ONLY the JSON object. No markdown formatting, no additional text."""
```

**Why this works:**
* Clear role definition ("impartial AI judge")
* Structured evidence presentation
* Explicit evaluation criteria
* Strict output format requirement
* No room for ambiguity

## Performance Characteristics

| Operation | Avg Time | Range | Cost |
|-----------|----------|-------|------|
| create_case | 7s | 5-10s | Low |
| submit_evidence | 7s | 5-10s | Low |
| resolve_case | 60s | 30-90s | High |
| get_case | <1s | <1s | Free |

**Why resolution is slow:**

GenLayer uses "Optimistic Democracy" consensus:
* Multiple validators with different LLMs
* Each independently analyzes the dispute
* Must reach consensus on fairness
* Cannot be sped up without sacrificing security

This is a feature, not a bug.

## Security Considerations

### Data Privacy

All data is public on blockchain:
* Evidence is permanently stored
* Anyone can read case details
* Don't submit sensitive information
* Consider anonymizing parties

### Manipulation Resistance

The multi-validator system prevents:
* Single validator bias
* Deterministic prediction
* Bribery (would need majority)
* Prompt injection attacks (multiple models verify)

### Trust Assumptions

You trust:
* GenLayer validator network
* Multiple AI providers
* Consensus mechanism

You don't trust:
* Any single validator
* Any single AI model
* Contract deployer

## Extending the Contract

### Add Case Counter

```python
case_count: int

def __init__(self):
    # ... existing init
    self.case_count = 0

@gl.public.write
def create_case(self, plaintiff: str, defendant: str) -> None:
    # ... existing code
    self.case_count += 1

@gl.public.view
def get_case_count(self) -> int:
    return self.case_count
```

### Add Categories

```python
category: str  # "contract", "product", "service", etc.

@gl.public.write
def create_case(self, plaintiff: str, defendant: str, category: str) -> None:
    # ... existing code
    self.category = category
```

### Add Appeal Mechanism

```python
appealed: bool
appeal_reasoning: str

@gl.public.write
def appeal_decision(self, reason: str) -> None:
    if self.status != "resolved":
        return
    
    self.appealed = True
    self.appeal_reasoning = reason
    self.status = "under_appeal"
```

## References

* [GenLayer Docs](https://docs.genlayer.com)
* [Intelligent Contracts Guide](https://docs.genlayer.com/developers/intelligent-contracts/introduction)
* [Calling LLMs](https://docs.genlayer.com/developers/intelligent-contracts/features/calling-llms)
* [Equivalence Principle](https://docs.genlayer.com/developers/intelligent-contracts/equivalence-principle)
* [SDK Reference](https://sdk.genlayer.com)

---

For support, join [GenLayer Discord](https://discord.gg/8Jm4v89VAu)
