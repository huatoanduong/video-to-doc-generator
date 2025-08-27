# Slide Change Detection for Lecture Videos

This Python script detects PowerPoint slide changes in lecture video recordings using OpenCV. It's designed to work alongside the existing transcription pipeline to create comprehensive study materials.

## Features

- **Hybrid Detection**: Combines SSIM, histogram comparison, and template matching
- **Multiple Sensitivity Levels**: High, balanced, and low sensitivity options
- **Batch Processing**: Memory-efficient processing for long videos (3+ hours)
- **Comprehensive Output**: JSON format with timestamps, slide numbers, and descriptions
- **Progress Tracking**: Real-time progress updates and detailed logging
- **Flexible Configuration**: Customizable thresholds and parameters

## Installation

### 1. Install Dependencies

```bash
# Install OpenCV and other required packages
pip install -r requirements_slide_detection.txt

# Or install manually
pip install opencv-python numpy scikit-image
```

### 2. Verify Installation

```bash
# Test all dependencies and functionality
python test_installation.py

# Or test OpenCV specifically
python -c "import cv2; print(f'OpenCV version: {cv2.__version__}')"
```

## Usage

### Available Scripts

The slide detection system includes several scripts for different purposes:

- **`slide_detector.py`** - Main script for detecting slide changes in videos
- **`test_installation.py`** - Test script to verify all dependencies are working
- **`example_usage.py`** - Examples of how to use the detector programmatically
- **`requirements_slide_detection.txt`** - Dependencies file for the slide detection feature

### Command Line Interface

#### Basic Usage
```bash
# Process video with default balanced sensitivity
python slide_detector.py "your_lecture_video.mp4"
```

#### Advanced Options
```bash
# High sensitivity detection (catches all changes)
python slide_detector.py "lecture.mp4" --sensitivity high

# Low sensitivity (major transitions only)
python slide_detector.py "lecture.mp4" --sensitivity low

# Custom output file
python slide_detector.py "lecture.mp4" --output "my_slides.json"

# Custom thresholds
python slide_detector.py "lecture.mp4" \
    --ssim-threshold 0.80 \
    --histogram-threshold 0.25 \
    --frame-interval 3

# Verbose logging
python slide_detector.py "lecture.mp4" --verbose
```

### Programmatic Usage

```python
from slide_detector import SlideChangeDetector

# Initialize detector
detector = SlideChangeDetector(sensitivity="balanced")

# Process video
slide_changes = detector.process_video(
    "lecture.mp4", 
    "output.json"
)

# Print summary
detector.print_summary()

# Access results
for change in slide_changes:
    print(f"Slide {change['slide_number']} at {change['timestamp']}")
```

### Testing and Examples

#### Test Installation
```bash
# Run comprehensive dependency test
python test_installation.py
```

#### Run Examples
```bash
# See programmatic usage examples
python example_usage.py
```

#### Quick Start Test
```bash
# Test with a small video first
python slide_detector.py "test_video.mp4" --sensitivity high --verbose
```

## Output Format

The script generates a JSON file with the following structure:

```json
{
  "detection_info": {
    "sensitivity": "balanced",
    "ssim_threshold": 0.85,
    "histogram_threshold": 0.15,
    "frame_interval": 5,
    "detection_date": "2025-01-27T10:30:00"
  },
  "slide_changes": [
    {
      "timestamp": "00:00:00",
      "timestamp_seconds": 0.0,
      "frame_number": 0,
      "slide_number": 1,
      "description": "Slide 1"
    },
    {
      "timestamp": "00:05:30",
      "timestamp_seconds": 330.0,
      "frame_number": 9900,
      "slide_number": 2,
      "description": "Slide 2"
    }
  ],
  "summary": {
    "total_slides": 2,
    "total_duration": "00:05:30"
  }
}
```

## Detection Sensitivity Options

### 1. High Granularity (1-2 seconds)
- **Use Case**: When you need to track every minor content update
- **Performance**: ~2-3x slower, higher memory usage
- **Accuracy**: Very high, catches all changes
- **Command**: `--sensitivity high`

### 2. Balanced (5-10 seconds) - **Recommended**
- **Use Case**: Good balance for most lecture videos
- **Performance**: ~1.5x slower than major transitions
- **Accuracy**: High, catches most changes
- **Command**: `--sensitivity balanced` (default)

### 3. Major Transitions Only
- **Use Case**: When you only care about new slides
- **Performance**: Fastest, lowest memory usage
- **Accuracy**: Good for main slides, might miss content updates
- **Command**: `--sensitivity low`

## Technical Details

### Detection Methods

1. **Primary**: Structural Similarity Index (SSIM)
   - Analyzes structural patterns and textures
   - More accurate than histogram comparison
   - Handles lighting changes well

2. **Secondary**: Histogram Comparison
   - Compares color distribution between frames
   - Fast and efficient
   - Good fallback method

3. **Future**: Template Matching
   - Will use exported JPG slides as reference
   - Most accurate for known content
   - Requires slide export (planned feature)

### Processing Strategy

- **Batch Processing**: Memory-efficient for long videos
- **Frame Skipping**: Configurable interval between comparisons
- **Progress Tracking**: Real-time updates and logging
- **Error Handling**: Graceful fallbacks and detailed error messages

## Performance Tips

### For Long Videos (3+ hours)
- Use `--sensitivity balanced` for good performance/accuracy balance
- Monitor memory usage during processing
- Consider using `--frame-interval 10` for faster processing

### For High-Quality Videos (FullHD+)
- SSIM works well with high-resolution content
- Histogram comparison handles color variations
- Adjust thresholds based on video quality

### Memory Optimization
- Batch processing automatically manages memory
- Frame interval controls processing frequency
- Lower sensitivity uses less memory

## Troubleshooting

### Common Issues

1. **OpenCV Import Error**
   ```bash
   pip uninstall opencv-python
   pip install opencv-python-headless
   ```

2. **Memory Issues on Long Videos**
   ```bash
   # Use lower sensitivity
   python slide_detector.py "video.mp4" --sensitivity low
   
   # Increase frame interval
   python slide_detector.py "video.mp4" --frame-interval 10
   ```

3. **False Positives/Negatives**
   ```bash
   # Adjust SSIM threshold
   python slide_detector.py "video.mp4" --ssim-threshold 0.90
   
   # Adjust histogram threshold
   python slide_detector.py "video.mp4" --histogram-threshold 0.10
   ```

4. **Slow Processing**
   ```bash
   # Use lower sensitivity
   python slide_detector.py "video.mp4" --sensitivity low
   
   # Increase frame interval
   python slide_detector.py "video.mp4" --frame-interval 15
   ```

5. **Script Import Errors**
   ```bash
   # Test all dependencies first
   python test_installation.py
   
   # Check Python path and working directory
   python -c "import sys; print(sys.path)"
   ```

### Debug Mode

Enable verbose logging for detailed analysis:

```bash
python slide_detector.py "video.mp4" --verbose
```

This will create a `slide_detection.log` file with detailed processing information.

## Project Structure

```
video-to-doc-generator/
├── slide_detector.py              # Main slide detection script
├── test_installation.py           # Dependency testing script
├── example_usage.py               # Usage examples
├── requirements_slide_detection.txt # Slide detection dependencies
├── SLIDE_DETECTION_README.md      # This documentation file
├── whisper/                       # Existing transcription pipeline
│   └── whisper_script.py
└── README.md                      # Main project documentation
```

## Integration with Transcription Pipeline

The slide detection output can be combined with your existing Whisper transcription:

1. **Run slide detection first**:
   ```bash
   python slide_detector.py "lecture.mp4"
   ```

2. **Run transcription**:
   ```bash
   python whisper/whisper_script.py "audio_folder"
   ```

3. **Combine results** (future feature):
   - Match slide timestamps with transcription timestamps
   - Create synchronized study materials
   - Generate markdown with slide references

## Future Enhancements

- [ ] Template matching with exported PowerPoint slides
- [ ] Real-time processing mode
- [ ] Integration with transcription pipeline
- [ ] Web interface for configuration
- [ ] Support for multiple video formats
- [ ] Machine learning-based detection improvements

## Examples

### Example 1: Basic Detection
```bash
python slide_detector.py "M03W02 - K Nearest Neighbor (KNN).mp4"
```

### Example 2: High Accuracy
```bash
python slide_detector.py "lecture.mp4" \
    --sensitivity high \
    --output "detailed_slides.json" \
    --verbose
```

### Example 3: Fast Processing
```bash
python slide_detector.py "long_lecture.mp4" \
    --sensitivity low \
    --frame-interval 15 \
    --output "quick_slides.json"
```

## Quick Reference

### Essential Commands
```bash
# Test everything works
python test_installation.py

# Basic slide detection
python slide_detector.py "video.mp4"

# High accuracy detection
python slide_detector.py "video.mp4" --sensitivity high --verbose

# Fast processing for long videos
python slide_detector.py "video.mp4" --sensitivity low --frame-interval 10

# See examples
python example_usage.py
```

### File Outputs
- **JSON**: `{video_name}_slide_changes.json` - Main results
- **Log**: `slide_detection.log` - Detailed processing log
- **Console**: Real-time progress and summary

## Support

For issues and questions:
1. Check the troubleshooting section above
2. Enable verbose logging with `--verbose`
3. Review the `slide_detection.log` file
4. Check OpenCV and dependency versions
5. Run `python test_installation.py` to verify setup

## License

This script is provided as-is for educational and personal use.
