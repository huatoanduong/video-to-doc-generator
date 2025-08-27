#!/usr/bin/env python3
"""
Example usage of the Slide Change Detector

This script demonstrates how to use the SlideChangeDetector class
programmatically in your own Python code.
"""

from slide_detector import SlideChangeDetector
import json

def main():
    # Example 1: Basic usage with default settings
    print("=== Example 1: Basic Usage ===")
    
    detector = SlideChangeDetector()
    
    # Process a video file
    try:
        slide_changes = detector.process_video(
            "M03W02 - K Nearest Neighbor (KNN).mp4",
            "basic_slide_changes.json"
        )
        
        print(f"Detected {len(slide_changes)} slide changes")
        
        # Print first few changes
        for change in slide_changes[:3]:
            print(f"  {change['timestamp']} - {change['description']}")
            
    except FileNotFoundError:
        print("Video file not found. Please update the path to your video file.")
    
    print("\n" + "="*50 + "\n")
    
    # Example 2: High sensitivity detection
    print("=== Example 2: High Sensitivity Detection ===")
    
    high_sensitivity_detector = SlideChangeDetector(
        sensitivity="high",
        ssim_threshold=0.90,
        histogram_threshold=0.10
    )
    
    print(f"High sensitivity detector initialized with:")
    print(f"  SSIM threshold: {high_sensitivity_detector.ssim_threshold}")
    print(f"  Histogram threshold: {high_sensitivity_detector.histogram_threshold}")
    print(f"  Frame interval: {high_sensitivity_detector.frame_interval}")
    
    print("\n" + "="*50 + "\n")
    
    # Example 3: Custom thresholds
    print("=== Example 3: Custom Thresholds ===")
    
    custom_detector = SlideChangeDetector(
        sensitivity="balanced",
        ssim_threshold=0.80,      # More lenient SSIM
        histogram_threshold=0.25,  # More lenient histogram
        frame_interval=3           # Process more frames
    )
    
    print(f"Custom detector initialized with:")
    print(f"  SSIM threshold: {custom_detector.ssim_threshold}")
    print(f"  Histogram threshold: {custom_detector.histogram_threshold}")
    print(f"  Frame interval: {custom_detector.frame_interval}")
    
    print("\n" + "="*50 + "\n")
    
    # Example 4: Working with results
    print("=== Example 4: Working with Results ===")
    
    # Simulate some detected slide changes
    sample_changes = [
        {
            "timestamp": "00:00:00",
            "timestamp_seconds": 0.0,
            "frame_number": 0,
            "slide_number": 1,
            "description": "Slide 1 (Introduction)"
        },
        {
            "timestamp": "00:05:30",
            "timestamp_seconds": 330.0,
            "frame_number": 9900,
            "slide_number": 2,
            "description": "Slide 2 (KNN Overview)"
        },
        {
            "timestamp": "00:12:45",
            "timestamp_seconds": 765.0,
            "frame_number": 22950,
            "slide_number": 3,
            "description": "Slide 3 (Algorithm Steps)"
        }
    ]
    
    # Create a detector instance and set the results
    example_detector = SlideChangeDetector()
    example_detector.slide_changes = sample_changes
    
    # Print summary
    example_detector.print_summary()
    
    # Save to JSON
    example_detector.save_results("example_slide_changes.json")
    print(f"\nExample results saved to: example_slide_changes.json")
    
    # Load and display the saved JSON
    with open("example_slide_changes.json", 'r') as f:
        loaded_data = json.load(f)
    
    print(f"\nLoaded data summary:")
    print(f"  Total slides: {loaded_data['summary']['total_slides']}")
    print(f"  Detection sensitivity: {loaded_data['detection_info']['sensitivity']}")
    print(f"  Detection date: {loaded_data['detection_info']['detection_date']}")

if __name__ == "__main__":
    main()
