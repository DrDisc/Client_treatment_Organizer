# Integration Guide

This document describes the various integration methods available in Client Treatment Organizer and how to implement them.

## Integration Modes Overview

### 1. Context Menu Integration
**Complexity**: Low  
**Platform**: Windows  
**Use Case**: Quick access to client folders from Explorer

### 2. File Watcher Integration
**Complexity**: Medium  
**Platform**: Cross-platform  
**Use Case**: Real-time synchronization with folder changes

### 3. Folder Parser Integration
**Complexity**: Medium  
**Platform**: Cross-platform  
**Use Case**: Automatic detection of existing client structures

### 4. Shell Extension Integration
**Complexity**: High  
**Platform**: Windows (requires C++)  
**Use Case**: Deep integration with Windows Explorer

## 1. Context Menu Integration

### How It Works
When users right-click on a client folder in Windows Explorer, they see a "Open with Client Treatment Organizer" option that launches the app with that folder as context.

### Windows Registry Setup

```registry
Windows Registry Editor Version 5.00

[HKEY_CLASSES_ROOT\Directory\shell\Client_Treatment_Organizer]
@="Open with Client Treatment Organizer"
"Icon"="C:\\Program Files\\Client_Treatment_Organizer\\icon.ico"

[HKEY_CLASSES_ROOT\Directory\shell\Client_Treatment_Organizer\command]
@="C:\\Program Files\\Client_Treatment_Organizer\\client_treatment_organizer.exe \"%1\""
```

### Implementation in Python

```python
# integrations/context_menu.py

import winreg
import os
from pathlib import Path

class ContextMenuIntegration:
    def __init__(self, app_path, icon_path):
        self.app_path = app_path
        self.icon_path = icon_path
    
    def install(self):
        """Install context menu entry in Windows Registry"""
        try:
            # Open Registry
            key = winreg.CreateKey(
                winreg.HKEY_CLASSES_ROOT,
                r'Directory\shell\Client_Treatment_Organizer'
            )
            
            # Set display name
            winreg.SetValueEx(key, '', 0, winreg.REG_SZ, 
                            'Open with Client Treatment Organizer')
            
            # Set icon
            winreg.SetValueEx(key, 'Icon', 0, winreg.REG_SZ, 
                            self.icon_path)
            
            # Create command subkey
            cmd_key = winreg.CreateKey(key, 'command')
            
            # Set command
            command = f'"{self.app_path}" "%1"'
            winreg.SetValueEx(cmd_key, '', 0, winreg.REG_SZ, command)
            
            winreg.CloseKey(key)
            winreg.CloseKey(cmd_key)
            
            return True
        except Exception as e:
            print(f"Failed to install context menu: {e}")
            return False
    
    def uninstall(self):
        """Remove context menu entry from Windows Registry"""
        try:
            winreg.DeleteTree(
                winreg.HKEY_CLASSES_ROOT,
                r'Directory\shell\Client_Treatment_Organizer'
            )
            return True
        except Exception as e:
            print(f"Failed to uninstall context menu: {e}")
            return False
```

### Command-Line Arguments
When context menu opens the app, pass the folder path:
```bash
client_treatment_organizer.exe "C:\Users\User\Client_Files\John_Doe"
```

## 2. File Watcher Integration

### How It Works
Continuously monitors client folders for changes (new files, deletions, modifications) and synchronizes with the metadata database in real-time.

### Implementation

```python
# integrations/file_watcher.py

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileModifiedEvent
import os
from pathlib import Path

class ClientFolderHandler(FileSystemEventHandler):
    def __init__(self, metadata_manager, callback=None):
        self.metadata_manager = metadata_manager
        self.callback = callback
    
    def on_created(self, event):
        if not event.is_directory:
            print(f"New file detected: {event.src_path}")
            self.metadata_manager.index_file(event.src_path)
            if self.callback:
                self.callback('created', event.src_path)
    
    def on_modified(self, event):
        if not event.is_directory:
            print(f"File modified: {event.src_path}")
            self.metadata_manager.update_file_metadata(event.src_path)
            if self.callback:
                self.callback('modified', event.src_path)
    
    def on_deleted(self, event):
        if not event.is_directory:
            print(f"File deleted: {event.src_path}")
            self.metadata_manager.remove_file_metadata(event.src_path)
            if self.callback:
                self.callback('deleted', event.src_path)
    
    def on_moved(self, event):
        if not event.is_directory:
            print(f"File moved: {event.src_path} -> {event.dest_path}")
            self.metadata_manager.move_file_metadata(
                event.src_path, 
                event.dest_path
            )
            if self.callback:
                self.callback('moved', event.src_path, event.dest_path)

class FileWatcher:
    def __init__(self, metadata_manager):
        self.metadata_manager = metadata_manager
        self.observer = Observer()
        self.watched_paths = {}
    
    def watch_client_folder(self, folder_path, callback=None):
        """Start watching a client folder for changes"""
        handler = ClientFolderHandler(
            self.metadata_manager, 
            callback=callback
        )
        
        watch = self.observer.schedule(
            handler,
            folder_path,
            recursive=True
        )
        
        self.watched_paths[folder_path] = watch
        
        if not self.observer.is_alive():
            self.observer.start()
    
    def unwatch_folder(self, folder_path):
        """Stop watching a folder"""
        if folder_path in self.watched_paths:
            self.observer.unschedule(self.watched_paths[folder_path])
            del self.watched_paths[folder_path]
    
    def stop_all(self):
        """Stop all file watching"""
        self.observer.stop()
        self.observer.join()
```

### Configuration
File watcher settings in `config.yaml`:
```yaml
file_watcher:
  enabled: true
  watch_interval: 1  # seconds
  recursive: true
  ignored_patterns:
    - "*.tmp"
    - "~*"
    - ".~*"
  events:
    - created
    - modified
    - deleted
    - moved
```

## 3. Folder Parser Integration

### How It Works
Analyzes existing folder structures to automatically detect client folders and suggest categorization without requiring user configuration.

### Implementation

```python
# core/folder_parser.py

import os
import re
from pathlib import Path
from collections import defaultdict

class FolderParser:
    def __init__(self):
        self.client_patterns = [
            r'^[A-Z][a-z]+_[A-Z][a-z]+',  # FirstName_LastName
            r'^[A-Z]{2}\d{3,4}',           # ID format (JD001)
            r'^\d{4}-\d{2}-\d{2}',         # Date-based
            r'^Client_\d+',                # Client_1, Client_2
        ]
    
    def parse_structure(self, root_path):
        """Analyze folder structure and return analysis results"""
        analysis = {
            'total_folders': 0,
            'total_files': 0,
            'detected_clients': [],
            'folder_hierarchy': {},
            'file_categories': defaultdict(int),
            'date_patterns': []
        }
        
        # Walk through directory
        for root, dirs, files in os.walk(root_path):
            analysis['total_folders'] += len(dirs)
            analysis['total_files'] += len(files)
            
            # Categorize files
            for file in files:
                category = self._categorize_file(file)
                analysis['file_categories'][category] += 1
        
        # Detect client folders
        analysis['detected_clients'] = self._detect_clients(
            root_path
        )
        
        return analysis
    
    def _detect_clients(self, root_path):
        """Detect likely client folders based on naming patterns"""
        clients = []
        
        for item in os.listdir(root_path):
            item_path = os.path.join(root_path, item)
            
            if os.path.isdir(item_path):
                for pattern in self.client_patterns:
                    if re.match(pattern, item):
                        clients.append({
                            'name': item,
                            'path': item_path,
                            'confidence': self._calculate_confidence(
                                item, 
                                item_path
                            )
                        })
                        break
        
        return sorted(clients, 
                     key=lambda x: x['confidence'], 
                     reverse=True)
    
    def _categorize_file(self, filename):
        """Categorize file by extension and naming"""
        ext = os.path.splitext(filename)[1].lower()
        
        categories = {
            '.pdf': 'documents',
            '.docx': 'documents',
            '.doc': 'documents',
            '.txt': 'notes',
            '.xlsx': 'data',
            '.csv': 'data',
            '.jpg': 'images',
            '.png': 'images',
            '.mp3': 'audio',
            '.mp4': 'video',
        }
        
        return categories.get(ext, 'other')
    
    def _calculate_confidence(self, folder_name, folder_path):
        """Calculate confidence score for client folder detection"""
        score = 0
        
        # Name format matching
        if re.match(self.client_patterns[0], folder_name):
            score += 40
        elif re.match(self.client_patterns[1], folder_name):
            score += 30
        
        # Has subdirectories (typical of client folders)
        if os.listdir(folder_path):
            score += 20
        
        # Contains common file types
        files = [f for f in os.listdir(folder_path) 
                if os.path.isfile(os.path.join(folder_path, f))]
        if files:
            score += 10
        
        return min(score, 100)  # Cap at 100
```

## 4. Shell Extension Integration (Advanced)

### How It Works
Creates a custom Windows Explorer extension with overlay icons and toolbar buttons.

### Requirements
- Windows SDK
- C++ knowledge or pre-built extension library
- Administrator privileges for installation

### High-Level Overview
```cpp
// Example structure (simplified)
class ClientOrganizerShellExt : public IContextMenu, IShellExtInit {
    // Implement interface methods
    // Add custom menu items
    // Add overlay icons
    // Handle commands
};
```

This requires compilation and separate installation. Consider using Python-based solutions first.

## Choosing the Right Integration

| Need | Integration | Complexity | Platform |
|------|-------------|-----------|----------|
| Quick access to folders | Context Menu | Low | Windows |
| Real-time sync | File Watcher | Medium | Cross-platform |
| Auto-detect structure | Folder Parser | Medium | Cross-platform |
| Deep Explorer integration | Shell Extension | High | Windows only |

## Best Practices

1. **Always Test First**: Test integration before releasing to users
2. **Provide Uninstall**: Make it easy to remove integrations
3. **Non-Destructive**: Never modify original files
4. **Error Handling**: Graceful failure if integration points fail
5. **User Consent**: Ask permission before installing registry changes
6. **Documentation**: Document all integration methods clearly
7. **Backward Compatibility**: Support both integrated and standalone modes
