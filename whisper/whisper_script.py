# pip install git+https://github.com/openai/whisper.git
# sudo apt update && sudo apt install ffmpeg
# whisper "output001.mp3" --device cuda --language vi --model large --output_format txt


#!/usr/bin/env python3
"""
MP3 to Whisper Transcription Pipeline
This script automatically splits MP3 files into chunks and generates transcriptions using Whisper.
"""

import os
import subprocess
import glob
import argparse
from pathlib import Path
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def run_command(command, description=""):
    """Run a shell command and handle errors."""
    try:
        logger.info(f"Running: {description or command}")
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        logger.info(f"Successfully completed: {description or command}")
        return result
    except subprocess.CalledProcessError as e:
        logger.error(f"Error running command: {description or command}")
        logger.error(f"Error output: {e.stderr}")
        raise

def split_mp3(input_file, output_dir, segment_time="00:20:00"):
    """
    Split an MP3 file into chunks using ffmpeg.
    
    Args:
        input_file (str): Path to input MP3 file
        output_dir (str): Directory to save output chunks
        segment_time (str): Duration of each chunk (HH:MM:SS format)
    
    Returns:
        list: List of generated chunk filenames
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate output pattern
    output_pattern = os.path.join(output_dir, "output%03d.mp3")
    
    # Build ffmpeg command
    command = f'ffmpeg -i "{input_file}" -c copy -map 0 -segment_time {segment_time} -f segment "{output_pattern}"'
    
    logger.info(f"Splitting {input_file} into {segment_time} chunks...")
    run_command(command, f"ffmpeg split for {input_file}")
    
    # Get list of generated chunks
    chunk_files = sorted(glob.glob(os.path.join(output_dir, "output*.mp3")))
    logger.info(f"Generated {len(chunk_files)} chunks")
    
    return chunk_files

def transcribe_chunk(chunk_file, output_dir, language="vi", model="large", device="cuda"):
    """
    Generate Whisper transcription for a single MP3 chunk.
    
    Args:
        chunk_file (str): Path to MP3 chunk file
        output_dir (str): Directory to save transcription
        language (str): Language code for transcription
        model (str): Whisper model size
        device (str): Device to use (cuda/cpu)
    
    Returns:
        str: Path to generated transcription file
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate output filename
    chunk_name = Path(chunk_file).stem
    output_file = os.path.join(output_dir, f"{chunk_name}.txt")
    
    # Build whisper command
    command = f'whisper "{chunk_file}" --device {device} --language {language} --model {model} --output_format txt --output_dir "{output_dir}"'
    
    logger.info(f"Transcribing {chunk_file}...")
    run_command(command, f"Whisper transcription for {chunk_file}")
    
    return output_file

def process_folder(input_folder, output_base_dir, segment_time="00:20:00", language="vi", model="large", device="cuda"):
    """
    Process all MP3 files in a folder: split into chunks and transcribe each chunk.
    
    Args:
        input_folder (str): Folder containing MP3 files to process
        output_base_dir (str): Base directory for outputs
        segment_time (str): Duration of each chunk
        language (str): Language code for transcription
        model (str): Whisper model size
        device (str): Device to use
    """
    # Find all MP3 files in the input folder
    mp3_files = glob.glob(os.path.join(input_folder, "*.mp3"))
    
    if not mp3_files:
        logger.warning(f"No MP3 files found in {input_folder}")
        return
    
    logger.info(f"Found {len(mp3_files)} MP3 files to process")
    
    for mp3_file in mp3_files:
        mp3_name = Path(mp3_file).stem
        
        # Create output directories
        chunks_dir = os.path.join(output_base_dir, mp3_name, "chunks")
        transcriptions_dir = os.path.join(output_base_dir, mp3_name, "transcriptions")
        
        logger.info(f"Processing {mp3_name}...")
        
        try:
            # Step 1: Split MP3 into chunks
            chunk_files = split_mp3(mp3_file, chunks_dir, segment_time)
            
            # Step 2: Transcribe each chunk
            for chunk_file in chunk_files:
                transcribe_chunk(chunk_file, transcriptions_dir, language, model, device)
            
            logger.info(f"Successfully processed {mp3_name}")
            
        except Exception as e:
            logger.error(f"Error processing {mp3_name}: {str(e)}")
            continue

def main():
    """Main function with command line argument parsing."""
    parser = argparse.ArgumentParser(description="MP3 to Whisper Transcription Pipeline")
    parser.add_argument("input_folder", help="Folder containing MP3 files to process")
    parser.add_argument("--output-dir", default="output", help="Base output directory (default: output)")
    parser.add_argument("--segment-time", default="00:20:00", help="Duration of each chunk (default: 00:20:00)")
    parser.add_argument("--language", default="vi", help="Language code for transcription (default: vi)")
    parser.add_argument("--model", default="large", help="Whisper model size (default: large)")
    parser.add_argument("--device", default="cuda", help="Device to use (default: cuda)")
    
    args = parser.parse_args()
    
    # Check if input folder exists
    if not os.path.exists(args.input_folder):
        logger.error(f"Input folder does not exist: {args.input_folder}")
        return
    
    # Check if required tools are available
    try:
        run_command("ffmpeg -version", "ffmpeg version check")
    except Exception:
        logger.error("ffmpeg is not available. Please install ffmpeg first.")
        return
    
    try:
        run_command("whisper --help", "whisper version check")
    except Exception:
        logger.error("whisper is not available. Please install whisper first.")
        return
    
    # Process the folder
    process_folder(
        args.input_folder,
        args.output_dir,
        args.segment_time,
        args.language,
        args.model,
        args.device
    )
    
    logger.info("Processing completed!")

if __name__ == "__main__":
    main()