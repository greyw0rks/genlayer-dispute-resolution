# GenLayer 5-Minute Quick Start

Get your first Intelligent Contract running in 5 minutes.

## Step 1: Open Studio

Go to https://studio.genlayer.com

No installation. No setup. Just open your browser.

## Step 2: Paste This Contract

Click "New Contract" and paste:

```python
# { "Depends": "py-genlayer:test" }

from genlayer import *

class Contract(gl.Contract):
    message: str
    
    def __init__(self):
        self.message = "Hello GenLayer"
    
    @gl.public.view
    def get_message(self) -> str:
        return self.message
    
    @gl.public.write
    def set_message(self, new_message: str):
        self.message = new_message
```

## Step 3: Deploy

Click "Deploy new instance"

Wait 10-15 seconds for green "FINALIZED" status

## Step 4: Test

**Read the message:**
1. Expand "Read Methods"
2. Click `get_message`
3. Click "Query"
4. See: `"Hello GenLayer"`

**Change the message:**
1. Expand "Write Methods"
2. Click `set_message`
3. Enter: `AI-powered contracts are awesome`
4. Click "Execute"
5. Wait for FINALIZED

**Read again:**
1. Read Methods → `get_message` → Query
2. See your new message!

## Congratulations!

You just deployed an Intelligent Contract.

## Next Steps

**Try the full tutorial:**
- [Complete Tutorial](TUTORIAL.md) - Build dispute resolution system
- [Cheat Sheet](CHEATSHEET.md) - Quick reference
- [Studio Guide](STUDIO_GUIDE.md) - Master the UI

**Deploy the dispute resolution contract:**
1. Copy from `/contracts/dispute_resolution.py`
2. Paste in Studio
3. Deploy
4. Test with real AI decisions

## Need Help?

- Check [Troubleshooting](TROUBLESHOOTING.md)
- Join [Discord](https://discord.gg/8Jm4v89VAu)
- Read [Docs](https://docs.genlayer.com)

Welcome to GenLayer! 🚀
