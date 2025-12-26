# Contributing to LinguaFlow - English Tutor AI

Thank you for your interest in contributing to the English Tutor Bot project! This document provides guidelines and instructions for contributing.

## Code of Conduct

Be respectful and professional in all interactions. We are committed to providing a welcoming and inclusive environment for all contributors.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** to your local machine:
   ```bash
   git clone https://github.com/YOUR-USERNAME/english-tutor-bot.git
   cd english-tutor-bot
   ```

3. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\\Scripts\\activate
   ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Development Workflow

1. **Create a feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following the code style guidelines below

3. **Run tests and linting:**
   ```bash
   flake8 backend/
   black backend/
   isort backend/
   ```

4. **Commit your changes** with clear messages:
   ```bash
   git commit -m "type: Brief description of changes"
   ```

5. **Push to your fork:**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request** with a clear description of changes

## Code Style Guidelines

- Follow PEP 8 standards
- Use Black for code formatting (line length: 100)
- Use meaningful variable and function names
- Add docstrings to all public functions and classes
- Use type hints where applicable
- Keep functions small and focused

## Commit Message Format

Use conventional commits format:
- `feat:` New features
- `fix:` Bug fixes
- `refactor:` Code refactoring
- `docs:` Documentation changes
- `chore:` Maintenance tasks
- `test:` Test-related changes

Example: `feat: Add grammar correction module`

## Testing

- Write tests for new features
- Ensure all existing tests pass
- Aim for good test coverage

## Documentation

- Update README.md if adding new features
- Add docstrings to new functions
- Update CHANGELOG if applicable

## Questions?

Feel free to open an issue for discussions or questions about contributing.

Thank you for contributing! 🚀
