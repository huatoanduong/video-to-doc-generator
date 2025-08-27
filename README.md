# MP3 to Whisper Transcription Pipeline

This Python script automatically processes MP3 files by:
1. Splitting long MP3 files into manageable chunks (default: 20 minutes)
2. Generating Whisper transcriptions for each chunk
3. Organizing outputs in a structured directory format

## Prerequisites

Before running the script, you need to install:

### 1. FFmpeg
- **Windows**: Download from [ffmpeg.org](https://ffmpeg.org/download.html) or install via chocolatey: `choco install ffmpeg`
- **macOS**: `brew install ffmpeg`
- **Linux**: `sudo apt install ffmpeg` (Ubuntu/Debian) or `sudo yum install ffmpeg` (CentOS/RHEL)

### 2. Whisper
```bash
pip install git+https://github.com/openai/whisper.git
```

### 3. Python Dependencies
```bash
pip install -r requirements.txt
```

## Usage

### Convert mp4 to mp3
```
ffmpeg -i filename.mp4 filename.mp3
```

### Split a mp3 file into chunks
```
ffmpeg -i "path/to/mp3" -c copy -map 0 -segment_time 00:10:00 -f segment output%03d.mp3
```

### Basic Usage
```bash
python whisper/whisper_script.py "path/to/mp3/folder"
```

### Advanced Usage with Custom Parameters
```bash
python whisper/whisper_script.py "path/to/mp3/folder" \
    --output-dir "custom_output" \
    --segment-time "00:15:00" \
    --language "vi" \
    --model "large" \
    --device "cpu"
    --word_timestamps True 
```

### Parameters

- `input_folder`: **Required**. Path to folder containing MP3 files
- `--output-dir`: Output directory (default: "output")
- `--segment-time`: Duration of each chunk in HH:MM:SS format (default: "00:20:00")
- `--language`: Language code for transcription (default: "vi" for Vietnamese)
- `--model`: Whisper model size: tiny, base, small, medium, large (default: "large")
- `--device`: Device to use: cuda, cpu (default: "cuda")

## Output Structure

The script creates the following directory structure:

```
output/
├── M03W02 - K Nearest Neighbor (KNN)/
│   ├── chunks/
│   │   ├── output000.mp3
│   │   ├── output001.mp3
│   │   └── ...
│   └── transcriptions/
│       ├── output000.txt
│       ├── output001.txt
│       └── ...
└── Another_MP3_File/
    ├── chunks/
    └── transcriptions/
```

## Examples

### Process a folder with Vietnamese audio files
```bash
python whisper/whisper_script.py "localignore"
```

### Process with English language and 15-minute chunks
```bash
python whisper/whisper_script.py "localignore" \
    --language "en" \
    --segment-time "00:15:00"
```

### Use CPU instead of GPU (useful if CUDA is not available)
```bash
python whisper/whisper_script.py "localignore" \
    --device "cpu"
```

## Features

- **Automatic folder processing**: Loops through all MP3 files in a folder
- **Error handling**: Continues processing other files if one fails
- **Logging**: Detailed progress and error logging
- **Flexible chunking**: Configurable segment duration
- **Organized output**: Separate directories for chunks and transcriptions
- **Command-line interface**: Easy to use with various options
- **Slide change detection**: Detect PowerPoint slide changes in video recordings (planned feature)

## Troubleshooting

### Common Issues

1. **FFmpeg not found**: Install FFmpeg and ensure it's in your system PATH
2. **Whisper not found**: Install Whisper using the pip command above
3. **CUDA errors**: Use `--device cpu` if you don't have a compatible GPU
4. **Memory issues**: Use smaller models (tiny, base, small) for large files

### Performance Tips

- Use GPU (`--device cuda`) for faster transcription
- Use smaller models for faster processing (trade-off with accuracy)
- Process files in smaller batches if memory is limited

## Slide Change Detection (Planned Feature)

### Overview
A Python script using OpenCV to detect PowerPoint slide changes in lecture video recordings. This feature will work alongside the existing transcription pipeline to create comprehensive study materials.

### Technical Approach
- **Primary Detection**: Frame difference analysis using Structural Similarity Index (SSIM)
- **Secondary Validation**: Template matching with exported JPG slides (when available)
- **Fallback Method**: Histogram comparison for quick filtering
- **Processing Strategy**: Batch processing for memory efficiency on long videos

### Detection Sensitivity Options
1. **High Granularity** (1-2 seconds): Catches all changes, slower processing
2. **Balanced** (5-10 seconds): Good balance of speed and accuracy
3. **Major Transitions Only**: Fastest, detects only new slides

### Output Format
JSON file containing:
- Timestamp in HH:MM:SS format
- Sequential slide number
- Simple change description (e.g., "Slide 1", "Slide 2")

### Use Cases
- Long lecture videos (3+ hours)
- PowerPoint-based presentations
- Creating study materials with synchronized content
- Combining slide changes with transcription timestamps

### Implementation Notes
- Requires OpenCV and additional dependencies
- Supports FullHD video input
- Optimized for image-heavy slides
- Template matching requires JPG export of PowerPoint slides

## License

This script is provided as-is for educational and personal use.