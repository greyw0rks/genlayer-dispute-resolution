# GenLayer Troubleshooting Guide

Common issues and solutions when building on GenLayer.

## Deployment Issues

### Methods Not Showing in Studio

**Symptoms:** "No read methods" and "No write methods" in left panel

**Solutions:**

1. Add decorators to ALL methods:
```python
@gl.public.write  # For methods that modify state
def my_method(self):
    pass

@gl.public.view   # For read-only methods
def get_data(self):
    pass
```

2. Refresh the page (F5)

3. Click "Upgrade code" button

4. Redeploy the contract

### "use TreeMap" Error

**Symptoms:** Contract fails to deploy with storage error

**Problem:** Using Python's `dict` for storage

**Solution:**

Replace:
```python
data: dict[int, SomeClass]  # ❌
```

With:
```python
data: TreeMap[u256, SomeClass]  # ✅
```

### "use bigint or sized integers" Error

**Symptoms:** Type error during deployment

**Problem:** Using Python's generic `int` in storage

**Solution:**

Replace:
```python
counter: int  # ❌
```

With:
```python
counter: u256  # ✅
```

### "Missing @gl.public decorator" Error

**Symptoms:** Methods exist but not visible

**Solution:**

Add decorator before each public method:
```python
@gl.public.write
def update_data(self, value: str):
    self.data = value

@gl.public.view
def get_data(self) -> str:
    return self.data
```

## Execution Errors

### "Write method should not return a value"

**Symptoms:** Method with `@gl.public.write` decorator fails

**Problem:** Write methods cannot return values in GenLayer

**Solution:**

Remove return statement:
```python
@gl.public.write
def create_item(self, name: str):  # No return type
    item_id = self.counter
    self.items[item_id] = Item(name=name)
    self.counter += u256(1)
    # No return statement
```

Or switch to view if you need to return:
```python
@gl.public.view  # Changed to view
def get_item_count(self) -> int:
    return int(self.counter)
```

### "Reading storage in nondet mode is not supported"

**Symptoms:** `SystemError: 6: forbidden` when accessing storage in AI functions

**Problem:** Cannot access blockchain storage inside non-deterministic blocks

**Solution:**

Extract data BEFORE the nondet function:
```python
# ❌ WRONG
def analyze():
    prompt = f"Analyze: {self.data.field}"  # Accessing storage
    return gl.nondet.exec_prompt(prompt)

# ✅ CORRECT
# Extract first
field_value = self.data.field

def analyze():
    prompt = f"Analyze: {field_value}"  # Using local variable
    return gl.nondet.exec_prompt(prompt)
```

### "object.__init__() takes exactly one argument"

**Symptoms:** Error when creating custom class instances

**Problem:** Custom class missing `__init__` method

**Solution:**

Add explicit constructor:
```python
@allow_storage
class MyData:
    name: str
    value: int
    
    # Add this:
    def __init__(self, name: str = "", value: int = 0):
        self.name = name
        self.value = value
```

## Transaction Issues

### Transaction Stuck on PENDING

**Symptoms:** Transaction doesn't finalize

**Solutions:**

1. Wait 2-3 minutes (LLM operations take time)
2. Check Logs tab for errors
3. Refresh the page
4. Try again with simpler input

### "Both parties must submit evidence"

**Symptoms:** resolve_case fails with this error

**Problem:** Missing evidence from one party

**Solution:**

Make sure you called submit_evidence twice:
```python
submit_evidence(0, "plaintiff", "evidence...")
submit_evidence(0, "defendant", "evidence...")
# Then call resolve_case(0)
```

### "Case already resolved"

**Symptoms:** Cannot resolve case twice

**This is expected behavior.** Each case can only be resolved once.

**Solution:**

Create a new case to test again:
```python
create_case("NewPlaintiff", "NewDefendant")
# This creates case ID 1
```

## UI Issues

### Contract Deployed but No Address Shown

**Symptoms:** Deployment says success but no address visible

**Solutions:**

1. Check Transactions section for FINALIZED status
2. Click the transaction to see contract address
3. Refresh the page
4. Look in bottom panel for contract address

### AI Validators Not Reaching Consensus

**Symptoms:** Resolve takes very long or fails

**Solutions:**

1. Make your prompt more specific
2. Request JSON format explicitly in prompt
3. Use stricter equivalence criteria
4. Check Validators tab to see disagreement
5. Simplify the task

### Methods Disabled/Grayed Out

**Symptoms:** Cannot execute methods

**Solutions:**

1. Ensure contract is deployed (FINALIZED status)
2. Check all required fields are filled
3. Verify account has balance
4. Refresh the page

## Type Conversion Issues

### "Cannot convert int to u256"

**Problem:** Mixing int and u256 types

**Solution:**

Convert explicitly:
```python
# Storage uses u256
case_id = self.counter  # u256

# Converting for method parameter
return int(case_id)  # Convert to int for return

# Converting from method parameter
case = self.cases.get(u256(case_id))  # Convert int to u256
```

### "TreeMap has no attribute 'keys()'"

**Problem:** TreeMap doesn't have same methods as dict

**Solution:**

Use iteration pattern:
```python
# ❌ WRONG
for key in self.cases.keys():

# ✅ CORRECT
for case_id in range(int(self.case_counter)):
    case = self.cases.get(u256(case_id))
```

## API Errors

### "module 'genlayer.gl' has no attribute 'eq_principle_non_comp'"

**Problem:** Using outdated API

**Solution:**

Update to new API:
```python
# ❌ OLD
result = gl.eq_principle_non_comp(fn, "criteria")
result = gl.ask_llm(prompt)

# ✅ NEW
result = gl.eq_principle.prompt_non_comparative(
    fn,
    task="task description",
    criteria="validation criteria"
)
result = gl.nondet.exec_prompt(prompt)
```

## Best Practices to Avoid Issues

1. **Always use TreeMap for storage dictionaries**
2. **Extract storage data before nondet blocks**
3. **Add @gl.public decorators to all public methods**
4. **Use u256 in storage, int in method signatures**
5. **Provide __init__ for custom classes**
6. **Test edge cases in Studio before deployment**
7. **Check Logs tab when things fail**
8. **Read error messages carefully - they're usually specific**

## Still Stuck?

1. Check [GenLayer Docs](https://docs.genlayer.com)
2. Search [Discord](https://discord.gg/8Jm4v89VAu)
3. Review [example contracts](https://github.com/genlayerlabs)
4. Open an issue on GitHub

## Debug Checklist

When something fails, check:

- [ ] All methods have decorators
- [ ] Using TreeMap instead of dict
- [ ] Using u256 instead of int in storage
- [ ] Storage not accessed in nondet blocks
- [ ] Custom classes have @allow_storage
- [ ] Custom classes have __init__
- [ ] Write methods don't return values
- [ ] Contract deployed successfully
- [ ] Using latest API (gl.nondet.exec_prompt, etc.)

Most issues come from these common mistakes!
