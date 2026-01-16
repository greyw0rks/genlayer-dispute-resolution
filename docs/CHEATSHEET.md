# GenLayer Developer Cheat Sheet

## Quick Start Commands

```bash
npm install -g genlayer
genlayer network
genlayer deploy
gltest
```

## Contract Structure

```python
from genlayer import *

class Contract(gl.Contract):
    # State variables with type annotations
    my_data: str
    counter: int
    
    def __init__(self):
        self.my_data = "initial"
        self.counter = 0
    
    def my_method(self, arg: str) -> str:
        # Regular deterministic code
        self.counter += 1
        return arg
```

## Non-Deterministic Operations

### Web Data Fetching

```python
def fetch_data():
    data = gl.get_webpage('https://example.com', mode='text')
    return data

result = gl.eq_principle_strict_eq(fetch_data)
```

Modes:
- `text` - Plain text content
- `html` - Raw HTML
- `markdown` - Converted to markdown

### LLM Calls

```python
def analyze_text():
    prompt = "Summarize this: ..."
    return gl.ask_llm(prompt)

result = gl.eq_principle_non_comp(
    analyze_text,
    "Summary must capture key points"
)
```

## Equivalence Principles

### Strict Equality
Use for: deterministic operations, web fetching, exact matching

```python
result = gl.eq_principle_strict_eq(my_function)
```

### Comparative
Use for: similar but not identical outputs

```python
result = gl.eq_principle_comp(
    my_function,
    0.8  # 80% similarity threshold
)
```

### Non-Comparative
Use for: subjective analysis, open-ended questions

```python
result = gl.eq_principle_non_comp(
    my_function,
    "Output must meet these criteria..."
)
```

## Data Types

### Primitives
```python
my_int: int
my_str: str
my_bool: bool
my_float: float
```

### Collections
```python
my_list: list[str]
my_dict: dict[str, int]
my_set: set[int]
```

### Custom Classes
```python
class MyData:
    name: str
    value: int
    active: bool

my_storage: dict[int, MyData]
```

### Address Type
```python
from genlayer import Address

owner: Address
balances: dict[Address, int]
```

## Common Patterns

### Create & Update
```python
def create_item(self, name: str) -> int:
    item_id = self.counter
    self.items[item_id] = Item(name=name, created=True)
    self.counter += 1
    return item_id

def update_item(self, item_id: int, name: str):
    item = self.items.get(item_id)
    if not item:
        raise Exception("Not found")
    item.name = name
```

### Query Methods
```python
def get_item(self, item_id: int) -> dict:
    item = self.items.get(item_id)
    if not item:
        return {}
    return {"name": item.name, "created": item.created}

def get_all_items(self) -> list[dict]:
    return [self.get_item(id) for id in self.items.keys()]
```

### Web + LLM Pattern
```python
def analyze_url(self, url: str):
    def fetch_and_analyze():
        # Fetch web content
        content = gl.get_webpage(url, mode='text')
        
        # Analyze with LLM
        prompt = f"Analyze this content: {content}"
        return gl.ask_llm(prompt)
    
    result = gl.eq_principle_non_comp(
        fetch_and_analyze,
        "Must provide analysis"
    )
    return result
```

## Testing

### Test Structure
```python
from tools.request import (
    create_new_account,
    deploy_intelligent_contract,
    send_transaction,
    call_contract_method,
    post_request_localhost,
    payload
)
from tools.response import has_success_status

def test_contract():
    # Setup validators
    setup = post_request_localhost(
        payload("sim_createRandomValidators", [5])
    ).json()
    
    # Create account
    account = create_new_account()
    
    # Deploy
    code = open("contracts/my_contract.py").read()
    address, response = deploy_intelligent_contract(
        account, code, "{}"
    )
    
    # Write
    write_result = send_transaction(
        account, address, "method_name", [arg1, arg2]
    )
    assert has_success_status(write_result)
    
    # Read
    read_result = call_contract_method(
        address, account, "get_data", []
    )
    assert has_success_status(read_result)
    
    # Cleanup
    post_request_localhost(payload("sim_deleteAllValidators"))
```

## Frontend Integration

### Setup Client
```typescript
import { createClient, createAccount } from 'genlayer-js';
import { simulator } from 'genlayer-js/chains';

const account = createAccount();
const client = createClient({
    chain: simulator,
    account
});
```

### Write Transaction
```typescript
const hash = await client.writeContract({
    address: contractAddress,
    functionName: 'update_data',
    args: ['new_value']
});

const receipt = await client.waitForTransactionReceipt({
    hash,
    status: 'FINALIZED'
});
```

### Read Contract
```typescript
const result = await client.readContract({
    address: contractAddress,
    functionName: 'get_data',
    args: []
});
```

## Deployment

### CLI Deployment
```bash
genlayer deploy --contract contracts/my_contract.py --args "arg1" 42
```

### Script Deployment
```typescript
// deploy/deployScript.ts
import { GenLayerClient } from "genlayer-js";

export default async function main(client: GenLayerClient) {
    const code = await fs.readFile("contracts/my_contract.py", "utf-8");
    
    const tx = await client.deployContract({
        code,
        args: ["arg1", 42]
    });
    
    const receipt = await client.waitForTransactionReceipt({
        hash: tx,
        status: "FINALIZED"
    });
    
    return receipt.contractAddress;
}
```

```bash
genlayer deploy --script deploy/deployScript.ts
```

## Error Handling

### In Contracts
```python
def my_method(self, value: int):
    if value < 0:
        raise Exception("Value must be positive")
    
    item = self.items.get(value)
    if not item:
        raise Exception("Item not found")
```

### In Frontend
```typescript
try {
    const hash = await client.writeContract({...});
    const receipt = await client.waitForTransactionReceipt({
        hash,
        status: 'FINALIZED',
        timeout: 60000
    });
} catch (error) {
    if (error.message.includes('insufficient funds')) {
        console.error('Not enough balance');
    } else {
        console.error('Transaction failed:', error);
    }
}
```

## Common Issues & Solutions

### LLM Responses Not Matching
Problem: Validators can't reach consensus
Solution: Use non-comparative mode with clear criteria

```python
# Bad
result = gl.eq_principle_strict_eq(llm_function)

# Good
result = gl.eq_principle_non_comp(
    llm_function,
    "Must return valid JSON with required fields"
)
```

### Transaction Timeout
Problem: Complex operations taking too long
Solution: Increase timeout

```typescript
await client.waitForTransactionReceipt({
    hash,
    status: 'FINALIZED',
    timeout: 120000  // 2 minutes
});
```

### Storage Not Updating
Problem: Modifications in non-deterministic blocks don't persist
Solution: Return values and update storage in deterministic code

```python
# Bad
def update_storage():
    self.data = "new_value"  # Won't persist
    return "done"

# Good
def get_new_value():
    return "new_value"

self.data = gl.eq_principle_strict_eq(get_new_value)
```

## Best Practices

1. Keep LLM prompts specific and structured
2. Request JSON outputs for easier parsing
3. Use non-comparative mode for subjective analysis
4. Test with multiple validator configurations
5. Handle errors gracefully in contracts
6. Set appropriate timeouts in frontend
7. Cache expensive operations when possible
8. Document your equivalence criteria clearly

## Network Configuration

### Studionet (Development)
```bash
genlayer network
# Select: studionet
```

### Testnet
```bash
genlayer network
# Select: testnet-bradbury
```

### Local
```bash
genlayer network
# Select: localnet
```

## Useful Links

Documentation: https://docs.genlayer.com
GitHub: https://github.com/genlayerlabs
Discord: https://discord.gg/8Jm4v89VAu
Studio: https://studio.genlayer.com
Boilerplate: https://github.com/genlayerlabs/genlayer-project-boilerplate

## Quick Debugging

### Check Contract State
```typescript
const state = await client.readContract({
    address: contractAddress,
    functionName: 'get_all_data',
    args: []
});
console.log(state);
```

### Monitor Validators
In GenLayer Studio, check the Validators tab to see:
- Active validators
- Their LLM providers
- Consensus results
- Vote breakdowns

### View Transaction Details
```typescript
const receipt = await client.waitForTransactionReceipt({ hash });
console.log(receipt.status);
console.log(receipt.result);
```

## Advanced Patterns

### Multi-Step Analysis
```python
def complex_analysis(self, data: str):
    def step_one():
        return gl.ask_llm(f"Extract key points from: {data}")
    
    points = gl.eq_principle_non_comp(
        step_one,
        "Must list key points"
    )
    
    def step_two():
        return gl.ask_llm(f"Score these points: {points}")
    
    scores = gl.eq_principle_non_comp(
        step_two,
        "Must return scores for each point"
    )
    
    return scores
```

### Conditional Web Fetching
```python
def verify_claim(self, claim: str, source_url: str):
    def check_source():
        if not source_url:
            return "No source provided"
        
        content = gl.get_webpage(source_url, mode='text')
        prompt = f"Does this support the claim '{claim}'? Content: {content}"
        return gl.ask_llm(prompt)
    
    return gl.eq_principle_non_comp(
        check_source,
        "Must answer yes or no with reasoning"
    )
```

## Performance Tips

1. Minimize LLM calls per transaction
2. Batch related operations
3. Use strict equivalence when possible (faster)
4. Keep prompts concise
5. Cache web fetches when data doesn't change
6. Structure data efficiently in storage

## Migration from Traditional Smart Contracts

### Solidity → GenLayer

```solidity
// Solidity
contract MyContract {
    mapping(address => uint256) public balances;
    
    function updateBalance(uint256 amount) public {
        balances[msg.sender] = amount;
    }
}
```

```python
# GenLayer
from genlayer import *

class Contract(gl.Contract):
    balances: dict[Address, int]
    
    def __init__(self):
        self.balances = {}
    
    def update_balance(self, amount: int):
        self.balances[gl.msg_sender()] = amount
```

Key differences:
- Python instead of Solidity
- Native dict instead of mapping
- gl.msg_sender() instead of msg.sender
- Can now add LLM and web capabilities
