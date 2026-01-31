# Deployment Guide

Complete guide to deploying GenLayer Dispute Resolution dApp.

## Prerequisites

- GenLayer Studio account ([studio.genlayer.com](https://studio.genlayer.com))
- Web browser
- GitHub account (for deployment)

## Part 1: Deploy Smart Contract

### Step 1: Open GenLayer Studio

Navigate to [studio.genlayer.com](https://studio.genlayer.com)

### Step 2: Create New Contract

1. Click "New Contract"
2. Name: `DisputeResolution`
3. Delete template code

### Step 3: Copy Contract Code

1. Open `contracts/dispute_resolution.py`
2. Copy entire file
3. Paste into Studio editor

Verify first line: `# { "Depends": "py-genlayer:test" }`

### Step 4: Deploy

1. Click "Deploy" button
2. Wait 10-30 seconds
3. Copy contract address when shown

Example: `0x1234567890abcdef1234567890abcdef12345678`

### Step 5: Test in Studio

Try these methods:

```python
# Create case
create_case("Alice", "Bob")

# Get count
get_case_count()  # Returns 1

# View case
get_case(0)  # Returns case details
```

All methods should appear and work.

## Part 2: Deploy Frontend

### Option A: Vercel (Recommended)

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
cd frontend
vercel

# Follow prompts
# Save deployment URL
```

### Option B: Netlify

1. Go to [netlify.com](https://netlify.com)
2. Drag `frontend` folder to upload
3. Site deploys automatically
4. Save deployment URL

### Option C: GitHub Pages

```bash
# Push to GitHub first
git add .
git commit -m "Initial commit"
git push origin main

# Enable Pages
# Repository Settings → Pages
# Source: main branch
# Save
```

### Option D: Local Development

```bash
cd frontend
python -m http.server 8000
# Open http://localhost:8000
```

## Part 3: Connect Frontend to Contract

### Update Contract Address

Edit `frontend/index.html`:

```javascript
// Find this line (around line 450)
const CONTRACT_ADDRESS = 'your_contract_address_here';

// Replace with your actual address
const CONTRACT_ADDRESS = '0x1234567890abcdef1234567890abcdef12345678';
```

### Add GenLayer JS SDK

Add before closing `</body>` tag:

```html
<script src="https://unpkg.com/genlayer-js@latest/dist/index.js"></script>
```

### Initialize Client

Replace mock code with:

```javascript
const client = new GenLayerClient({
    endpoint: 'https://studio.genlayer.com/api'
});

const contract = client.getContract(CONTRACT_ADDRESS);
```

### Update Form Handlers

**Create Case:**
```javascript
document.getElementById('createForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const plaintiff = document.getElementById('plaintiff').value;
    const defendant = document.getElementById('defendant').value;
    
    try {
        const tx = await contract.write.create_case(plaintiff, defendant);
        await tx.wait();
        alert('✓ Case created!');
        e.target.reset();
        updateCaseSelectors();
    } catch (error) {
        alert('Error: ' + error.message);
    }
});
```

**Submit Evidence:**
```javascript
document.getElementById('evidenceForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const caseId = parseInt(document.getElementById('caseId').value);
    const party = document.getElementById('party').value;
    const evidence = document.getElementById('evidence').value;
    
    try {
        const tx = await contract.write.submit_evidence(caseId, party, evidence);
        await tx.wait();
        alert('✓ Evidence submitted!');
        e.target.reset();
    } catch (error) {
        alert('Error: ' + error.message);
    }
});
```

**Resolve Case:**
```javascript
document.getElementById('resolveForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const caseId = parseInt(document.getElementById('resolveCaseId').value);
    const btn = e.target.querySelector('button');
    
    btn.disabled = true;
    btn.innerHTML = '<span class="loading"></span> Analyzing...';
    
    try {
        const tx = await contract.write.resolve_case(caseId);
        await tx.wait(); // Takes 30-90 seconds
        
        alert('✓ Case resolved!');
        loadCases();
    } catch (error) {
        alert('Error: ' + error.message);
    } finally {
        btn.disabled = false;
        btn.textContent = 'Resolve Case';
    }
});
```

**Load Cases:**
```javascript
async function loadCases() {
    try {
        const result = await contract.read.get_all_cases();
        cases = result.cases;
        
        // Existing display code...
    } catch (error) {
        console.error('Error loading cases:', error);
    }
}
```

## Part 4: GitHub Repository Setup

### Initialize Repository

```bash
git init
git add .
git commit -m "Initial commit: GenLayer Dispute Resolution dApp"
```

### Create GitHub Repository

1. Go to [github.com/new](https://github.com/new)
2. Repository name: `genlayer-dispute-resolution`
3. Description: "AI-powered dispute resolution on GenLayer"
4. Public repository
5. Don't initialize with README (we have one)
6. Create repository

### Push Code

```bash
git remote add origin https://github.com/yourusername/genlayer-dispute-resolution.git
git branch -M main
git push -u origin main
```

### Enable GitHub Pages (Optional)

1. Repository Settings
2. Pages section
3. Source: main branch
4. Folder: /frontend
5. Save

## Part 5: Configure CI/CD

### Add Vercel Secrets

If using GitHub Actions:

1. Get Vercel token: `vercel login` then `vercel whoami`
2. Get Org ID and Project ID from Vercel project settings
3. Add to GitHub Secrets:
   - `VERCEL_TOKEN`
   - `VERCEL_ORG_ID`
   - `VERCEL_PROJECT_ID`

### Test Workflow

```bash
git add .
git commit -m "Test deployment workflow"
git push
```

Check Actions tab for deployment status.

## Troubleshooting

### Contract Won't Deploy

**Check:**
- First line: `# { "Depends": "py-genlayer:test" }`
- No syntax errors
- Proper indentation
- All decorators present

**Common Issues:**
- Missing `@gl.public.write` or `@gl.public.view`
- Incorrect API names
- Storage type mismatches

### Frontend Connection Fails

**Check:**
- Contract address is correct
- GenLayer JS SDK loaded
- Browser console for errors
- Network connectivity

**Test Contract:**
```javascript
// In browser console
console.log(await contract.read.get_case_count());
```

Should return number without errors.

### Deployment Fails

**Vercel:**
- Check build logs
- Verify no errors in HTML
- Test locally first

**Netlify:**
- Check deploy logs
- Verify all files present
- Test drag-and-drop first

**GitHub Pages:**
- Check Actions tab
- Verify branch is correct
- Wait 5-10 minutes for first deploy

### Resolution Takes Too Long

This is normal! 30-90 seconds is expected for AI consensus.

If it takes >2 minutes:
- Check GenLayer status
- Try again (network might be busy)
- Verify both parties submitted evidence

## Production Checklist

Before going live:

- [ ] Contract deployed and tested
- [ ] All methods work in Studio
- [ ] Frontend deployed successfully
- [ ] Contract address updated in frontend
- [ ] GenLayer JS SDK integrated
- [ ] All form handlers updated
- [ ] Error handling added
- [ ] Loading states implemented
- [ ] Tested full user flow
- [ ] README updated with live links
- [ ] Documentation complete
- [ ] Analytics added (optional)
- [ ] Social media ready

## Monitoring

### Contract Health

Check regularly:
- Transaction success rate
- Average resolution time
- Validator consensus rate
- Error patterns

### Frontend Health

Monitor:
- Page load time
- API response time
- Error rate
- User engagement

### Use GenLayer Studio

- View transaction history
- Check logs for errors
- Monitor validator activity
- Review consensus patterns

## Updating

### Smart Contract Updates

GenLayer contracts are immutable. To update:

1. Deploy new contract version
2. Update frontend with new address
3. Migrate data if needed (manual)
4. Announce to users

### Frontend Updates

```bash
# Make changes
git add .
git commit -m "Update: description"
git push

# Auto-deploys via CI/CD
# Or manually: vercel --prod
```

## Support

**Issues:**
- Check Logs in GenLayer Studio
- Review browser console
- Search GitHub issues

**Help:**
- [GenLayer Discord](https://discord.gg/8Jm4v89VAu)
- [GitHub Discussions](https://github.com/yourusername/genlayer-dispute-resolution/discussions)
- [Documentation](../README.md)

## Next Steps

After deployment:

1. Share on social media
2. Post in GenLayer Discord
3. Write announcement blog post
4. Submit to dApp directories
5. Gather user feedback
6. Plan improvements

Congratulations! Your dApp is live. 🎉
