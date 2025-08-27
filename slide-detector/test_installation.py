#!/usr/bin/env python3
"""
Test script to verify slide detection dependencies are properly installed.
Run this script to check if all required packages are available.
"""


def test_imports():
    """Test if all required packages can be imported."""
    print("Testing package imports...")

    try:
        import cv2
        print(f"✓ OpenCV version: {cv2.__version__}")
    except ImportError as e:
        print(f"✗ OpenCV import failed: {e}")
        return False

    try:
        import numpy as np
        print(f"✓ NumPy version: {np.__version__}")
    except ImportError as e:
        print(f"✗ NumPy import failed: {e}")
        return False

    try:
        import json
        print("✓ JSON module available")
    except ImportError as e:
        print(f"✗ JSON import failed: {e}")
        return False

    try:
        import argparse
        print("✓ Argparse module available")
    except ImportError as e:
        print(f"✗ Argparse import failed: {e}")
        return False

    try:
        import logging
        print("✓ Logging module available")
    except ImportError as e:
        print(f"✗ Logging import failed: {e}")
        return False

    try:
        from pathlib import Path
        print("✓ Pathlib module available")
    except ImportError as e:
        print(f"✗ Pathlib import failed: {e}")
        return False

    try:
        from datetime import datetime
        print("✓ Datetime module available")
    except ImportError as e:
        print(f"✗ Datetime import failed: {e}")
        return False

    return True


def test_opencv_functionality():
    """Test basic OpenCV functionality."""
    print("\nTesting OpenCV functionality...")

    try:
        import cv2
        import numpy as np

        # Test basic image operations
        test_image = np.zeros((100, 100, 3), dtype=np.uint8)
        test_image[50, 50] = [255, 255, 255]  # White pixel

        # Test color conversion
        gray = cv2.cvtColor(test_image, cv2.COLOR_BGR2GRAY)
        print("✓ Basic image operations work")

        # Test histogram calculation
        hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
        print("✓ Histogram calculation works")

        # Test image comparison
        similarity = cv2.compareHist(hist, hist, cv2.HISTCMP_CORREL)
        print(
            f"✓ Histogram comparison works (self-similarity: {similarity:.3f})")

        return True

    except Exception as e:
        print(f"✗ OpenCV functionality test failed: {e}")
        return False


def test_slide_detector_import():
    """Test if the slide detector can be imported."""
    print("\nTesting slide detector import...")

    try:
        from slide_detector import SlideChangeDetector
        print("✓ SlideChangeDetector class imported successfully")

        # Test instantiation
        detector = SlideChangeDetector()
        print("✓ SlideChangeDetector instance created successfully")

        return True

    except Exception as e:
        print(f"✗ Slide detector import failed: {e}")
        return False


def main():
    """Run all tests."""
    print("=" * 50)
    print("SLIDE DETECTION DEPENDENCY TEST")
    print("=" * 50)

    all_tests_passed = True

    # Test 1: Package imports
    if not test_imports():
        all_tests_passed = False

    # Test 2: OpenCV functionality
    if not test_opencv_functionality():
        all_tests_passed = False

    # Test 3: Slide detector import
    if not test_slide_detector_import():
        all_tests_passed = False

    # Summary
    print("\n" + "=" * 50)
    if all_tests_passed:
        print("🎉 ALL TESTS PASSED! Your system is ready for slide detection.")
        print("\nYou can now run:")
        print("  python slide_detector.py --help")
        print("  python example_usage.py")
    else:
        print("❌ SOME TESTS FAILED. Please check the errors above.")
        print("\nCommon solutions:")
        print(
            "  1. Install missing packages: pip install -r requirements_slide_detection.txt")
        print("  2. Check Python version compatibility")
        print("  3. Verify OpenCV installation")
    print("=" * 50)


if __name__ == "__main__":
    main()
