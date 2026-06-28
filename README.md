# voxie-bestie

A local AI study companion that speaks in Susan's voice (from *The Marvelous Mrs. Maisel*), powered by zero-shot voice cloning via XTTS-v2.

## Architecture

```
voxie/
├── brain/
│   └── client.py          # VoxieClient — manages rooms & message history
├── peripherals/
│   ├── voice_box.py       # SusanVoiceBox — XTTS-v2 voice cloning engine
│   └── assets/            # susan-reference.wav (not tracked), output.wav (generated)
├── rooms/                 # Knowledge domain directories
├── tests/                 # pytest suite
├── main.py
└── test_voice.py          # Standalone voice verification script
```

## Setup

Requires Python 3.11, uv, cmake, and LLVM 20 (all installed via Homebrew).

```bash
uv venv --python 3.11
source .venv/bin/activate

# LLVM 20 must be on the build path for llvmlite to compile
export LLVM_CONFIG=/usr/local/opt/llvm@20/bin/llvm-config
export CMAKE_PREFIX_PATH=/usr/local/opt/llvm@20

uv pip install TTS soundfile
uv pip install "transformers>=4.33.0,<4.40"   # pin for XTTS-v2 compatibility
uv pip install pytest
```

## Voice Reference File

Place a clean 10–30 second WAV clip of Susan's voice at:

```
peripherals/assets/susan-reference.wav
```

The file must be pre-processed to **22050 Hz, mono, PCM-16**. Use the helper snippet in `test_voice.py` or run:

```python
import soundfile as sf
from scipy.signal import resample_poly
from math import gcd

data, sr = sf.read("peripherals/assets/susan-reference.wav")
if data.ndim == 2:
    data = data.mean(axis=1)          # stereo -> mono
target_sr = 22050
g = gcd(sr, target_sr)
data = resample_poly(data, target_sr // g, sr // g)
sf.write("peripherals/assets/susan-reference.wav", data, target_sr, subtype="PCM_16")
```

## Running

```bash
# Verify voice cloning works (downloads ~1.87 GB XTTS-v2 model on first run)
python test_voice.py

# Run tests
pytest
```

## Voice Cloning Notes

- XTTS-v2 is **zero-shot** — no retraining needed, just swap the reference WAV
- The model captures vocal timbre well; strong regional accents (Boston) require fine-tuning on more audio
- First-run model download goes to `~/Library/Application Support/tts/`
- Hardware: uses MPS (Apple Silicon GPU) if available, falls back to CPU
- `transformers` must stay pinned to `<4.40` — newer versions removed `BeamSearchScorer` which XTTS-v2 depends on
