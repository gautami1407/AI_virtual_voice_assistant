"""
Asset Management Module
=======================
This module provides portable, cross-platform file path handling for all assets.
It centralizes asset loading and handles missing files gracefully.

Changes Made:
- Created to replace hardcoded absolute paths throughout the project
- All asset paths are now relative to the project root or this module
- Missing assets are handled with warnings and fallback placeholders
- Compatible with Windows, Linux, and macOS
"""

import os
from pathlib import Path
from typing import Optional

# Get the directory where this module is located (project root)
PROJECT_ROOT = Path(__file__).parent.resolve()
ASSETS_DIR = PROJECT_ROOT / "assets"


def get_asset_path(asset_name: str, use_assets_subfolder: bool = False) -> Path:
    """
    Get a portable path to an asset file.
    
    Args:
        asset_name: Name of the asset file (e.g., "bujji.gif", "icon.png")
        use_assets_subfolder: If True, look in assets/ subfolder; if False, look in project root
    
    Returns:
        Path object pointing to the asset location
    """
    if use_assets_subfolder:
        return ASSETS_DIR / asset_name
    return PROJECT_ROOT / asset_name


def asset_exists(asset_name: str, use_assets_subfolder: bool = False) -> bool:
    """
    Check if an asset file exists.
    
    Args:
        asset_name: Name of the asset file
        use_assets_subfolder: If True, look in assets/ subfolder
    
    Returns:
        True if the file exists, False otherwise
    """
    return get_asset_path(asset_name, use_assets_subfolder).exists()


def load_image_safely(
    asset_name: str, 
    use_assets_subfolder: bool = False,
    fallback_text: str = "Image not available"
) -> Optional[Path]:
    """
    Safely load an image path with existence checking.
    
    Args:
        asset_name: Name of the image file
        use_assets_subfolder: If True, look in assets/ subfolder
        fallback_text: Text to display in warning if asset missing
    
    Returns:
        Path to the image if it exists, None otherwise
    """
    asset_path = get_asset_path(asset_name, use_assets_subfolder)
    
    if not asset_path.exists():
        print(f"[WARNING] {fallback_text}: '{asset_path}' not found.")
        print(f"         Expected: {asset_name} in {ASSETS_DIR if use_assets_subfolder else PROJECT_ROOT}")
        return None
    
    return asset_path


def ensure_assets_directory() -> None:
    """
    Create the assets directory if it doesn't exist.
    This ensures the application can create missing directories gracefully.
    """
    if not ASSETS_DIR.exists():
        ASSETS_DIR.mkdir(parents=True, exist_ok=True)
        print(f"[INFO] Created assets directory: {ASSETS_DIR}")


def get_gif_path(gif_name: str) -> Path:
    """
    Get path to a GIF file (looks in project root first, then assets/).
    
    Args:
        gif_name: Name of the GIF file
    
    Returns:
        Path object pointing to the GIF location
    """
    if asset_exists(gif_name, use_assets_subfolder=False):
        return get_asset_path(gif_name, use_assets_subfolder=False)
    elif asset_exists(gif_name, use_assets_subfolder=True):
        return get_asset_path(gif_name, use_assets_subfolder=True)
    return get_asset_path(gif_name, use_assets_subfolder=False)


def get_image_path(image_name: str) -> Path:
    """
    Get path to an image file (looks in project root first, then assets/).
    
    Args:
        image_name: Name of the image file
    
    Returns:
        Path object pointing to the image location
    """
    if asset_exists(image_name, use_assets_subfolder=False):
        return get_asset_path(image_name, use_assets_subfolder=False)
    elif asset_exists(image_name, use_assets_subfolder=True):
        return get_asset_path(image_name, use_assets_subfolder=True)
    return get_asset_path(image_name, use_assets_subfolder=False)


def get_output_path(filename: str) -> Path:
    """
    Get a portable path for output files (screenshots, camera pictures, etc).
    Output files are saved in the project root directory.
    
    Args:
        filename: Name of the output file
    
    Returns:
        Path object pointing to the output file location
    """
    return PROJECT_ROOT / filename


if __name__ == "__main__":
    # Test the asset paths
    print(f"Project root: {PROJECT_ROOT}")
    print(f"Assets directory: {ASSETS_DIR}")
    print(f"bujji.gif exists: {asset_exists('bujji.gif')}")