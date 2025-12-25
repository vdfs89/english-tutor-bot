# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-05-22

### Added

- **Core:** Initial release of LinguaFlow AI.
- **Python App:** Streamlit interface (`interface_streamlit.py`) featuring:
  - Real-time chat with Llama 3 via Groq API.
  - Voice interaction (Speech-to-Text & Text-to-Speech).
  - Study tools for generating weekly plans and video recommendations.
- **Web:** Landing page (`index.html`) to navigate between Flutter, HTML, and Python versions.
- **CI/CD:** GitHub Actions workflow (`manual.yml`) to build and deploy to GitHub Pages.
- **Docs:** Added `README.md`, `CONTRIBUTING.md`, `LICENSE.md`, and `CHANGELOG.md`.

### Changed

- **UX:** Improved microphone error handling in the Python application.
- **Config:** Updated `.gitignore` to exclude build artifacts and secrets.
- **Deploy:** Configured workflow to publish Python source code alongside web versions.
- **Auth:** Added support for Streamlit Community Cloud secrets (`st.secrets`).

### Fixed

- Formatting issues in `README.md` (markdown linting).
- Inline styles removed from `index.html` for better code quality.
- GitHub Actions permissions for deploying to `gh-pages`.