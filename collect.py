#!/usr/bin/env python3
"""
Topic-Based Markdown Collector with Auto-Split
Collects markdown files organized by topic directories and creates split files for each topic.
"""

import os
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Tuple, Dict
from collections import defaultdict


def find_markdown_files(directory: Path) -> List[Path]:
    """
    Recursively find all markdown files in the given directory.
    
    Args:
        directory: Path to the directory to search
        
    Returns:
        List of Path objects for all markdown files found
    """
    markdown_extensions = {'.md', '.markdown', '.mkd', '.mdown'}
    markdown_files = []
    
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = Path(root) / file
            if file_path.suffix.lower() in markdown_extensions:
                markdown_files.append(file_path)
    
    return sorted(markdown_files)


def read_file_content(file_path: Path) -> Tuple[str, bool]:
    """
    Read the content of a file with proper encoding handling.
    
    Args:
        file_path: Path to the file to read
        
    Returns:
        Tuple of (content, success_flag)
    """
    encodings = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252']
    
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                return f.read(), True
        except UnicodeDecodeError:
            continue
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return "", False
    
    print(f"Could not decode {file_path} with any supported encoding")
    return "", False


def get_topic_from_path(file_path: Path, base_dir: Path) -> str:
    """
    Extract topic from file path. 
    E.g., docs/python/basics/intro.md -> python
    E.g., docs/algorithms/sorting/quicksort.md -> algorithms
    """
    relative_path = file_path.relative_to(base_dir)
    parts = relative_path.parts
    
    # If file is directly in base_dir, use 'general' as topic
    if len(parts) == 1:
        return 'general'
    
    # Otherwise, first directory after base_dir is the topic
    return parts[0]


def estimate_size(content: str) -> int:
    """Estimate the size of content in bytes."""
    return len(content.encode('utf-8'))


def split_and_save_topic(topic: str, sections: List[Tuple[str, str]], 
                        output_dir: Path, max_size_mb: float) -> int:
    """
    Split topic content into multiple files if needed.
    
    Args:
        topic: Topic name
        sections: List of (file_path, content) tuples
        output_dir: Output directory
        max_size_mb: Maximum size per file in MB
        
    Returns:
        Number of files created for this topic
    """
    max_size_bytes = int(max_size_mb * 1024 * 1024)
    
    # Create topic directory
    topic_dir = output_dir / topic
    topic_dir.mkdir(parents=True, exist_ok=True)
    
    current_content = []
    current_size = 0
    file_number = 1
    
    # Header for each file
    def create_header(part_num, total="TBD"):
        return (f"# {topic.title()} Notes - Part {part_num}\n"
                f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"Topic: {topic}\n"
                f"This is part {part_num} of {total} parts\n\n---\n\n")
    
    files_created = []
    
    for file_path, content in sections:
        # Add file header
        section_content = f"## File: {file_path}\n\n{content}\n\n---\n\n"
        section_size = estimate_size(section_content)
        
        # Check if adding this would exceed limit
        if current_size + section_size > max_size_bytes and current_content:
            # Save current file
            file_name = f"{topic}_{file_number}.md"
            file_path = topic_dir / file_name
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(create_header(file_number))
                f.write(''.join(current_content))
            
            files_created.append(file_path)
            file_number += 1
            current_content = []
            current_size = 0
        
        current_content.append(section_content)
        current_size += section_size
    
    # Save last file
    if current_content:
        file_name = f"{topic}_{file_number}.md"
        file_path = topic_dir / file_name
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(create_header(file_number))
            f.write(''.join(current_content))
        
        files_created.append(file_path)
    
    # Update headers with correct total
    for i, file_path in enumerate(files_created, 1):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        content = content.replace(
            f"This is part {i} of TBD parts",
            f"This is part {i} of {len(files_created)} parts"
        )
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    return len(files_created)


def collect_by_topics(docs_dir: Path, output_dir: Path, 
                     max_size_mb: float = 1.0,
                     create_index: bool = True) -> None:
    """
    Collect markdown files organized by topic directories.
    
    Args:
        docs_dir: Base directory containing topic subdirectories
        output_dir: Output directory for split files
        max_size_mb: Maximum size per file in MB
        create_index: Whether to create an index file
    """
    if not docs_dir.exists():
        raise ValueError(f"Directory {docs_dir} does not exist")
    
    if not docs_dir.is_dir():
        raise ValueError(f"{docs_dir} is not a directory")
    
    # Find all markdown files
    markdown_files = find_markdown_files(docs_dir)
    
    if not markdown_files:
        print("No markdown files found in the directory")
        return
    
    print(f"Found {len(markdown_files)} markdown files")
    
    # Group files by topic
    files_by_topic = defaultdict(list)
    
    for file_path in markdown_files:
        topic = get_topic_from_path(file_path, docs_dir)
        files_by_topic[topic].append(file_path)
    
    print(f"\nFound {len(files_by_topic)} topics:")
    for topic, files in sorted(files_by_topic.items()):
        print(f"  📁 {topic}: {len(files)} files")
    
    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Process each topic
    topic_stats = {}
    index_content = [
        "# Markdown Notes Index\n",
        f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n",
        f"Source directory: {docs_dir.absolute()}\n",
        f"Total topics: {len(files_by_topic)}\n",
        f"Total files: {len(markdown_files)}\n\n"
    ]
    
    for topic in sorted(files_by_topic.keys()):
        print(f"\nProcessing topic: {topic}")
        topic_files = files_by_topic[topic]
        
        # Collect content for this topic
        topic_sections = []
        successful_files = 0
        failed_files = 0
        total_size = 0
        
        for file_path in sorted(topic_files):
            relative_path = file_path.relative_to(docs_dir)
            print(f"  Reading: {relative_path}")
            
            content, success = read_file_content(file_path)
            
            if success and content.strip():
                topic_sections.append((str(relative_path), content))
                successful_files += 1
                total_size += estimate_size(content)
            else:
                failed_files += 1
        
        # Split and save topic files
        if topic_sections:
            num_files = split_and_save_topic(topic, topic_sections, output_dir, max_size_mb)
            
            topic_stats[topic] = {
                'files_processed': successful_files,
                'files_failed': failed_files,
                'total_size_mb': total_size / (1024 * 1024),
                'split_files': num_files
            }
            
            # Add to index
            index_content.append(f"\n## Topic: {topic}\n")
            index_content.append(f"- Source files: {successful_files}\n")
            index_content.append(f"- Total size: {total_size / (1024 * 1024):.2f} MB\n")
            index_content.append(f"- Split into: {num_files} file(s)\n")
            index_content.append(f"- Location: `{output_dir.name}/{topic}/`\n")
            
            if num_files == 1:
                index_content.append(f"- File: `{topic}_{1}.md`\n")
            else:
                index_content.append(f"- Files: `{topic}_1.md` to `{topic}_{num_files}.md`\n")
    
    # Print summary
    print("\n" + "="*50)
    print("📊 Collection Summary")
    print("="*50)
    
    for topic, stats in sorted(topic_stats.items()):
        print(f"\n📁 {topic}:")
        print(f"   Files processed: {stats['files_processed']}")
        print(f"   Total size: {stats['total_size_mb']:.2f} MB")
        print(f"   Split into: {stats['split_files']} file(s)")
        
        # List created files
        topic_dir = output_dir / topic
        for i in range(1, stats['split_files'] + 1):
            file_path = topic_dir / f"{topic}_{i}.md"
            size = file_path.stat().st_size / (1024 * 1024)
            print(f"     - {topic}_{i}.md: {size:.2f} MB")
    
    # Create index file if requested
    if create_index:
        index_file = output_dir / "index.md"
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(''.join(index_content))
        
        print(f"\n📄 Created index file: {index_file}")
    
    print(f"\n✅ All files saved to: {output_dir.absolute()}")
    print("\n💡 You can now upload individual topic files to your Claude project!")


def main():
    parser = argparse.ArgumentParser(
        description="Collect markdown files by topic and split them appropriately"
    )
    parser.add_argument(
        "docs_dir",
        type=str,
        help="Path to your docs directory containing topic subdirectories"
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        default="split",
        help="Output directory name (default: split)"
    )
    parser.add_argument(
        "--max-size",
        type=float,
        default=1.0,
        help="Maximum size per file in MB (default: 1.0)"
    )
    parser.add_argument(
        "--no-index",
        action="store_true",
        help="Don't create an index file"
    )
    
    args = parser.parse_args()
    
    docs_dir = Path(args.docs_dir)
    output_dir = Path(args.output)
    
    try:
        collect_by_topics(
            docs_dir,
            output_dir,
            max_size_mb=args.max_size,
            create_index=not args.no_index
        )
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
