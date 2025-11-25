# Client Treatment Organizer

A file manager integration tool that bridges the gap between existing client file systems and treatment management workflows. This tool enables seamless organization, tracking, and access to client treatment files without disrupting existing folder structures.

## Overview

Client Treatment Organizer is designed for healthcare professionals (particularly Speech and Language Pathologists) who maintain client files in existing folder structures and need a unified way to organize, track, and manage treatment documentation alongside their current file management system.

## Key Features (Planned)

### Core Integration
- **Context Menu Integration**: Right-click on client folders for quick actions
- **File Watcher**: Real-time synchronization with existing folder structures
- **Folder Parser**: Automatically detect and catalog existing client folders
- **Metadata Management**: Attach metadata to files without modifying originals

### File Management
- **Import/Export Bridge**: Two-way sync between app and existing folders
- **Smart Categorization**: Auto-organize files by type (notes, evaluations, reports, etc.)
- **Document Tagging**: Tag files with treatment phases, dates, and client info
- **Quick Access**: Rapid file lookup and opening

### Organization
- **Client Tracking**: Monitor treatment progress across all files
- **Session Logging**: Track session dates and outcomes from file metadata
- **Treatment Timeline**: Visual timeline of client treatment from file dates
- **Batch Operations**: Organize multiple files at once

### Reporting
- **Treatment Summaries**: Generate summaries from existing documentation
- **Progress Reports**: Create reports from file metadata and tags
- **Export Functionality**: Export organized data to various formats

## Project Structure

```
Client_treatment_Organizer/
├── src/
│   ├── core/
│   │   ├── file_scanner.py
│   │   ├── metadata_manager.py
│   │   └── folder_parser.py
│   ├── integrations/
│   │   ├── context_menu.py
│   │   ├── file_watcher.py
│   │   └── shell_extension.py
│   ├── ui/
│   │   ├── main_window.py
│   │   ├── dialogs.py
│   │   └── styles.py
│   ├── utils/
│   │   ├── config.py
│   │   ├── validators.py
│   │   └── helpers.py
│   └── __init__.py
├── tests/
│   ├── test_file_scanner.py
│   ├── test_metadata_manager.py
│   └── test_integrations.py
├── docs/
│   ├── ARCHITECTURE.md
│   ├── SETUP.md
│   ├── USAGE.md
│   └── INTEGRATION_GUIDE.md
├── assets/
│   ├── icons/
│   └── screenshots/
├── .github/
│   └── workflows/
│       └── ci.yml
├── requirements.txt
├── setup.py
├── LICENSE
├── .gitignore
└── README.md
```

## Getting Started

### Prerequisites
- Python 3.7+
- Windows 7+ (for context menu integration)
- File system with existing client folder structure

### Installation

```bash
# Clone the repository
git clone https://github.com/DrDisc/Client_treatment_Organizer.git

# Install dependencies
cd Client_treatment_Organizer
pip install -r requirements.txt

# Run the application
python -m src.main
```

## Integration Modes

### 1. Context Menu Integration
Add shortcuts to Windows Explorer right-click menu for quick access to client folders.

### 2. File Watcher
Continuously monitor existing client folders and synchronize changes with the application.

### 3. Import/Export
Bidirectional sync between your existing folder structure and the application's database.

### 4. Folder Parser
Automatically scan and analyze existing client folder structures to build an index.

## Documentation

- [Architecture Overview](docs/ARCHITECTURE.md) - System design and component breakdown
- [Setup Guide](docs/SETUP.md) - Installation and configuration
- [User Guide](docs/USAGE.md) - How to use the application
- [Integration Guide](docs/INTEGRATION_GUIDE.md) - Detailed integration strategies

## Roadmap

### Phase 1: Core Infrastructure
- [x] Project setup
- [ ] File scanning and catalog system
- [ ] Metadata management framework
- [ ] Basic UI

### Phase 2: Integration Features
- [ ] Context menu integration
- [ ] File watcher implementation
- [ ] Folder parser enhancement

### Phase 3: Advanced Features
- [ ] Treatment timeline visualization
- [ ] Reporting system
- [ ] Advanced search and filtering

### Phase 4: Polish & Release
- [ ] Testing and quality assurance
- [ ] Documentation completion
- [ ] Executable build

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Important Notes

⚠️ **Data Privacy**: This application works with sensitive healthcare information. Always ensure proper data privacy and security measures are in place.

- Do not commit real client data to this repository
- Back up your client files regularly
- Keep your computer and application secure
- Follow HIPAA and local privacy regulations

## Support

For issues, questions, or suggestions, please open an issue on the GitHub repository.

---

**Note**: This application is designed to work alongside existing file managers, not replace them. It enhances your current workflow without disrupting your established systems.
