# 🤝 Contributing Guide

Thank you for considering contributing to the Multimodal Explanation System!

## How to Contribute

### 1. Reporting Bugs

If you find a bug, please create an issue with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, browser, versions)
- Screenshots or error logs if applicable

### 2. Suggesting Features

Feature requests are welcome! Please include:
- Clear description of the feature
- Use case and benefits
- Potential implementation approach
- Any relevant examples or mockups

### 3. Code Contributions

#### Getting Started

1. Fork the repository
2. Clone your fork:
```bash
git clone https://github.com/yourusername/multimodal-explanation-system.git
```

3. Create a feature branch:
```bash
git checkout -b feature/your-feature-name
```

4. Make your changes
5. Test thoroughly
6. Commit with clear messages
7. Push to your fork
8. Create a Pull Request

#### Code Style

**Python (Backend)**
- Follow PEP 8 style guide
- Use type hints where appropriate
- Add docstrings to functions
- Keep functions focused and small

```python
def analyze_image(self, image_data: bytes) -> dict:
    """
    Analyze image using vision models.
    
    Args:
        image_data: Raw image bytes
        
    Returns:
        Dictionary containing analysis results
    """
    pass
```

**JavaScript/React (Frontend)**
- Use functional components with hooks
- Follow React best practices
- Use meaningful variable names
- Add comments for complex logic

```javascript
// Good
const handleImageUpload = async (file) => {
  // Process and upload image
}

// Avoid
const h = (f) => { /* ... */ }
```

**CSS**
- Use BEM naming convention
- Keep selectors specific but not overly nested
- Use CSS variables for colors and spacing

```css
.component-name {
  /* styles */
}

.component-name__element {
  /* styles */
}

.component-name--modifier {
  /* styles */
}
```

#### Testing

- Add tests for new features
- Ensure existing tests pass
- Test manually before submitting PR

#### Commit Messages

Use clear, descriptive commit messages:

```
feat: Add support for PDF uploads
fix: Resolve audio playback issue on Safari
docs: Update installation instructions
refactor: Simplify vision service logic
test: Add unit tests for speech service
```

Prefixes:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

### 4. Documentation

Improvements to documentation are always welcome:
- Fix typos or unclear explanations
- Add examples or tutorials
- Improve code comments
- Create guides for specific use cases

## Development Workflow

### 1. Set Up Development Environment

```bash
# Install dependencies
cd backend && pip install -r requirements.txt
cd ../frontend && npm install

# Set up environment variables
cp backend/.env.example backend/.env
# Edit .env with your API keys
```

### 2. Run in Development Mode

```bash
# Terminal 1: Backend
cd backend
python app.py

# Terminal 2: Frontend
cd frontend
npm run dev
```

### 3. Make Changes

- Write clean, documented code
- Follow existing patterns
- Keep changes focused
- Test as you go

### 4. Test Your Changes

```bash
# Backend tests (when available)
cd backend
pytest

# Frontend tests (when available)
cd frontend
npm test

# Manual testing
# Follow TESTING.md checklist
```

### 5. Submit Pull Request

- Push to your fork
- Create PR with clear description
- Reference any related issues
- Wait for review

## Areas for Contribution

### High Priority
- [ ] Add comprehensive test suite
- [ ] Improve error handling
- [ ] Enhance annotation accuracy
- [ ] Optimize performance
- [ ] Add more vision models

### Medium Priority
- [ ] Multi-language support
- [ ] User authentication
- [ ] Database integration
- [ ] Advanced caching
- [ ] Mobile app

### Nice to Have
- [ ] Video support
- [ ] 3D model analysis
- [ ] Collaborative features
- [ ] Plugin system
- [ ] Custom model training

## Code Review Process

1. Maintainer reviews PR
2. Feedback provided if needed
3. Author makes requested changes
4. Approval and merge

## Community Guidelines

- Be respectful and inclusive
- Help others learn and grow
- Provide constructive feedback
- Follow code of conduct

## Questions?

- Open an issue for questions
- Check existing documentation
- Review closed issues for similar questions

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Credited in documentation

Thank you for contributing! 🎉
