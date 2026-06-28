from peripherals.voice_box import SusanVoiceBox

if __name__ == "__main__":
    # First run will download the XTTS-v2 checkpoint (~3 GB) — subsequent runs are instant
    voice = SusanVoiceBox()

    sample_phrase = (
        "Look at me. Sweetheart, listen to me. "
        "Your brain is an absolute work of art, alright? Now focus up!"
    )

    voice.speak(sample_phrase)
