"""
Client Treatment Organizer - Main Application Entry Point

This is a placeholder for the main application.
The full GUI implementation will be added in subsequent releases.
"""

import sys
from pathlib import Path

def main():
    """Main application entry point"""
    print("=" * 60)
    print("Client Treatment Organizer v0.0.1")
    print("=" * 60)
    print("\nWelcome to Client Treatment Organizer!")
    print("\nThis is the initial release of the application.")
    print("Core functionality is currently in development.")
    print("\nFeatures coming soon:")
    print("  • File manager integration")
    print("  • Client folder scanning")
    print("  • Metadata management")
    print("  • Windows context menu integration")
    print("  • Real-time file watching")
    print("  • Treatment timeline visualization")
    print("\nFor more information, visit:")
    print("https://github.com/DrDisc/Client_treatment_Organizer")
    print("\n" + "=" * 60)
    
    # Try to import tkinter for GUI
    try:
        import tkinter as tk
        from tkinter import messagebox
        
        # Create a simple welcome window
        root = tk.Tk()
        root.title("Client Treatment Organizer v0.0.1")
        root.geometry("400x300")
        
        # Center window on screen
        root.update_idletasks()
        width = root.winfo_width()
        height = root.winfo_height()
        x = (root.winfo_screenwidth() // 2) - (width // 2)
        y = (root.winfo_screenheight() // 2) - (height // 2)
        root.geometry(f'{width}x{height}+{x}+{y}')
        
        # Create welcome label
        tk.Label(
            root,
            text="Client Treatment Organizer",
            font=("Arial", 16, "bold"),
            pady=10
        ).pack()
        
        tk.Label(
            root,
            text="v0.0.1 - Initial Release",
            font=("Arial", 10),
            fg="gray"
        ).pack()
        
        tk.Label(
            root,
            text="\nCore functionality is in development.\n\nCheck back soon for:",
            font=("Arial", 10)
        ).pack()
        
        features_text = """
• File manager integration
• Client organization tools
• Metadata management
• Automated file tracking
        """
        
        tk.Label(
            root,
            text=features_text,
            font=("Arial", 9),
            justify="left"
        ).pack(pady=10)
        
        tk.Button(
            root,
            text="Visit Repository",
            command=lambda: open_url("https://github.com/DrDisc/Client_treatment_Organizer")
        ).pack(pady=10)
        
        tk.Button(
            root,
            text="Exit",
            command=root.quit
        ).pack()
        
        root.mainloop()
    
    except ImportError:
        print("\nNote: Tkinter not available. Running in console mode.")
        print("Press Enter to exit...")
        input()

def open_url(url):
    """Open URL in default browser"""
    import webbrowser
    webbrowser.open(url)

if __name__ == "__main__":
    main()
