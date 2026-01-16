# Complete GenLayer Studio UI Guide

## Overview

GenLayer Studio is your browser-based IDE for developing, testing, and deploying Intelligent Contracts. This guide shows you exactly how to use every feature.

## Interface Layout

```
┌─────────────────────────────────────────────────────────────────┐
│  GenLayer Logo    [Run and Debug Tab]           [Account Info]  │
├──────────┬──────────────────────────────────────────────────────┤
│          │                                                       │
│  Left    │              Code Editor                             │
│  Panel   │              (Middle Panel)                          │
│          │                                                       │
│  - Files │                                                       │
│  - Deploy│                                                       │
│  - Methods                                                       │
│  - Txns  │                                                       │
│          │                                                       │
├──────────┴──────────────────────────────────────────────────────┤
│  Bottom Panel: Logs | Console | Validators                      │
└─────────────────────────────────────────────────────────────────┘
```

## Step-by-Step Workflow

### Part 1: Loading Your Contract

**Method A: New Contract**

1. Click **"Run and Debug"** tab at top
2. Look at left panel under "Contract:"
3. Click **"Deploy new instance"** button
4. A new editor tab opens
5. Delete the example code
6. Paste your contract code
7. The file auto-saves

**Method B: From File**

1. Click the **file icon** in left panel
2. Navigate to your `.py` file
3. Click to open in editor
4. Contract loads in the middle panel

**Your contract should now show in the editor with syntax highlighting.**

---

### Part 2: Deploying the Contract

**Look at the left panel "Contract:" section**

You'll see:
- Contract name: `test_dispute_resolution.py`
- Status indicator (grey = not deployed)
- Two buttons below

**Click "Deploy new instance"**

What happens:
1. Progress indicator appears
2. Bottom panel shows deployment logs
3. After 10-30 seconds, you'll see "FINALIZED"
4. Contract address appears: `0x2f...`
5. Status turns green

**Deployment Success Indicators:**
- ✅ Green "FINALIZED" badge in Transactions section
- ✅ Contract address displayed
- ✅ Methods become available

---

### Part 3: Understanding the Left Panel Sections

**1. Contract Section**
```
Contract: test_dispute_resolution.py
├─ Deployed at 0x2f...
├─ [Deploy new instance]
└─ [Upgrade code]
```

**2. Read Methods**
These are view functions that don't change state:
- `get_case`
- `get_all_cases`

Click to expand and see input fields.

**3. Write Methods**
These modify the contract state:
- `create_case`
- `submit_evidence`
- `resolve_case`

These require transactions and gas.

**4. Transactions**
Shows all transactions you've sent:
- Pending (yellow)
- Finalized (green)
- Failed (red)

Click any transaction to see details.

---

### Part 4: Executing Write Methods (Creating a Case)

**Step 1: Expand Write Methods**

Click the dropdown arrow next to "Write Methods"

**Step 2: Select create_case**

You should see:
```
create_case
├─ plaintiff (str): [________]
└─ defendant (str): [________]
```

**Step 3: Fill in Arguments**

Type directly in the input boxes:
- plaintiff: `Alice`
- defendant: `Bob`

**Step 4: Click Execute**

You'll see:
1. Transaction appears in "Transactions" section
2. Status: "Pending..."
3. Bottom panel shows execution logs
4. After 5-10 seconds: Status changes to "FINALIZED"

**Step 5: Check Result**

Click the transaction in the Transactions list.

You should see:
```json
{
  "result": 0,
  "status": "success"
}
```

The `0` is your case ID!

---

### Part 5: Executing More Write Methods

**Submit Plaintiff Evidence**

1. Select `submit_evidence` from Write Methods
2. Fill in:
   - case_id: `0`
   - party: `plaintiff`
   - evidence: `I hired Bob for $5000. Contract signed Jan 1. Deadline was Jan 30. Bob delivered Feb 15, 15 days late with broken features.`
3. Click Execute
4. Wait for "FINALIZED"

**Submit Defendant Evidence**

1. Select `submit_evidence` again
2. Fill in:
   - case_id: `0`
   - party: `defendant`
   - evidence: `Alice changed requirements 15 times after signing. I have email proof. Original features delivered on time. Her broken features are new requests not in original contract.`
3. Click Execute
4. Wait for "FINALIZED"

**Resolve the Case (AI Magic!)**

1. Select `resolve_case`
2. Fill in:
   - case_id: `0`
3. Click Execute
4. **This takes 30-60 seconds** - AI validators are analyzing
5. Watch the bottom panel "Logs" tab for validator activity
6. Wait for "FINALIZED"

---

### Part 6: Reading Contract State

**Using Read Methods**

1. Expand "Read Methods" in left panel
2. Select `get_case`
3. Fill in:
   - case_id: `0`
4. Click **"Query"** (not Execute - read methods don't need transactions)

**Result appears immediately:**
```json
{
  "plaintiff": "Alice",
  "defendant": "Bob",
  "plaintiff_evidence": "I hired Bob...",
  "defendant_evidence": "Alice changed...",
  "resolved": true,
  "winner": "defendant",
  "reasoning": "Based on the evidence, Bob delivered the original contracted features on time. Alice's claim of broken features appears to stem from additional requirements not included in the original contract..."
}
```

**Check All Cases**

1. Select `get_all_cases`
2. Click "Query"
3. See array of all cases

---

### Part 7: Understanding the Bottom Panel

**Tabs Available:**

**1. Logs Tab**
- Shows execution output
- Validator consensus process
- Error messages
- Real-time updates during transactions

**2. Console Tab**
- Direct RPC interaction
- Advanced debugging
- Manual JSON-RPC calls

**3. Validators Tab**
- Shows active validators
- Their LLM providers (GPT-4, Claude, Llama, etc.)
- Consensus votes
- Useful for debugging why validators disagree

**4. Contract Tab** (Button at bottom right)
- Schema viewer
- All methods with descriptions
- Interactive testing interface

---

### Part 8: Using the Console (Advanced)

Click the **Console** tab at bottom.

**Direct Method Calls:**

Type and press Enter:
```javascript
await contract.create_case("Charlie", "Dave")
```

**Query State:**
```javascript
await contract.get_case(0)
```

**Check Account:**
```javascript
account.address
```

This gives you programmatic control.

---

### Part 9: Monitoring Validators

**Click "Validators" tab at bottom**

You'll see:
```
Validator 1: GPT-4 (OpenAI)
Status: Active
Last Vote: Approved

Validator 2: Claude-3 (Anthropic)  
Status: Active
Last Vote: Approved

Validator 3: Llama-70B (Heurist)
Status: Active
Last Vote: Approved
```

**During resolve_case execution, watch this tab:**
- Validators analyze evidence
- Each votes on the outcome
- You see consensus forming in real-time
- If validators disagree, you see the appeal process

---

### Part 10: Understanding Transaction Statuses

**In the Transactions section:**

**PENDING** (Yellow)
- Transaction submitted
- Waiting for leader validator
- Usually lasts 2-5 seconds

**PROPOSING** (Blue)
- Leader proposed a result
- Other validators checking
- 5-15 seconds for simple operations
- 30-60 seconds for LLM operations

**COMMITTING** (Blue)
- Validators reached consensus
- Writing to blockchain
- 2-5 seconds

**FINALIZED** (Green)
- Transaction complete
- Result available
- State updated

**FAILED** (Red)
- Transaction reverted
- Error in contract logic
- Click to see error message

---

### Part 11: Debugging Failed Transactions

**When a transaction shows FAILED:**

1. Click the failed transaction in the list
2. Look at the error message
3. Common errors:

**"Case not found"**
- You used wrong case_id
- Use `get_all_cases` to see valid IDs

**"Case already resolved"**
- Can't resolve same case twice
- Create new case to test again

**"Both parties must submit evidence"**
- Need both plaintiff AND defendant evidence
- Submit missing evidence first

**"Invalid party"**
- party must be exactly "plaintiff" or "defendant"
- Check spelling and quotes

---

### Part 12: Testing Your Full Workflow

**Complete Test Sequence:**

```
1. Deploy Contract
   ↓ (wait for FINALIZED)
   
2. create_case("Alice", "Bob")
   ↓ (returns case_id: 0)
   
3. submit_evidence(0, "plaintiff", "evidence text")
   ↓ (wait for FINALIZED)
   
4. submit_evidence(0, "defendant", "evidence text")
   ↓ (wait for FINALIZED)
   
5. resolve_case(0)
   ↓ (wait 30-60 seconds for AI analysis)
   
6. get_case(0)
   ↓ (see the winner and reasoning!)
```

---

### Part 13: Useful Keyboard Shortcuts

- **Ctrl/Cmd + S** - Save contract code
- **Ctrl/Cmd + /** - Toggle comment
- **Ctrl/Cmd + F** - Find in file
- **Ctrl/Cmd + D** - Duplicate line
- **Alt + Up/Down** - Move line up/down

---

### Part 14: Studio Settings

**Click the gear icon (⚙️) if available:**

- Theme (light/dark)
- Font size
- Auto-save interval
- Validator configuration
- Network selection

---

### Part 15: Common UI Issues and Fixes

**Issue: Methods not showing**
- Refresh the page
- Re-deploy the contract
- Check console for errors

**Issue: Transaction stuck on PENDING**
- Wait up to 2 minutes
- Refresh the page
- Check bottom panel logs

**Issue: Can't see contract code**
- Click the file tab at top
- Look for your .py file
- Click to reopen

**Issue: Execution button disabled**
- Check all required fields are filled
- Make sure contract is deployed
- Verify account has balance

**Issue: Results not showing**
- Click the transaction in the list
- Look in the Console tab
- Check the Logs tab for errors

---

### Part 16: Best Practices

**1. Save Often**
Contract auto-saves, but manually save with Ctrl+S to be sure.

**2. Name Your Transactions**
Studio tracks all transactions. Deploy multiple contracts to test different versions.

**3. Use Read Methods Frequently**
Query state between write operations to verify changes.

**4. Monitor Logs**
Keep the Logs tab visible during execution to catch issues early.

**5. Test Edge Cases**
- Submit empty evidence
- Use invalid case IDs
- Try to resolve before evidence submitted
- Test duplicate operations

**6. Watch Validators**
During resolve_case, watch the Validators tab to see AI consensus forming.

---

### Part 17: Exporting Results

**To save your test results:**

1. Right-click in the result panel
2. Select "Copy" or "Copy as JSON"
3. Paste into your documentation

**Or take screenshots:**
- Full workflow screenshot
- Final result showing AI decision
- Validator consensus view

---

### Part 18: Working with Multiple Contracts

**Deploy multiple versions:**

1. Edit your contract code
2. Click "Deploy new instance" again
3. Studio creates a new deployment
4. Both contracts remain accessible
5. Switch between them in the left panel

**Compare results:**
- Deploy V1, test
- Deploy V2 with improvements, test
- Compare transaction results

---

### Part 19: Understanding Gas and Costs

**In Studio:**
- Gas is simulated
- No real costs
- Unlimited transactions
- Perfect for testing

**Transactions show estimated gas:**
- Simple operations: ~100k gas
- LLM operations: ~500k-1M gas
- Use this to estimate real testnet costs

---

### Part 20: Getting Help

**Resources in Studio:**

- **Documentation link** (top right)
- **Discord link** (for questions)
- **Example contracts** (File → Examples)
- **Error messages** (click for more info)

**Debugging Checklist:**

✓ Contract deployed successfully?
✓ All methods visible in left panel?
✓ Arguments filled correctly?
✓ Previous transactions finalized?
✓ Logs show any errors?
✓ Validators all active?

---

## Quick Reference Card

**Deploy:**
1. Paste code → Deploy new instance → Wait for green

**Write Transaction:**
1. Write Methods → Select function → Fill args → Execute → Wait

**Read State:**
1. Read Methods → Select function → Fill args → Query → See result

**Debug:**
1. Click failed transaction → Read error → Fix → Retry

**Monitor:**
1. Logs tab = execution output
2. Validators tab = consensus process
3. Transactions = history

---

## Your Next Steps

Now that you know the Studio:

1. **Complete the full test workflow** (create → evidence → resolve → check)
2. **Screenshot the AI decision** for your tutorial
3. **Test edge cases** to document errors
4. **Try different evidence** to see how AI responds
5. **Document your experience** in the tutorial

The Studio UI is your testing playground. Experiment freely - you can't break anything!
