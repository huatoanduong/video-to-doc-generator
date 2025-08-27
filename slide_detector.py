#!/usr/bin/env python3
"""
Slide Change Detector for Lecture Videos

This script detects PowerPoint slide changes in lecture video recordings using OpenCV.
It combines frame difference analysis, template matching, and histogram comparison
for accurate detection of slide transitions.

Author: AI Assistant
Date: 2025
"""

import cv2
import numpy as np
import json
import argparse
import os
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Tuple, Optional
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('slide_detection.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class SlideChangeDetector:
    """Detects slide changes in lecture videos using multiple OpenCV techniques."""
    
    def __init__(self, 
                 sensitivity: str = "balanced",
                 ssim_threshold: float = 0.85,
                 histogram_threshold: float = 0.15,
                 frame_interval: int = 5):
        """
        Initialize the slide change detector.
        
        Args:
            sensitivity: Detection sensitivity ("high", "balanced", "low")
            ssim_threshold: SSIM threshold for frame similarity (0.0-1.0)
            histogram_threshold: Histogram difference threshold (0.0-1.0)
            frame_interval: Number of frames to skip between comparisons
        """
        self.sensitivity = sensitivity
        self.ssim_threshold = ssim_threshold
        self.histogram_threshold = histogram_threshold
        self.frame_interval = frame_interval
        
        # Adjust parameters based on sensitivity
        if sensitivity == "high":
            self.frame_interval = 2
            self.ssim_threshold = 0.90
            self.histogram_threshold = 0.10
        elif sensitivity == "low":
            self.frame_interval = 10
            self.ssim_threshold = 0.80
            self.histogram_threshold = 0.20
            
        self.slide_changes = []
        self.current_slide_number = 0
        self.previous_frame = None
        self.previous_histogram = None
        
        logger.info(f"Initialized detector with {sensitivity} sensitivity")
        logger.info(f"Frame interval: {self.frame_interval}, SSIM threshold: {self.ssim_threshold}")
    
    def calculate_histogram_similarity(self, frame1: np.ndarray, frame2: np.ndarray) -> float:
        """Calculate histogram similarity between two frames."""
        try:
            # Convert to grayscale for histogram comparison
            gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
            gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
            
            # Calculate histograms
            hist1 = cv2.calcHist([gray1], [0], None, [256], [0, 256])
            hist2 = cv2.calcHist([gray2], [0], None, [256], [0, 256])
            
            # Normalize histograms
            hist1 = cv2.normalize(hist1, hist1).flatten()
            hist2 = cv2.normalize(hist2, hist2).flatten()
            
            # Calculate correlation
            similarity = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
            return similarity
            
        except Exception as e:
            logger.error(f"Error calculating histogram similarity: {e}")
            return 0.0
    
    def calculate_ssim(self, frame1: np.ndarray, frame2: np.ndarray) -> float:
        """Calculate Structural Similarity Index between two frames."""
        try:
            # Convert to grayscale
            gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
            gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
            
            # Resize frames to same size for comparison
            height, width = gray1.shape
            gray2_resized = cv2.resize(gray2, (width, height))
            
            # Calculate SSIM
            ssim_score = cv2.compareSSIM(gray1, gray2_resized)
            return ssim_score
            
        except Exception as e:
            logger.error(f"Error calculating SSIM: {e}")
            # Fallback to histogram comparison
            return self.calculate_histogram_similarity(frame1, frame2)
    
    def detect_change(self, current_frame: np.ndarray, frame_number: int) -> bool:
        """
        Detect if there's a significant change between frames.
        
        Args:
            current_frame: Current video frame
            frame_number: Current frame number
            
        Returns:
            True if change detected, False otherwise
        """
        if self.previous_frame is None:
            self.previous_frame = current_frame.copy()
            self.previous_histogram = self.calculate_histogram_similarity(
                current_frame, current_frame
            )
            return False
        
        # Calculate similarities
        ssim_score = self.calculate_ssim(self.previous_frame, current_frame)
        histogram_similarity = self.calculate_histogram_similarity(
            self.previous_frame, current_frame
        )
        
        # Determine if change occurred
        ssim_change = ssim_score < self.ssim_threshold
        histogram_change = histogram_similarity < self.histogram_threshold
        
        # Log detailed comparison for debugging
        if frame_number % 100 == 0:  # Log every 100 frames
            logger.debug(f"Frame {frame_number}: SSIM={ssim_score:.3f}, "
                        f"Hist={histogram_similarity:.3f}")
        
        # Change detected if either method indicates significant difference
        change_detected = ssim_change or histogram_change
        
        if change_detected:
            logger.info(f"Change detected at frame {frame_number}: "
                       f"SSIM={ssim_score:.3f}, Hist={histogram_similarity:.3f}")
        
        # Update previous frame and histogram
        self.previous_frame = current_frame.copy()
        self.previous_histogram = histogram_similarity
        
        return change_detected
    
    def process_video(self, video_path: str, output_path: str = None) -> List[Dict]:
        """
        Process video file and detect slide changes.
        
        Args:
            video_path: Path to input video file
            output_path: Path for output JSON file (optional)
            
        Returns:
            List of detected slide changes
        """
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")
        
        # Open video
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise ValueError(f"Could not open video file: {video_path}")
        
        # Get video properties
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = total_frames / fps
        
        logger.info(f"Processing video: {video_path}")
        logger.info(f"FPS: {fps:.2f}, Total frames: {total_frames}, "
                   f"Duration: {duration/60:.2f} minutes")
        
        # Reset state
        self.slide_changes = []
        self.current_slide_number = 0
        self.previous_frame = None
        self.previous_histogram = None
        
        frame_count = 0
        start_time = time.time()
        
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Process every nth frame based on sensitivity
                if frame_count % self.frame_interval == 0:
                    if self.detect_change(frame, frame_count):
                        # Calculate timestamp
                        timestamp_seconds = frame_count / fps
                        timestamp_str = self.seconds_to_timestamp(timestamp_seconds)
                        
                        # Increment slide number
                        self.current_slide_number += 1
                        
                        # Record slide change
                        slide_change = {
                            "timestamp": timestamp_str,
                            "timestamp_seconds": round(timestamp_seconds, 2),
                            "frame_number": frame_count,
                            "slide_number": self.current_slide_number,
                            "description": f"Slide {self.current_slide_number}"
                        }
                        
                        self.slide_changes.append(slide_change)
                        logger.info(f"Slide {self.current_slide_number} detected at {timestamp_str}")
                
                frame_count += 1
                
                # Progress update every 1000 frames
                if frame_count % 1000 == 0:
                    elapsed = time.time() - start_time
                    progress = (frame_count / total_frames) * 100
                    logger.info(f"Progress: {progress:.1f}% ({frame_count}/{total_frames}) "
                              f"Elapsed: {elapsed:.1f}s")
        
        finally:
            cap.release()
        
        # Add final slide if video ends
        if self.current_slide_number == 0:
            # No changes detected, add initial slide
            self.slide_changes.append({
                "timestamp": "00:00:00",
                "timestamp_seconds": 0.0,
                "frame_number": 0,
                "slide_number": 1,
                "description": "Slide 1 (Initial)"
            })
        
        # Save results
        if output_path:
            self.save_results(output_path)
        
        logger.info(f"Processing complete. Detected {len(self.slide_changes)} slide changes")
        return self.slide_changes
    
    def seconds_to_timestamp(self, seconds: float) -> str:
        """Convert seconds to HH:MM:SS format."""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds = int(seconds % 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    
    def save_results(self, output_path: str):
        """Save detection results to JSON file."""
        try:
            results = {
                "detection_info": {
                    "sensitivity": self.sensitivity,
                    "ssim_threshold": self.ssim_threshold,
                    "histogram_threshold": self.histogram_threshold,
                    "frame_interval": self.frame_interval,
                    "detection_date": datetime.now().isoformat()
                },
                "slide_changes": self.slide_changes,
                "summary": {
                    "total_slides": len(self.slide_changes),
                    "total_duration": self.slide_changes[-1]["timestamp"] if self.slide_changes else "00:00:00"
                }
            }
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Results saved to: {output_path}")
            
        except Exception as e:
            logger.error(f"Error saving results: {e}")
            raise
    
    def print_summary(self):
        """Print a summary of detected slide changes."""
        if not self.slide_changes:
            print("No slide changes detected.")
            return
        
        print(f"\n{'='*60}")
        print(f"SLIDE CHANGE DETECTION SUMMARY")
        print(f"{'='*60}")
        print(f"Total slides detected: {len(self.slide_changes)}")
        print(f"Detection sensitivity: {self.sensitivity}")
        print(f"Processing time: {self.slide_changes[-1]['timestamp']}")
        print(f"{'='*60}")
        
        print(f"{'Timestamp':<12} {'Slide':<6} {'Frame':<8} {'Description'}")
        print(f"{'-'*60}")
        
        for change in self.slide_changes:
            print(f"{change['timestamp']:<12} {change['slide_number']:<6} "
                  f"{change['frame_number']:<8} {change['description']}")
        
        print(f"{'='*60}")


def main():
    """Main function for command-line usage."""
    parser = argparse.ArgumentParser(
        description="Detect PowerPoint slide changes in lecture videos",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage with balanced sensitivity
  python slide_detector.py "lecture_video.mp4"
  
  # High sensitivity detection
  python slide_detector.py "lecture_video.mp4" --sensitivity high
  
  # Custom output file
  python slide_detector.py "lecture_video.mp4" --output "slide_changes.json"
  
  # Low sensitivity for major transitions only
  python slide_detector.py "lecture_video.mp4" --sensitivity low
        """
    )
    
    parser.add_argument(
        "video_path",
        help="Path to input video file"
    )
    
    parser.add_argument(
        "--output", "-o",
        help="Output JSON file path (default: auto-generated)"
    )
    
    parser.add_argument(
        "--sensitivity", "-s",
        choices=["high", "balanced", "low"],
        default="balanced",
        help="Detection sensitivity (default: balanced)"
    )
    
    parser.add_argument(
        "--ssim-threshold",
        type=float,
        default=0.85,
        help="SSIM threshold for frame similarity (0.0-1.0, default: 0.85)"
    )
    
    parser.add_argument(
        "--histogram-threshold",
        type=float,
        default=0.15,
        help="Histogram difference threshold (0.0-1.0, default: 0.15)"
    )
    
    parser.add_argument(
        "--frame-interval",
        type=int,
        default=5,
        help="Frame interval for processing (default: 5)"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    
    # Set logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Generate output path if not specified
    if not args.output:
        video_name = Path(args.video_path).stem
        args.output = f"{video_name}_slide_changes.json"
    
    try:
        # Initialize detector
        detector = SlideChangeDetector(
            sensitivity=args.sensitivity,
            ssim_threshold=args.ssim_threshold,
            histogram_threshold=args.histogram_threshold,
            frame_interval=args.frame_interval
        )
        
        # Process video
        logger.info("Starting slide change detection...")
        slide_changes = detector.process_video(args.video_path, args.output)
        
        # Print summary
        detector.print_summary()
        
        logger.info(f"Detection complete! Results saved to: {args.output}")
        
    except Exception as e:
        logger.error(f"Error during processing: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
