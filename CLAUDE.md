# Buddhist Study Materials - TTS Audiobook Project

## Project Status: COMPLETE

| Version | Status | Files | Size | Location |
|---------|--------|-------|------|----------|
| v1 | Complete (deprecated) | 55 MP3s | 2.0 GB | `audio_output_combined/` |
| **v2** | **COMPLETE** | **55 MP3s** | **2.2 GB** | **`audio_output_v2/`** |

---

## Quick Reference

### Use v2 Audio (Recommended)
```
audio_output_v2/
├── 00-On-Attaining-Buddhahood/    (8 MP3s)
├── 01-Wisdom-Happiness-Peace/     (32 MP3s)
├── 02-Basics-Nichiren-Buddhism/   (9 MP3s - Ch8 source was empty)
└── 03-New-Human-Revolution/       (6 MP3s)
```

### TTS Configuration
- **Model**: Kokoro-82M (prince-canuma/Kokoro-82M)
- **Voice**: bf_isabella (British female)
- **Format**: MP3 @ 192kbps
- **Speed**: 1.0x

---

## Project History

### v1 (Completed: Nov 2024)
- Generated 55 MP3s from original text files
- **Issues**: Awkward pauses from Markdown formatting, OCR artifacts, line breaks

### v2 Text Cleanup (Completed: Dec 2025)
- **MANUAL review** of all 56 text files (not programmatic)
- Removed Markdown headers (#, ##, ###)
- Removed bold (**) and italic (* _) markers
- Removed bullet points (-)
- Converted "1-10" to "1 through 10"
- Fixed OCR artifacts and encoding issues
- Cleaned line breaks for natural reading flow

### v2 TTS Processing (Completed: Dec 2025)
- Regenerated all audio from cleaned text
- 55 MP3 files, 2.2 GB total
- 0 failures

---

## Directory Structure

```
Buddhist-Study-Materials/
├── CLAUDE.md                          # This file
├── PROJECT_DOCUMENTATION.md           # Detailed documentation
├── v2_tts_progress.json               # TTS progress tracker
│
├── text_v2_combined/                  # CLEANED source text (56 files)
│   ├── 00-On-Attaining-Buddhahood/   (8 files)
│   ├── 01-Wisdom-Happiness-Peace/    (32 files)
│   ├── 02-Basics-Nichiren-Buddhism/  (10 files - Ch8 empty)
│   └── 03-New-Human-Revolution/      (6 files)
│
├── audio_output_v2/                   # FINAL v2 MP3s (2.2 GB)
│   ├── 00-On-Attaining-Buddhahood/
│   ├── 01-Wisdom-Happiness-Peace/
│   ├── 02-Basics-Nichiren-Buddhism/
│   └── 03-New-Human-Revolution/
│
├── audio_output_combined/             # v1 MP3s (deprecated)
├── text_v2_tts_optimized/             # Raw text copies (435 files)
└── [Original PDF source folders]
```

---

## Content Summary

### 00-On-Attaining-Buddhahood (8 chapters)
SGI President Ikeda's lecture series on Nichiren's writing "On Attaining Buddhahood in This Lifetime"

### 01-Wisdom-Happiness-Peace (32 chapters)
"The Wisdom for Creating Happiness and Peace" - Selections from writings of Daisaku Ikeda

### 02-Basics-Nichiren-Buddhism (10 chapters, Ch8 empty)
"The Basics of Nichiren Buddhism for the New Era of Worldwide Kosen-rufu"

### 03-New-Human-Revolution (6 chapters)
Volume 30 of "The New Human Revolution" - Shin'ichi Yamamoto's activities in 1981

---

## Regenerating Audio

If you need to regenerate the audio:

```bash
cd /Users/bonganimlambo/Documents/Code\ Development/Projects/text-to-speech-local-models/kokoro
source .venv/bin/activate
python ../batch_buddhist_v2.py
```

The script:
- Reads from `text_v2_combined/`
- Outputs to `audio_output_v2/`
- Tracks progress in `v2_tts_progress.json`
- Skips already-completed files
- Combines WAV segments into single MP3 per chapter

To reprocess a specific file:
1. Remove its entry from `v2_tts_progress.json`
2. Delete the existing MP3 from `audio_output_v2/`
3. Run the batch script again

---

## Important Notes

1. **Text cleanup was MANUAL** - Each file reviewed line-by-line for TTS readability
2. **Chapter 8 of Basics is empty** - Source file had no content
3. **v1 audio deprecated** - Use v2 for better quality
4. **Original files unchanged** - All edits in `text_v2_combined/`

---

## Key Scripts

| Script | Location | Purpose |
|--------|----------|---------|
| `batch_buddhist_v2.py` | `../text-to-speech-local-models/` | v2 batch TTS processing |
| `batch_buddhist_tts.py` | `../text-to-speech-local-models/` | v1 script (deprecated) |

---

*Last Updated: December 2025*
*Project Status: COMPLETE*
