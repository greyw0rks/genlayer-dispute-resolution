# Contributing to GenLayer Dispute Resolution

Thank you for your interest in contributing! This project is open source and welcomes contributions.

## How to Contribute

### Reporting Bugs

1. Check if the bug already exists in Issues
2. If not, create a new issue with:
   - Clear title
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots if applicable
   - Your environment (browser, OS)

### Suggesting Features

1. Check existing issues for similar suggestions
2. Create new issue with:
   - Clear use case
   - Why it's valuable
   - How it might work

### Code Contributions

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test thoroughly
5. Commit with clear messages (`git commit -m 'Add amazing feature'`)
6. Push to branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Development Setup

### Prerequisites

- Python 3.10+
- Web browser
- GenLayer Studio account

### Local Development

```bash
# Clone your fork
git clone https://github.com/yourusername/genlayer-dispute-resolution.git
cd genlayer-dispute-resolution

# Test contract
# Copy contracts/dispute_resolution.py to GenLayer Studio
# Deploy and test

# Run frontend locally
cd frontend
python -m http.server 8000
```

### Testing

Before submitting PR:

1. Test contract in GenLayer Studio
2. Verify all methods work
3. Test frontend functionality
4. Check console for errors
5. Test on different browsers

## Code Style

### Python (Smart Contract)

- Follow PEP 8
- Use type hints
- Add docstrings for public methods
- Keep functions focused and small

```python
@gl.public.write
def create_case(self, plaintiff: str, defendant: str) -> None:
    """
    Create a new dispute case
    
    Args:
        plaintiff: Name of party bringing dispute
        defendant: Name of party being accused
    """
    # Implementation
```

### JavaScript (Frontend)

- Use clear variable names
- Comment complex logic
- Keep functions small
- Handle errors gracefully

```javascript
async function createCase(plaintiff, defendant) {
    try {
        const tx = await contract.write.create_case(plaintiff, defendant);
        await tx.wait();
        showSuccess('Case created!');
    } catch (error) {
        showError('Failed to create case: ' + error.message);
    }
}
```

### HTML/CSS

- Semantic HTML
- Accessible design
- Responsive layouts
- Clear class names

## Pull Request Guidelines

### Title Format

- `feat: Add case categories`
- `fix: Resolve evidence submission bug`
- `docs: Update deployment guide`
- `style: Improve mobile responsiveness`

### Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
How was this tested?

## Screenshots
If applicable

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-reviewed code
- [ ] Commented complex logic
- [ ] Updated documentation
- [ ] No breaking changes (or documented)
- [ ] Tested in GenLayer Studio
```

## Areas for Contribution

### High Priority

- [ ] Evidence file upload support
- [ ] Case categories (contract, product, service)
- [ ] Better error handling
- [ ] Mobile optimization
- [ ] Loading states

### Medium Priority

- [ ] Appeal mechanism
- [ ] Multi-language support
- [ ] Analytics dashboard
- [ ] Email notifications
- [ ] Export case reports

### Low Priority

- [ ] Dark mode toggle
- [ ] Case templates
- [ ] Batch operations
- [ ] Advanced filtering
- [ ] Case statistics

## Documentation

When adding features:

1. Update README.md
2. Add to appropriate docs/ file
3. Update API documentation
4. Include code examples

## Community

- Join [GenLayer Discord](https://discord.gg/8Jm4v89VAu)
- Follow development in GitHub Discussions
- Help answer questions in Issues
- Share your use cases

## Code of Conduct

Be respectful and constructive:

- Use welcoming language
- Respect differing viewpoints
- Accept constructive criticism
- Focus on what's best for community
- Show empathy

## Questions?

- Check [docs/](docs/) folder
- Search existing issues
- Ask in Discord
- Create new discussion

## License

By contributing, you agree your contributions will be licensed under MIT License.

## Recognition

Contributors will be:
- Listed in README.md
- Mentioned in release notes
- Credited in documentation

Thank you for making this project better! 🙏
