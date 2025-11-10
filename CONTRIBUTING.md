# Contributing to FIBO BrandGuard

Thank you for your interest in contributing to FIBO BrandGuard! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/fibo-brandguard.git`
3. Create a new branch: `git checkout -b feature/your-feature-name`
4. Install dependencies: `pip install -r requirements.txt`

## Development Workflow

### Running Tests

Test individual modules:
```bash
python3 -c "from vlm_agent import VLMAgent; print('VLM Agent OK')"
python3 -c "from policy_engine import PolicyEngine; print('Policy Engine OK')"
python3 -c "from fibo_client import FIBOClient; print('FIBO Client OK')"
python3 -c "from audit_log import AuditLog; print('Audit Log OK')"
```

Run the demo:
```bash
python3 demo.py
```

### Running the App

```bash
streamlit run app.py
```

## Code Style

- Follow PEP 8 Python style guidelines
- Use docstrings for all functions and classes
- Keep functions focused and modular
- Add comments for complex logic

## Module Structure

- **vlm_agent.py**: Handles JSON prompt construction
- **policy_engine.py**: Enforces brand policies
- **fibo_client.py**: Manages FIBO API interaction
- **audit_log.py**: Maintains audit trail
- **app.py**: Main Streamlit interface
- **brand_profile.json**: Brand configuration

## Submitting Changes

1. Ensure your code passes all tests
2. Update documentation if needed
3. Commit your changes with clear messages
4. Push to your fork
5. Submit a pull request

## Feature Ideas

- Integration with real Bria FIBO API
- Additional policy validation rules
- Export audit logs to CSV/PDF
- Multi-language support
- Custom brand profile editor
- Image comparison tools
- Batch processing capabilities

## Bug Reports

Please include:
- Description of the issue
- Steps to reproduce
- Expected vs actual behavior
- Python version and OS
- Error messages/logs

## Questions?

Open an issue for discussion!

## License

By contributing, you agree to license your contributions under the MIT License.
