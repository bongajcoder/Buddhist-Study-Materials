# Buddhist Study Materials TTS Project - Full Documentation

## Project History

### Phase 1: PDF to Text Extraction
- Extracted text from Buddhist study material PDFs
- Organized into 4 main categories
- Created individual chapter text files

### Phase 2: v1 TTS Processing (Completed Dec 2025)
- Processed all text files through Kokoro TTS
- Generated 55 MP3 audiobooks (~2GB total)
- **Issues discovered**: Awkward pauses, robotic reading in places

### Phase 3: v2 Text Cleanup (Completed Dec 2025)
- Manually reviewed ALL 56 text files
- Removed Markdown formatting
- Fixed OCR artifacts
- Optimized text for TTS readability

### Phase 4: v2 TTS Processing (Completed Dec 2025)
- Regenerated all audio from cleaned text
- 55 MP3 files, 2.2GB total
- Significantly improved audio quality

---

## Detailed Text Cleanup Process

Each text file was manually reviewed and cleaned. The following transformations were applied:

### Formatting Removed:
```
# Header          → Header
## Subheader      → Subheader
**bold text**     → bold text
*italic text*     → italic text
_italic text_     → italic text
- bullet point    → [converted to prose or removed]
```

### Number Formatting:
```
1-10              → 1 through 10
Sections 1-5      → Sections 1 through 5
pages 3-5         → pages 3 through 5
```

### Reference Formatting:
```
(WND-1, 3)        → (WND-1, page 3) or kept as-is
page m.           → p.m.
```

### Structural Changes:
- Removed Table of Contents markers that read awkwardly
- Combined fragmented sentences across line breaks
- Removed placeholder text like "[Content summarizing...]"
- Converted list structures to flowing prose where appropriate

---

## File Inventory

### 00-On-Attaining-Buddhahood (8 files)
| File | Description |
|------|-------------|
| On Attaining Buddhahood - 00 Front Matter.txt | Title, TOC, Editor's Note |
| On Attaining Buddhahood - 01 Chapter 1.txt | Fundamental Purpose of Life |
| On Attaining Buddhahood - 02 Chapter 2.txt | Significance of Chanting |
| On Attaining Buddhahood - 03 Chapter 3.txt | Law Outside Yourself |
| On Attaining Buddhahood - 04 Chapter 4.txt | Transforming Fundamental Attitude |
| On Attaining Buddhahood - 05 Chapter 5.txt | Brave and Vigorous Spirit |
| On Attaining Buddhahood - 06 Chapter 6.txt | Mystic Nature of Our Lives |
| On Attaining Buddhahood - 07 Chapter 7.txt | Oneness of Mentor and Disciple |

### 01-Wisdom-Happiness-Peace (32 files)
Chapters 01-31 plus Conclusion covering SGI President Ikeda's guidance on creating happiness and peace through Buddhist practice.

### 02-Basics-Nichiren-Buddhism (10 files)
| File | Description |
|------|-------------|
| Chapter-01.txt | Introduction to Nichiren Buddhism |
| Chapter-02.txt | The Gohonzon |
| Chapter-03.txt | Faith, Practice, and Study |
| Chapter-04.txt | The Oneness of Mentor and Disciple |
| Chapter-05.txt | Shakubuku and Dialogue |
| Chapter-06.txt | The SGI Organization |
| Chapter-07.txt | Kosen-rufu and World Peace |
| Chapter-08.txt | **EMPTY FILE** |
| Chapter-09.txt | Buddhist View of Life and Death |
| Chapter-10.txt | Conclusion |

### 03-New-Human-Revolution (6 files)
Volume 30 chapters covering Shin'ichi Yamamoto's 1981 activities:
| File | Description |
|------|-------------|
| Chapter-01-Great-Mountain.txt | Sections 1-60 |
| Chapter-02-Awaiting-the-Time.txt | Sections 11-68 |
| Chapter-03-Launching-Out.txt | Sections 11-65 |
| Chapter-04-Bells-of-Dawn.txt | Sections 1-80 (summary format) |
| Chapter-05-Cheers-of-Victory.txt | Sections 1-89 |
| Chapter-06-Vow.txt | Sections 1-139 (final volume) |

---

## Technical Details

### TTS Engine: Kokoro
- Model: prince-canuma/Kokoro-82M
- MLX-based (optimized for Apple Silicon)
- Located: `../text-to-speech-local-models/kokoro/`

### Voice Settings
- Voice ID: `bf_isabella`
- Language: British English (code: `b`)
- Speed: 1.0x (normal)

### Audio Output
- Format: MP3
- Bitrate: 192 kbps
- Channels: Mono
- Sample Rate: 24000 Hz

### Processing Pipeline
1. Read text file
2. Generate audio in WAV segments (Kokoro outputs numbered segments)
3. Combine all segments using pydub
4. Export as single MP3
5. Delete intermediate WAV files
6. Update progress tracker

---

## Troubleshooting

### If audio sounds robotic or has pauses:
- Check source text file in `text_v2_combined/`
- Look for remaining Markdown or special characters
- Manually clean and reprocess

### If processing fails:
- Check `v2_tts_progress.json` for failed files
- Ensure Kokoro venv is activated
- Check for sufficient disk space

### To reprocess a single file:
1. Remove the file entry from `v2_tts_progress.json`
2. Delete the existing MP3 from `audio_output_v2/`
3. Run `batch_buddhist_v2.py` again

---

## Future Improvements (Optional)

1. **Voice variety**: Try different Kokoro voices for different books
2. **Speed adjustment**: Some users prefer 1.1x or 1.2x speed
3. **Chapter markers**: Add metadata for audiobook chapter navigation
4. **Missing content**: Chapter 8 of Basics needs source content

---

## Credits

- **Source Materials**: SGI-USA publications
- **TTS Model**: Kokoro by Prince Canuma
- **Processing**: Bongani Mlambo with Claude Code assistance
- **Date Completed**: December 2025
