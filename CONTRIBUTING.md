# Contributing to AI-Powered Dispute Resolution

Thank you for your interest in contributing! This project welcomes contributions from everyone.

## Ways to Contribute

- 🐛 Report bugs
- 💡 Suggest features
- 📝 Improve documentation
- 🔧 Submit code improvements
- 🧪 Add test cases
- 🎨 Enhance UI/UX
- 📖 Write tutorials

## Getting Started

### 1. Set Up Development Environment

```bash
# Fork and clone the repository
git clone https://github.com/your-username/dispute-resolution-genlayer.git
cd dispute-resolution-genlayer

# Install dependencies (optional, for local testing)
pip install -r requirements.txt
```

### 2. Test the Contract

Open https://studio.genlayer.com and test the current version to understand how it works.

### 3. Choose What to Work On

Check the Issues tab for:
- `good first issue` - Great for beginners
- `help wanted` - Need community input
- `documentation` - Improve docs
- `enhancement` - New features

## Development Workflow

### Making Changes

1. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Edit the relevant files
   - Follow existing code style
   - Add comments for complex logic

3. **Test your changes**
   - Deploy to GenLayer Studio
   - Run through the full workflow
   - Test edge cases

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "Clear description of changes"
   ```

5. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create Pull Request**
   - Go to the original repository
   - Click "New Pull Request"
   - Describe your changes clearly

## Code Style

### Python (Contracts)

```python
# ✅ Good
@gl.public.write
def submit_evidence(self, case_id: int, party: str, evidence: str):
    """Submit evidence for a specific party."""
    case = self.cases.get(u256(case_id))
    if not case:
        raise Exception("Case not found")
    
    # Extract data before nondet blocks
    evidence_text = evidence
    
    # Rest of logic...

# ❌ Avoid
def submit_evidence(self,case_id:int,party:str,evidence:str):
    # No docstring
    case=self.cases.get(u256(case_id)) # No spaces
    if not case: raise Exception("Case not found") # Multiple statements
```

**Rules:**
- Use type annotations
- Add docstrings for public methods
- Follow PEP 8 style guide
- Use descriptive variable names
- Add comments for non-obvious code

### Markdown (Documentation)

```markdown
# ✅ Good

## Clear Heading

Explanation with concrete example:

​```python
# Working code example
result = get_case(0)
​```

**Key Point**: Always test your code.

# ❌ Avoid

unclear heading
no examples just text walls
```

**Rules:**
- Use clear, descriptive headings
- Include code examples
- Keep paragraphs short
- Use lists for multiple items
- Add emphasis sparingly

## Testing Guidelines

### Before Submitting

Test your changes thoroughly:

**Contract Changes:**
1. Deploy to Studio
2. Run through complete flow
3. Test all affected methods
4. Verify error handling
5. Check edge cases

**Documentation Changes:**
1. Check all links work
2. Verify code examples run
3. Ensure formatting is correct
4. Spell check content
5. Have someone else review

**Test Cases:**
1. Create realistic scenarios
2. Verify expected outcomes
3. Test both success and failure paths
4. Document expected behavior

### Test Checklist

- [ ] Code deploys without errors
- [ ] All methods work as expected
- [ ] Error messages are clear
- [ ] Documentation is updated
- [ ] Examples are tested
- [ ] No breaking changes (or documented if necessary)

## Pull Request Guidelines

### PR Title Format

Use clear, descriptive titles:

```
✅ Good:
- "Add multi-party dispute support"
- "Fix storage access in nondet blocks"
- "Update API documentation with examples"

❌ Avoid:
- "Update"
- "Fix bug"
- "Changes"
```

### PR Description Template

```markdown
## What Changed

Brief description of what you changed and why.

## Type of Change

- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Code refactoring
- [ ] Other (please describe)

## Testing

How did you test these changes?

- [ ] Deployed to Studio
- [ ] Ran full workflow
- [ ] Tested edge cases
- [ ] Updated tests

## Screenshots (if applicable)

Add screenshots showing the changes in action.

## Checklist

- [ ] Code follows project style
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] Tests pass
- [ ] No breaking changes (or documented)
```

## Contribution Categories

### Bug Fixes

When reporting bugs:

```markdown
**Bug Description**
Clear description of the issue.

**Steps to Reproduce**
1. Step one
2. Step two
3. See error

**Expected Behavior**
What should happen.

**Actual Behavior**
What actually happens.

**Screenshots/Error Messages**
Include relevant output.

**Environment**
- Browser: Chrome 120
- GenLayer Studio version: Latest
- Date: 2026-01-16
```

When fixing bugs:
- Reference the issue number
- Explain root cause
- Describe the fix
- Add test to prevent regression

### New Features

Before implementing:
1. Open an issue to discuss
2. Get feedback from maintainers
3. Ensure it aligns with project goals

When implementing:
- Keep changes focused
- Update documentation
- Add examples
- Include tests

### Documentation

Documentation improvements always welcome:

**Types of doc contributions:**
- Fix typos
- Clarify confusing sections
- Add missing examples
- Improve formatting
- Translate to other languages

**Doc standards:**
- Use simple, clear language
- Include working code examples
- Test all code samples
- Link related sections
- Keep it beginner-friendly

## Code of Conduct

### Be Respectful

- Welcome newcomers
- Be patient with questions
- Provide constructive feedback
- Assume good intentions
- Help others learn

### Be Professional

- Keep discussions on-topic
- No harassment or discrimination
- Respect different viewpoints
- Give credit where due
- Maintain confidentiality

### Be Collaborative

- Share knowledge openly
- Ask for help when needed
- Review others' PRs thoughtfully
- Celebrate successes
- Learn from mistakes

## Review Process

### What Happens After You Submit

1. **Automatic Checks** - Code style, tests
2. **Maintainer Review** - Usually within 48 hours
3. **Feedback** - Changes requested or approved
4. **Merge** - Once approved and tests pass

### During Review

- Respond to feedback promptly
- Make requested changes
- Ask questions if unclear
- Be open to suggestions
- Update as needed

### After Merge

- Your contribution becomes part of the project
- You'll be added to contributors list
- Share your contribution!

## Getting Help

Stuck? Need guidance?

- **Discord**: Join the GenLayer Discord for quick help
- **Issues**: Open an issue for project-specific questions
- **Discussions**: Use GitHub Discussions for open-ended topics
- **Documentation**: Check docs/ folder for guides

## Recognition

Contributors are recognized in:

- Contributors section of README
- Release notes for significant contributions
- Special thanks in documentation
- Community showcase

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Questions?

Still have questions about contributing?

- Check the [FAQ](docs/FAQ.md)
- Read the [documentation](docs/)
- Open a [discussion](https://github.com/your-repo/discussions)
- Ask For greyw0rks in [Discord](https://discord.gg/8Jm4v89VAu)

---

**Thank you for contributing!** Every contribution, no matter how small, makes this project better. 🚀
