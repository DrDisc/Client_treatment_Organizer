#!/usr/bin/env python
"""
Build script to create Windows executable using PyInstaller
Run: python build_exe.py
"""

import os
import sys
import subprocess
from pathlib import Path

def check_requirements():
    """Check if required packages are installed"""
    try:
        import PyInstaller
        print("✓ PyInstaller is installed")
    except ImportError:
        print("✗ PyInstaller not found. Installing...")
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "pyinstaller", "pillow"
        ])

def create_icon():
    """Create a simple icon for the application"""
    icon_path = Path("assets/icon.ico")
    
    if icon_path.exists():
        print(f"✓ Icon already exists at {icon_path}")
        return str(icon_path)
    
    print("Creating application icon...")
    try:
        from PIL import Image, ImageDraw
        
        # Create assets directory if it doesn't exist
        icon_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Create a simple icon (512x512)
        img = Image.new('RGB', (512, 512), color='white')
        draw = ImageDraw.Draw(img)
        
        # Draw a simple speech bubble shape
        # Outer rectangle
        draw.rectangle([50, 50, 462, 400], outline='#2E7D32', width=5, fill='#C8E6C9')
        
        # Triangle pointer
        draw.polygon([462, 400, 462, 450, 412, 400], fill='#C8E6C9', outline='#2E7D32')
        
        # Text
        draw.text((100, 150), "CTO", fill='#1B5E20', font=None)
        
        # Convert to ICO format
        img = img.convert('P')
        img.save(str(icon_path), 'ICO')
        
        print(f"✓ Icon created at {icon_path}")
        return str(icon_path)
    
    except ImportError:
        print("⚠ Pillow not installed, skipping icon creation")
        return None
    except Exception as e:
        print(f"⚠ Error creating icon: {e}")
        return None

def build_executable(icon_path=None):
    """Build the executable using PyInstaller"""
    print("\nBuilding executable...")
    
    # Build PyInstaller command
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=Client Treatment Organizer",
        "--onefile",
        "--windowed",
        "--distpath=dist",
        "--workpath=build",
        "--specpath=.",
    ]
    
    # Add icon if available
    if icon_path and os.path.exists(icon_path):
        cmd.append(f"--icon={icon_path}")
    
    # Add data files
    cmd.append("--add-data=src:src")
    
    # Add the main entry point
    cmd.append("src/main.py")
    
    print(f"Running: {' '.join(cmd)}")
    
    try:
        subprocess.check_call(cmd)
        print("\n✓ Executable built successfully!")
        
        exe_path = Path("dist/Client Treatment Organizer.exe")
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print(f"✓ Output: {exe_path} ({size_mb:.1f} MB)")
            return True
        else:
            print(f"✗ Executable not found at expected location")
            return False
    
    except subprocess.CalledProcessError as e:
        print(f"✗ Build failed with error: {e}")
        return False

def cleanup():
    """Clean up build artifacts"""
    print("\nCleaning up build artifacts...")
    import shutil
    
    for path in ["build", "__pycache__"]:
        if os.path.exists(path):
            shutil.rmtree(path)
            print(f"✓ Removed {path}")

def main():
    """Main build process"""
    print("=" * 60)
    print("Client Treatment Organizer - Build Script")
    print("=" * 60)
    
    # Check requirements
    check_requirements()
    
    # Create icon
    icon_path = create_icon()
    
    # Build executable
    success = build_executable(icon_path)
    
    # Cleanup
    cleanup()
    
    print("\n" + "=" * 60)
    if success:
        print("Build completed successfully!")
        print("Executable location: dist/Client Treatment Organizer.exe")
        print("=" * 60)
        return 0
    else:
        print("Build failed!")
        print("=" * 60)
        return 1

if __name__ == "__main__":
    sys.exit(main())
