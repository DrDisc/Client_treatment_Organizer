# Architecture Overview

## System Design

The Client Treatment Organizer is built around a modular architecture that separates concerns and enables independent integration of various components.

### High-Level Architecture

```
┌─────────────────────────────────────────────────┐
│            User Interface Layer                 │
│  (Main Window, Dialogs, Visualizations)        │
└────────────────┬────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────┐
│         Integration Layer                       │
│  (Context Menu, File Watcher, Shell Ext)       │
└────────────────┬────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────┐
│          Core Services Layer                    │
│  (File Scanner, Metadata Manager, Parser)      │
└────────────────┬────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────┐
│         Data Management Layer                   │
│  (Database, File System, Configuration)        │
└─────────────────────────────────────────────────┘
```

## Core Components

### 1. File Scanner (`core/file_scanner.py`)
**Responsibility**: Scan and index client folders

**Key Methods**:
- `scan_directory()` - Recursively scan a directory
- `get_file_metadata()` - Extract metadata from files
- `build_file_index()` - Create an index of all files
- `detect_client_folders()` - Identify client folder patterns

**Data Output**:
- File index with paths, timestamps, sizes
- Detected client folder structure
- Metadata catalog

### 2. Metadata Manager (`core/metadata_manager.py`)
**Responsibility**: Store and retrieve file metadata without modifying originals

**Key Methods**:
- `add_metadata()` - Attach metadata to a file path
- `get_metadata()` - Retrieve metadata for a file
- `update_metadata()` - Modify existing metadata
- `remove_metadata()` - Remove metadata association
- `export_metadata()` - Export all metadata to formats

**Storage**:
- Uses JSON/YAML configuration files (in `.client_organizer/` folders)
- One metadata file per client folder
- Non-destructive (never modifies original files)

### 3. Folder Parser (`core/folder_parser.py`)
**Responsibility**: Analyze and understand existing folder structures

**Key Methods**:
- `parse_structure()` - Analyze folder naming conventions
- `detect_client_naming()` - Identify client naming patterns
- `map_folder_hierarchy()` - Create folder structure map
- `suggest_categorization()` - Recommend file categories

**Pattern Detection**:
- Client ID patterns (e.g., "JD001", "John_Doe")
- Date-based structures (e.g., YYYY/MM/DD)
- Document type patterns (notes, reports, evaluations)

### 4. Integration Manager (`integrations/`)
Handles all integration points with the system:

#### Context Menu Integration (`integrations/context_menu.py`)
- Windows Registry modifications
- Right-click menu entries
- Quick action handlers

#### File Watcher (`integrations/file_watcher.py`)
- Real-time folder monitoring using `watchdog`
- Change detection (new files, deletions, renames)
- Metadata synchronization triggers

#### Shell Extension (`integrations/shell_extension.py`)
- Custom file manager extension points
- Overlay icons
- Toolbar integration (future)

### 5. UI Layer (`ui/`)
**Components**:
- `main_window.py` - Primary application window
- `dialogs.py` - All dialog windows (import, settings, etc.)
- `styles.py` - Styling and theming

## Data Flow

### Scanning Workflow
```
User Selects Folder
        ↓
File Scanner reads directory
        ↓
Metadata Manager indexes results
        ↓
Folder Parser analyzes structure
        ↓
Results displayed in UI
        ↓
User can tag/organize files
        ↓
Metadata saved (no original files modified)
```

### File Watching Workflow
```
File Watcher monitors folder
        ↓
Change detected (new/modified/deleted file)
        ↓
Metadata Manager updates index
        ↓
UI updates in real-time
        ↓
User can review changes
```

### Import/Export Workflow
```
User initiates import from existing folder
        ↓
Folder Parser analyzes structure
        ↓
File Scanner indexes all files
        ↓
Metadata Manager creates associations
        ↓
Data exported to standard formats
        ↓
Can be synced with other tools
```

## Database Schema

### Metadata Structure
```json
{
  "client_id": "string",
  "client_name": "string",
  "files": [
    {
      "path": "string",
      "name": "string",
      "size": "integer",
      "created_date": "ISO 8601",
      "modified_date": "ISO 8601",
      "file_type": "string",
      "category": "string",
      "tags": ["array", "of", "tags"],
      "notes": "string"
    }
  ],
  "sessions": [
    {
      "date": "ISO 8601",
      "duration": "integer",
      "notes": "string",
      "documents": ["file_paths"]
    }
  ],
  "treatment_timeline": [
    {
      "date": "ISO 8601",
      "event": "string",
      "files": ["associated_file_paths"]
    }
  ]
}
```

## Integration Points

### Windows Context Menu
- Registry: `HKEY_CLASSES_ROOT\Directory\shell\Client_Treatment_Organizer`
- Action: Open folder in application with context

### File Watcher Integration
- Libraries: `watchdog` for cross-platform file monitoring
- Events: Created, Modified, Deleted, Moved

### Import/Export Formats
- JSON: Native format for metadata
- CSV: Spreadsheet export
- XML: For compatibility with other tools
- YAML: Configuration and simple metadata

## Design Principles

1. **Non-Destructive**: Never modify original client files
2. **Modular**: Each component can function independently
3. **Extensible**: Easy to add new integration points
4. **User-Centric**: Keeps user's existing workflow intact
5. **Privacy-First**: All data stored locally
6. **Performance**: Efficient file scanning and indexing

## Dependencies

### Core Libraries
- `watchdog`: File system monitoring
- `python-docx`: Word document handling
- `PyPDF2`: PDF handling
- `python-dateutil`: Date/time utilities
- `pyyaml`: Configuration management

### Standard Library
- `pathlib`: File system operations
- `json`: Data serialization
- `sqlite3`: Optional local database
- `tkinter`: GUI (built-in)

## Scalability Considerations

- Handles thousands of files through efficient indexing
- Lazy loading of metadata
- Asynchronous file watching
- Configurable monitoring depth
- Database optimization for large datasets
