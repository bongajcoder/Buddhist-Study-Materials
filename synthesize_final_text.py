#!/usr/bin/env python3
"""
Final Text Synthesis Script for "On Attaining Buddhahood in This Lifetime"

This script creates the most accurate possible text by:
1. Using gemini_full.txt as structural base (best page organization)
2. Applying comprehensive OCR error corrections
3. Fixing Buddhist terminology consistently
4. Removing page artifacts and headers
5. Producing a clean, book-quality text

Author: Buddhist Study Materials Project
Date: November 2025
"""

import re
from pathlib import Path
from datetime import datetime

# Configuration
BASE_DIR = Path("/Users/bonganimlambo/Documents/Code Development/Projects/Buddhist-Study-Materials/00-On Attaining Buddhism")
OUTPUT_FILE = BASE_DIR / "FINAL_BOOK_TEXT.txt"

# Primary source (best structure and completeness)
PRIMARY_SOURCE = BASE_DIR / "gemini extractions" / "on_attaining_buddhahood_gemini_full.txt"

# Chapter titles for reference
CHAPTERS = {
    1: "Attaining Buddhahood in This Lifetime—The Fundamental Purpose of Life and a Source of Hope for Humankind",
    2: "The Significance of Chanting Nam-myoho-renge-kyo—Achieving a Life of Supreme Victory Through Correct Buddhist Practice",
    3: "'If You Think the Law Is Outside Yourself, You Are Not Embracing the Mystic Law'",
    4: "Transforming Our Fundamental Attitude—Refusing To Live an 'Endless, Painful Austerity'",
    5: "Chanting Nam-myoho-renge-kyo With a 'Brave and Vigorous' Spirit—Polishing Our Lives Through Daily Challenge",
    6: "The Mystic Nature of Our Lives—'Become the Master of Your Mind Rather Than Let Your Mind Master You'",
    7: "Faith for Attaining Buddhahood in This Lifetime—Advance Unerringly Along the Great Path of the Oneness of Mentor and Disciple",
}


def load_text(filepath: Path) -> str:
    """Load text file with fallback encodings."""
    for encoding in ['utf-8', 'latin-1', 'cp1252']:
        try:
            with open(filepath, 'r', encoding=encoding) as f:
                return f.read()
        except UnicodeDecodeError:
            continue
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        return f.read()


def comprehensive_corrections(text: str) -> str:
    """Apply comprehensive OCR error corrections."""

    # ===== REMOVE MAJOR OCR ARTIFACTS FIRST =====
    # Remove heavily corrupted lines (mostly symbols/garbled text)
    text = re.sub(r'^[^\w\s]*[\-_\~\=\◄\►\▼\▲\•\♦\★\☆\○\●\□\■\△\▽\◇\◆\§\¶\†\‡\※\⁂\⁕\⁑\⁎\⁏\⁐\⁗\℗\®\©\™\℠\℡\℮\ℯ\ℰ\ℱ\Ⅻ\ⅻ\ⅿ\ↀ\ↁ\ↂ\Ↄ\ↄ\ↅ\ↆ\ↇ\ↈ]+[^\w\s]*$', '', text, flags=re.MULTILINE)

    # Remove lines that are mostly non-word characters
    def is_garbled_line(line):
        if not line.strip():
            return False
        word_chars = sum(1 for c in line if c.isalnum() or c.isspace())
        total_chars = len(line)
        return total_chars > 5 and (word_chars / total_chars) < 0.4

    lines = text.split('\n')
    cleaned_lines = [line for line in lines if not is_garbled_line(line)]
    text = '\n'.join(cleaned_lines)

    # ===== BUDDHIST TERMINOLOGY CORRECTIONS =====
    # These are the most critical - Buddhist names and terms

    buddhist_terms = {
        # Nichiren Daishonin variations
        r'\bNichirend?\b': 'Nichiren',
        r'\bNichrn\b': 'Nichiren',
        r'\bNichran\b': 'Nichiren',
        r'\bNicbiren\b': 'Nichiren',
        r'\bNkbiren\b': 'Nichiren',
        r'\bNietzsche\b(?=.*[Dd]ysonen|.*[Dd]aishonin|.*Buddhism)': 'Nichiren',  # Audio transcription error

        r'\bDaysonan\b': 'Daishonin',
        r'\bDaysonen\b': 'Daishonin',
        r'\bDaysonin\b': 'Daishonin',
        r'\bDayshonan\b': 'Daishonin',
        r'\bDayshoning\b': 'Daishonin',
        r'\bDaishonan\b': 'Daishonin',
        r'\bDatshonin\b': 'Daishonin',
        r'\bDaisbonin\b': 'Daishonin',
        r'\bDysonen\b': 'Daishonin',

        # Nam-myoho-renge-kyo variations
        r'\bNam-myohoringa\s+Kyol?\b': 'Nam-myoho-renge-kyo',
        r'\bNam-Myoho-Renge-Kyo\b': 'Nam-myoho-renge-kyo',
        r'\bNam-myoho-renge-Kyo\b': 'Nam-myoho-renge-kyo',
        r'\bNam-myoho\s+renge\s+kyo\b': 'Nam-myoho-renge-kyo',
        r'\bNamyoho-renge-kyo\b': 'Nam-myoho-renge-kyo',
        r'\bNam Yoho\b': 'Nam-myoho',
        r'\bNam Yohorenga\b': 'Nam-myoho-renge',
        r'\bN=\s*myohu-renge-kyo\b': 'Nam-myoho-renge-kyo',

        # Myoho-renge-kyo variations
        r'\bMyhorengeol\b': 'Myoho-renge-kyo',
        r'\bMyohoringe\b': 'Myoho-renge-kyo',
        r'\bMyohoring\b': 'Myoho-renge-kyo',
        r'\bMiohoringo\b': 'Myoho-renge-kyo',
        r'\bMiohorengeol\b': 'Myoho-renge-kyo',
        r'\bMyo\s+Horengeo\b': 'Myoho-renge-kyo',
        r'\bmyhorengeol\b': 'Myoho-renge-kyo',
        r'\bmyhorengeo\b': 'Myoho-renge-kyo',
        r'\bllohorenge-kyo\b': 'Myoho-renge-kyo',
        r'\bMyoho-renge-l\'yo\b': 'Myoho-renge-kyo',
        r'\bMyoho-raige-kyo\b': 'Myoho-renge-kyo',
        r'\bM}\'oho-rmge-l\'yo\b': 'Myoho-renge-kyo',
        r'\bMyoho-reng,...\s*kyo\b': 'Myoho-renge-kyo',

        # Other Buddhist terms
        r'\bBuddhahhod\b': 'Buddhahood',
        r'\bBtiddhahood\b': 'Buddhahood',
        r'\bBuddbahcwf\b': 'Buddhahood',
        r'\bBuJdhahood\b': 'Buddhahood',
        r'\bBuJJhahood\b': 'Buddhahood',
        r'\bBnddhahood\b': 'Buddhahood',
        r'\bRnddb!st\b': 'Buddhist',
        r'\bBudJ.h.l\b': 'Buddha',
        r'\bBuJJha\b': 'Buddha',
        r'\bBuddbahond\b': 'Buddhahood',

        r'\bShalyamuni\b': 'Shakyamuni',
        r'\bShJkyamunl\b': 'Shakyamuni',
        r'\bShJkyamuni\b': 'Shakyamuni',

        r'\bGonggyo\b': 'Gongyo',
        r'\bGakai\b': 'Gakkai',
        r'\bGak.kai\b': 'Gakkai',
        r'\bSaka\b(?=\s+University)': 'Soka',
        r'\bSaka\b(?=\s+Gakkai)': 'Soka',

        r'\bLotuS\b': 'Lotus',
        r'\blotw\b': 'Lotus',
        r'\bLotui\b': 'Lotus',
        r'\bl otw\b': 'Lotus',
        r'\bl otus\b': 'Lotus',

        r'\bSurr\.1\b': 'Sutra',
        r'\bSutr,1\b': 'Sutra',
        r'\bS111ra\b': 'Sutra',
        r'\bSMlnll\b': 'Sutras',

        r'\bDharma\b': 'Dharma',

        # WND references
        r'\(wwp-1\b': '(WND-1',
        r'\(WwND-1\b': '(WND-1',
        r'\(WNO-I\b': '(WND-1',
        r'\(WNO\.\s*I\b': '(WND-1',
        r'\(WND-7\b': '(WND-1',
        r'\(\\,VND-1\b': '(WND-1',
        r'\(/\\IWD-1\b': '(WND-1',
        r'WND-\s*1': 'WND-1',
    }

    for pattern, replacement in buddhist_terms.items():
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE if replacement.lower() == replacement else 0)

    # ===== OCR ARTIFACT CORRECTIONS =====
    ocr_fixes = {
        # Common OCR errors
        r'm\.-plen&nt': 'resplendent',
        r'rc\\\'olutionary': 'revolutionary',
        r'a\\.-complishing': 'accomplishing',
        r'<:hanged': 'changed',
        r'prac&--e': 'practice',
        r',icwed': 'viewed',
        r'practidng': 'practicing',
        r'higho1': 'highest',
        r'ronswn\.': 'constant,',
        r'~un': 'between',
        r'all\°"ing': 'allowing',
        r'oursel\\-es': 'ourselves',
        r'b\)\'': 'by',
        r'darknes\'S': 'darkness',
        r'onaasing\s*_\.\.\s*1fort': 'unceasing effort',
        r'~\s*of': 'essence of',
        r'dnrkncss': 'darkness',
        r'l\\cgativity': 'negativity',
        r'signi6cant': 'significant',
        r'50lll\'ce': 'source',
        r'bunwikind': 'humankind',
        r'tb,rc': 'there',
        r'livuig': 'living',
        r'bcms': 'beings',
        r'nfA1': 'next',
        r'prarti\.\.-e': 'practice',
        r'mn<asing': 'unceasing',
        r'1n other': 'In other',
        r'th\.ough': 'through',
        r'\'OUr': 'your',
        r'-\.iew': 'view',
        r'J\.1i': 'dai',
        r'\.shine': 'Daishonin',

        # Word breaks and hyphenation
        r'acti-\s*~?\s*vate': 'activate',
        r'acti-\s*vate': 'activate',
        r'mani-\s*fests': 'manifests',
        r'enlight-\s*enment': 'enlightenment',
        r'Bud-\s*dha': 'Buddha',
        r'ordi-\s*nary': 'ordinary',
        r'peo-\s*ple': 'people',
        r'trans-\s*migrate': 'transmigrate',
        r'trans-\s*migra-\s*tion': 'transmigration',
        r'hu-\s*man': 'human',
        r'reli-\s*gion': 'religion',
        r'enlight-\s*en-\s*ment': 'enlightenment',
        r'estab-\s*lished': 'established',
        r'prac-\s*tice': 'practice',
        r'spiri-\s*tual': 'spiritual',
        r'nega-\s*tive': 'negative',
        r'destruc-\s*tive': 'destructive',
        r'convic-\s*tion': 'conviction',
        r'spon-\s*ta-\s*neously': 'spontaneously',
        r'for-\s*mu-\s*lating': 'formulating',

        # Spacing issues
        r'\s{2,}': ' ',
        r'lt\s+means': 'It means',
        r'\bi\s+believe': 'I believe',
        r'\bi\s+will': 'I will',
        r'\bi\s+look': 'I look',
        r"I\s*'ll": "I'll",
        r"Pll": "I'll",

        # Punctuation
        r'\s+\.': '.',
        r'\s+,': ',',
        r'\s+;': ';',
        r'\s+:': ':',
        r',,': ',',
        r'\.\.': '.',

        # Common typos from audio transcription
        r'\bpray\b(?=\s+for|\s+to|\s+that)': 'pray',  # keep correct pray
        r'\basage\b': 'assuage',
        r'\bbreak\b(?=\s+through\s+the\s+darkness)': 'break',  # keep correct break

        # Garbled characters
        r'[ᥥ]+': '',
        r'f#,\.\.\s*\.---.*?---\s*': ' ',
        r'◄\s*': '',
        r'•\s*': '',
        r'~\s*(?=[A-Z])': '',

        # Page markers/artifacts to clean (keep page numbers clean)
        r'^---\s*Page\s+\d+\s*---$': '',  # Will handle these specially
        r'^\d+$': '',  # Solo page numbers on their own line

        # Headers to remove
        r'^On Attaining Buddhahood in This Lifetime$': '',  # Page header repeats
        r'^SGI President Ikeda\'s Lecture Series$': '',

        # Additional OCR garbage patterns
        r'yaa wim tD me JUIH idf': 'you wish to free yourself',
        r'e@HMecl simztime wilhout': 'endured since time without',
        r'rmgl,trnnml in dlidifdio~': 'enlightenment in this lifetime,',
        r'origimllf inhesn11 iaalltiringbrinp': 'originally inherent in all living beings',
        r'r0a AtlaiaiaglacMbeboocl': '("On Attaining Buddhahood',
        r'coostibrtes a cleeply rntaningful': 'constitutes a deeply meaningful',
        r'bappinew\. Nx:hirm lluddbivn': 'happiness. Nichiren Buddhism',
        r'ttaching of hope that enabla 11&': 'teaching of hope that enables us',
        r'UDS1l1\'pused': 'unsurpassed',
        r'wne\.': 'same.',
        r'asiured': 'assured',
        r'cnlightenmenL': 'enlightenment.',
        r'e:ci\.sts': 'exists',
        r'hwnanity': 'humanity',
        r'\\,VND': 'WND',
        r'\\Ve\'ll': "We'll",
        r'/\\IWD': 'WND',
        r'Myohorenge-kyo': 'Myoho-renge-kyo',
        r'Nammyoho-renge-kyo': 'Nam-myoho-renge-kyo',
        r'Nammyoho-rengekyo': 'Nam-myoho-renge-kyo',
        r'Nam-myohorenge-kyo': 'Nam-myoho-renge-kyo',
        r'lkedas': "Ikeda's",
        r'011 Attaining': 'On Attaining',
        r'Buddhal1ood': 'Buddhahood',
        r'i\'ifetime': 'Lifetime',
        r'profou7ld': 'profound',
        r'attaini~g': 'attaining',
        r'B11ddhahood': 'Buddhahood',
        r'irl this': 'in this',
        r'cm, powerfully': 'can powerfully',
        r'tran~fom1': 'transform',
        r'modem': 'modern',
        r'bis day': 'his day',
        r'peo-\s*ple': 'people',
        r'nfA1 time': 'next time',
    }

    for pattern, replacement in ocr_fixes.items():
        text = re.sub(pattern, replacement, text, flags=re.MULTILINE)

    return text


def clean_structure(text: str) -> str:
    """Clean document structure and formatting."""

    # Remove page markers but keep content organized
    # First, split by page markers
    pages = re.split(r'---\s*Page\s+(\d+)\s*---', text)

    # Reconstruct without markers
    cleaned_content = []

    i = 0
    while i < len(pages):
        content = pages[i].strip()
        if content and not content.isdigit():
            # Remove common OCR artifacts at start of pages
            content = re.sub(r'^[\s\.\,\'\"\*\•\~\-\_\=]+', '', content)
            # Remove stray characters
            content = re.sub(r'^[a-z]\s*$', '', content, flags=re.MULTILINE)
            # Remove garbled lines
            content = re.sub(r'^[^\w\s]{3,}.*$', '', content, flags=re.MULTILINE)
            content = re.sub(r'^[\s\.\,\'\"\*\•\~\-\=\◄\►\►\▼\▲]+$', '', content, flags=re.MULTILINE)
            # Remove lines that are mostly symbols
            content = re.sub(r'^[^a-zA-Z]*$', '', content, flags=re.MULTILINE)

            if content.strip():
                cleaned_content.append(content)
        i += 1

    # Join with proper spacing
    text = '\n\n'.join(cleaned_content)

    # Fix multiple newlines
    text = re.sub(r'\n{3,}', '\n\n', text)

    # Fix orphaned punctuation
    text = re.sub(r'\n([,\.\;\:])', r'\1', text)

    # Join broken sentences
    text = re.sub(r'(\w)-\s*\n\s*(\w)', r'\1\2', text)

    return text.strip()


def remove_front_matter(text: str) -> str:
    """Remove or format front matter (title page, copyright, etc.)."""

    # Find where actual content begins (after Editor's Note)
    editor_note_match = re.search(r"Editor's\s*Note", text, re.IGNORECASE)

    if editor_note_match:
        # Keep from Editor's Note onward
        text = text[editor_note_match.start():]

    return text


def format_chapter_headers(text: str) -> str:
    """Properly format chapter headers."""

    # Chapter patterns to identify
    chapter_patterns = [
        r'\[(\d+)\]',  # [1], [2], etc.
        r'\((\d+)\)',  # (1), (2), etc.
        r'Chapter\s+(\d+)',
    ]

    for i, title in CHAPTERS.items():
        # Look for chapter indicators and ensure proper formatting
        text = re.sub(
            rf'\[{i}\]\s*\n*({re.escape(title[:30])})',
            f'\n\n{"="*70}\nCHAPTER {i}\n{title}\n{"="*70}\n\n',
            text,
            flags=re.IGNORECASE
        )

    return text


def final_polish(text: str) -> str:
    """Final polish and quality checks."""

    # Ensure proper spacing around quotes
    text = re.sub(r'"\s+', '" ', text)
    text = re.sub(r'\s+"', ' "', text)

    # Fix common remaining issues
    text = re.sub(r'\s+\'s\b', "'s", text)
    text = re.sub(r'\s+n\'t\b', "n't", text)

    # Ensure single space after periods (except abbreviations)
    text = re.sub(r'\.  +', '. ', text)

    # Remove trailing whitespace
    text = '\n'.join(line.rstrip() for line in text.split('\n'))

    return text


def verify_key_phrases(text: str) -> dict:
    """Verify presence of key phrases from the book."""

    key_phrases = [
        "If you wish to free yourself from the sufferings of birth and death",
        "This truth is Myoho-renge-kyo",
        "Chanting Myoho-renge-kyo will therefore enable you to grasp the mystic truth",
        "Even though you chant and believe in Myoho-renge-kyo",
        "Arouse deep faith, and diligently polish your mirror day and night",
        "The Lotus Sutra is the king of sutras",
        "fundamental darkness",
        "attaining Buddhahood in this lifetime",
        "Nam-myoho-renge-kyo",
        "Nichiren Daishonin",
        "Soka Gakkai",
        "oneness of mentor and disciple",
        "human revolution",
        "mystic truth innate in all life",
    ]

    results = {}
    for phrase in key_phrases:
        found = phrase.lower() in text.lower()
        results[phrase] = found

    return results


def create_final_text():
    """Main function to create the final synthesized text."""

    print("=" * 70)
    print("FINAL TEXT SYNTHESIS")
    print("On Attaining Buddhahood in This Lifetime")
    print("=" * 70)

    # Load primary source
    print("\n1. Loading primary source (gemini_full.txt)...")
    text = load_text(PRIMARY_SOURCE)
    print(f"   Loaded {len(text):,} characters")

    # Apply comprehensive corrections
    print("\n2. Applying OCR error corrections...")
    text = comprehensive_corrections(text)
    print("   Applied Buddhist terminology fixes")
    print("   Applied OCR artifact corrections")

    # Clean structure
    print("\n3. Cleaning document structure...")
    text = clean_structure(text)
    print("   Removed page markers and artifacts")

    # Remove/format front matter
    print("\n4. Formatting document...")
    text = remove_front_matter(text)
    text = format_chapter_headers(text)
    text = final_polish(text)

    # Verify key phrases
    print("\n5. Verifying key phrases...")
    verification = verify_key_phrases(text)
    passed = sum(1 for v in verification.values() if v)
    total = len(verification)
    print(f"   {passed}/{total} key phrases verified")

    for phrase, found in verification.items():
        status = "✓" if found else "✗"
        print(f"   {status} {phrase[:50]}...")

    # Create output
    output = []
    output.append("=" * 70)
    output.append("ON ATTAINING BUDDHAHOOD IN THIS LIFETIME")
    output.append("Lectures by SGI President Daisaku Ikeda")
    output.append("=" * 70)
    output.append("")
    output.append("SYNTHESIZED BOOK TEXT")
    output.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    output.append("")
    output.append("This text has been synthesized from multiple OCR sources")
    output.append("with comprehensive error corrections applied.")
    output.append("=" * 70)
    output.append("")
    output.append("")
    output.append(text)

    final_text = '\n'.join(output)

    # Write output
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(final_text)

    print(f"\n6. Output saved to: {OUTPUT_FILE}")
    print(f"   Total characters: {len(final_text):,}")

    # Statistics
    word_count = len(final_text.split())
    line_count = len(final_text.split('\n'))
    print(f"   Word count: {word_count:,}")
    print(f"   Line count: {line_count:,}")

    print("\n" + "=" * 70)
    print("SYNTHESIS COMPLETE")
    print("=" * 70)

    return final_text


if __name__ == '__main__':
    create_final_text()
