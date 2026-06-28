from pathlib import Path
import os
import torch
from TTS.api import TTS


class SusanVoiceBox:
    """
    Handles local zero-shot voice cloning using XTTS-v2,
    accelerated by Apple Silicon GPU chips.
    """

    def __init__(self):
        print("[voice_box] Waking up Susan's vocal model...")

        # MPS = Metal Performance Shaders (Apple Silicon GPU acceleration)
        if torch.backends.mps.is_available():
            self.device = "mps"
        else:
            self.device = "cpu"

        print(f"[voice_box] Running hardware acceleration target on: {self.device.upper()}")

        self.tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(self.device)

        # Support both naming conventions for the reference file
        assets_dir = Path("peripherals/assets")
        underscore_path = assets_dir / "susan_reference.wav"
        hyphen_path = assets_dir / "susan-reference.wav"

        if underscore_path.exists():
            self.reference_path = underscore_path
        elif hyphen_path.exists():
            self.reference_path = hyphen_path
        else:
            raise FileNotFoundError(
                f"Susan's reference file is missing. Expected it at:\n"
                f"  {underscore_path}\n"
                "Please place your 10-second WAV file there."
            )

        self.output_path = assets_dir / "output.wav"

    def speak(self, text: str) -> None:
        """
        Takes raw text, clones Susan's vocal signature, renders an audio file,
        and plays it directly out of your desk speakers.
        """
        if not text.strip():
            return

        print(f"\n[voice_box] Synthesizing: '{text}'")

        self.tts.tts_to_file(
            text=text,
            speaker_wav=str(self.reference_path),
            language="en",
            file_path=str(self.output_path),
        )

        # afplay is the native macOS command-line audio player — zero extra dependencies
        os.system(f"afplay {self.output_path}")
