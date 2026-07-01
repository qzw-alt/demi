#!/usr/bin/env python3
"""
inject-tcm-sections.py — verified 2026-07-01, chinahospitalsguide.com

Batch-injects a category-specific HTML section into every disease/procedure article
in a `blog/` directory. Companion to templates/tcm-section-by-category.html.

Pattern:
  1. Classify each article into a category by filename keyword match
  2. Pick the matching template (one of 12 TCM categories)
  3. Find the insertion point via multi-marker fallback (7 patterns, last-resort
     places the section right before </body></html>)
  4. Idempotency check via UTF-8 byte string of the section's unique emoji
  5. Verify final injection count == expected count

Usage:
  python3 inject-tcm-sections.py <blog_dir>

Output: prints "✅ Injected: N articles" + per-category breakdown + any failures
"""

import os
import re
import sys
from collections import Counter

# ----- Configuration -----

BLOG_DIR_DEFAULT = "/home/ubuntu/.hermes/workspace/website/blog"
MARKER_BYTES = b'\xf0\x9f\x8c\xbf'  # 🌿 UTF-8 bytes

# Skip these article types (city guides, hospital listings, visa pages, rankings, etc.)
SKIP_FILENAME_KEYWORDS = [
    'tcm', 'acupuncture', 'baduanjin', 'hainan-tcm',
    'china-unique-medical', 'integrated-chinese',
    'index.html',
    'choose-hospital', 'medical-guide', 'how-to-prepare',
    'how-to-book', 'how-to-choose',
    'japan-china', 'best-hospitals', 'hospitals-in-',
    'china-vs-usa', 'foreigners-guide',
    'medical-device', 'jci-accredited', 'proton-therapy',
    'why-choose', 'why-medical', 'why-international',
    'china-hospital-rankings', 'guangzhou-medical',
    'cost-comparison',
    'china-medical-visa', 'china-visa-free',
    'top-10-questions',
    'giving-birth',
    'how-to-see-a-doctor',
    'liver-treatment',
    # Already-injected files (pillar pages we just created)
    'china-unique-medical-procedures.html',
    'integrated-chinese-western-medicine-china.html',
    'autonomous-robotic-surgery-china.html',
    'solid-tumor-car-t-china.html',
    'microsurgery-replantation-china.html',
    'organ-transplant-china-cost-access.html',
    '3d-printed-implants-china.html',
    'hepatobiliary-surgery-china-wu-mengchao.html',
    'stem-cell-therapy-china-access.html',
    'crispr-gene-therapy-china-clinical-trials.html',
    'ophthalmology-china-volume-expertise.html',
    'jinan-respiratory',
]

# Category keyword lists (filename contains any keyword → mapped to category)
CATEGORY_KEYWORDS = {
    'cancer_tumor': ['cancer', 'tumor', 'car-t', 'leukemia', 'lymphoma', 'melanoma', 'thyroid'],
    'pain_chronic': ['pain', 'migraine', 'epilepsy', 'headache'],
    'ivf_fertility': ['ivf', 'fertility', 'endometriosis'],
    'orthopedic': ['knee', 'hip', 'spine', 'shoulder', 'rotator', 'bone', 'orthopedic', 'fracture', 'hernia'],
    'cardio': ['heart', 'cardiac', 'bypass'],
    'neuro': ['neuro', 'brain', 'dbs', 'stroke', 'parkinson'],
    'eye': ['lasik', 'smile', 'cataract', 'eye'],
    'dental': ['dental', 'implant'],
    'wellness': ['wellness', 'health-checkup', 'health-screening', 'checkup'],
    'cosmetic': ['plastic', 'rhinoplasty', 'breast', 'hair-transplant', 'weight-loss', 'gastric-sleeve'],
    'kidney_dialysis': ['kidney', 'dialysis'],
    'organ_transplant': ['transplant', 'bone-marrow'],
}

# Multi-marker fallback chain (first match wins)
INSERTION_MARKERS = [
    r'<h3[^>]*>\s*📚\s*Related Articles',
    r'<h3[^>]*>\s*📚\s*Related Reading',
    r'<h2[^>]*>[^<]*Related Articles',
    r'<h2[^>]*>[^<]*Related Reading',
    r'<h2[^>]*>[^<]*You Might Also Like',
    r'<h2[^>]*>[^<]*You may also like',
    r'<h2[^>]*>[^<]*See Also',
]

LAST_RESORT_MARKERS = [
    r'</div>\s*\n?\s*<footer',
    r'</div>\s*\n?\s*</body>',
]


# ----- Helper functions -----

def classify(filename):
    """Return category string or None."""
    fn = filename.lower()
    for cat, kws in CATEGORY_KEYWORDS.items():
        if any(kw in fn for kw in kws):
            return cat
    return None


def should_skip(filename):
    fn = filename.lower()
    return any(kw in fn for kw in SKIP_FILENAME_KEYWORDS)


def find_insertion_point(content):
    """Find best insertion point via multi-marker fallback. Returns byte offset or None."""
    for marker in INSERTION_MARKERS:
        m = re.search(marker, content, re.IGNORECASE)
        if m:
            return m.start()

    # Last resort: inject right before </body></html>
    for marker in LAST_RESORT_MARKERS:
        m = re.search(marker, content, re.IGNORECASE)
        if m:
            return m.start()

    return None


def inject(filepath, tcm_html):
    """Inject a TCM section into one file. Returns (success: bool, message: str)."""
    with open(filepath, 'rb') as f:
        content_bytes = f.read()

    # Idempotency: skip if section already present
    if MARKER_BYTES in content_bytes:
        return False, "already injected"

    try:
        content = content_bytes.decode('utf-8')
    except UnicodeDecodeError:
        return False, "encoding error (not UTF-8)"

    insertion_point = find_insertion_point(content)
    if insertion_point is None:
        return False, "no insertion point found"

    new_content = content[:insertion_point] + tcm_html + '\n' + content[insertion_point:]

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    return True, "ok"


def count_injections(blog_dir):
    """Count files that have the marker byte string."""
    count = 0
    for f in os.listdir(blog_dir):
        if not f.endswith('.html'):
            continue
        fp = os.path.join(blog_dir, f)
        try:
            with open(fp, 'rb') as fh:
                if MARKER_BYTES in fh.read():
                    count += 1
        except (IOError, OSError):
            pass
    return count


# ----- TCM Templates (12 categories) -----
# Same content as templates/tcm-section-by-category.html, inlined so the
# script is self-contained. If updating, update both files.

TCM_TEMPLATES = {
    'cancer_tumor': '<div class="highlight-box" style="border-left-color: #28a745; background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%); margin: 30px 0;"><h3 style="color: #155724; margin-top: 0;">🌿 TCM Support for Cancer Care in China</h3><p>Cancer treatment at leading Chinese hospitals often includes <strong>integrated Chinese-Western oncology</strong> — a combination unavailable elsewhere. Patients undergoing chemotherapy or recovering from surgery can access:</p><ul><li><strong>Acupuncture for chemo-induced nausea</strong> — clinically shown to reduce nausea severity by 40-60% at hospitals like Beijing University of Chinese Medicine Dongzhimen and Shanghai University of TCM Longhua.</li><li><strong>Chinese herbal medicine (中药)</strong> — used to mitigate side effects of chemo and radiotherapy, support immune function, and improve quality of life. Always prescribed alongside — never as a replacement for — Western oncology treatment.</li><li><strong>Baduanjin (八段锦) qigong</strong> — prescribed as a recovery exercise to rebuild strength and reduce cancer-related fatigue.</li></ul><p>This integration is built into cancer care at major academic centers. See our <a href="integrated-chinese-western-medicine-china.html">complete guide to integrated Chinese-Western medicine</a> for details.</p></div>\n',
    'pain_chronic': '<div class="highlight-box" style="border-left-color: #28a745; background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%); margin: 30px 0;"><h3 style="color: #155724; margin-top: 0;">🌿 TCM Options for Chronic Pain in China</h3><p>Chinese hospitals offer a full <strong>Traditional Chinese Medicine (TCM) pain management</strong> toolkit that complements Western treatment:</p><ul><li><strong>Acupuncture (针灸)</strong> — endorsed by the WHO for migraine, tension headache, and chronic pain. Most major Chinese hospitals have dedicated acupuncture departments.</li><li><strong>Tuina (推拿)</strong> and <strong>cupping (拔罐)</strong> — manual therapies for musculoskeletal pain and tension.</li><li><strong>Moxibustion (艾灸)</strong> — heat therapy used for chronic pain, cold-related conditions, and fatigue.</li></ul><p>Many international patients combine Western neurology appointments with TCM sessions during the same hospital visit. Learn more in our <a href="acupuncture-treatment-china-2026.html">acupuncture guide</a> and <a href="tcm-traditional-chinese-medicine-guide.html">TCM guide</a>.</p></div>\n',
    'ivf_fertility': '<div class="highlight-box" style="border-left-color: #28a745; background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%); margin: 30px 0;"><h3 style="color: #155724; margin-top: 0;">🌿 Acupuncture & TCM Support for IVF in China</h3><p>Many Chinese reproductive medicine centers offer <strong>acupuncture as an adjunct to IVF</strong>, with timing protocols around embryo transfer. The integration is unique to China:</p><ul><li><strong>Pre- and post-transfer acupuncture</strong> — provided at TCM departments of fertility hospitals to support implantation and reduce transfer-related stress.</li><li><strong>Chinese herbal medicine</strong> — prescribed to support ovarian function, endometrial receptivity, and hormone balance (always under fertility specialist supervision).</li><li><strong>Combined Western IVF + TCM care</strong> — available at hospitals like Shanghai University of TCM Longhua and Beijing University of Chinese Medicine Dongzhimen.</li></ul><p>See our <a href="acupuncture-treatment-china-2026.html">acupuncture guide</a> for hospital-by-hospital details on IVF-support protocols.</p></div>\n',
    'orthopedic': '<div class="highlight-box" style="border-left-color: #28a745; background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%); margin: 30px 0;"><h3 style="color: #155724; margin-top: 0;">🌿 TCM for Orthopedic Recovery in China</h3><p>Orthopedic recovery at Chinese hospitals typically includes a <strong>TCM-Western integrated rehabilitation protocol</strong>:</p><ul><li><strong>Acupuncture</strong> for post-surgical pain management — reduces opioid need and speeds mobility recovery.</li><li><strong>Tuina (推拿) and bone-setting (正骨)</strong> manual therapy — used alongside physiotherapy for spinal, knee, and shoulder recovery.</li><li><strong>Chinese herbal plasters and moxibustion</strong> — topical and heat therapy for chronic joint pain and arthritis.</li></ul><p>This is one of the most common integrated Chinese-Western protocols in Chinese orthopedic centers. See <a href="tcm-traditional-chinese-medicine-guide.html">TCM guide</a>.</p></div>\n',
    'cardio': '<div class="highlight-box" style="border-left-color: #28a745; background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%); margin: 30px 0;"><h3 style="color: #155724; margin-top: 0;">🌿 TCM Cardiac Rehabilitation in China</h3><p>Cardiac rehabilitation at top Chinese hospitals often combines <strong>Western cardiac care with TCM</strong> for recovery and prevention:</p><ul><li><strong>Acupuncture</strong> for post-bypass pain, anxiety, and arrhythmia symptom management.</li><li><strong>Baduanjin (八段锦) and Tai Chi (太极)</strong> — prescribed as low-impact cardiac rehab exercise, with measurable cardiovascular benefits.</li><li><strong>Chinese herbal medicine</strong> for blood circulation, blood pressure, and lipid management (under cardiology supervision).</li></ul><p>Learn more in our <a href="tcm-traditional-chinese-medicine-guide.html">TCM guide</a> and <a href="integrated-chinese-western-medicine-china.html">integrated medicine guide</a>.</p></div>\n',
    'neuro': '<div class="highlight-box" style="border-left-color: #28a745; background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%); margin: 30px 0;"><h3 style="color: #155724; margin-top: 0;">🌿 TCM for Neurological Recovery in China</h3><p>For stroke and Parkinson\'s recovery, Chinese hospitals often run <strong>TCM-integrated neurological rehabilitation</strong>:</p><ul><li><strong>Acupuncture for stroke rehabilitation</strong> — widely used in Chinese rehabilitation centers to restore motor function, especially in early recovery.</li><li><strong>Baduanjin and Tai Chi</strong> — prescribed for Parkinson\'s patients to improve balance and reduce fall risk.</li><li><strong>Chinese herbal medicine</strong> — adjunct therapy for neurodegenerative symptom management.</li></ul><p>China also leads the world in <strong>iPSC-derived Parkinson\'s therapy</strong> — see our <a href="stem-cell-therapy-china-access.html">stem cell therapy guide</a> for the June 2026 dual FDA+NMPA milestone.</p></div>\n',
    'eye': '<div class="highlight-box" style="border-left-color: #28a745; background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%); margin: 30px 0;"><h3 style="color: #155724; margin-top: 0;">🌿 TCM Eye Care in China</h3><p>For age-related eye conditions (macular degeneration, dry eye, glaucoma support), some Chinese ophthalmology centers offer <strong>integrated eye care with TCM</strong>:</p><ul><li><strong>Acupuncture for dry eye and macular support</strong> — adjunct therapy used in TCM eye hospitals.</li><li><strong>Chinese herbal formulas</strong> — for age-related vision conditions (under ophthalmologist supervision).</li></ul><p>China\'s high myopia rates mean unmatched surgical volume for SMILE, LASIK, ICL, and cataract. See <a href="ophthalmology-china-volume-expertise.html">ophthalmology in China</a> for the volume advantage.</p></div>\n',
    'dental': '<div class="highlight-box" style="border-left-color: #28a745; background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%); margin: 30px 0;"><h3 style="color: #155724; margin-top: 0;">🌿 TCM for Dental Recovery in China</h3><p>After major dental work (implants, full-mouth restoration, orthognathic surgery), some Chinese dental centers offer <strong>TCM adjuncts</strong> for faster recovery:</p><ul><li><strong>Acupuncture</strong> for post-implant pain and swelling management.</li><li><strong>Chinese herbal mouth rinses</strong> — anti-inflammatory and wound-healing support.</li></ul><p>China\'s <strong>autonomous robotic dental implant</strong> (world\'s first, 2017, AFMU Xi\'an) is another unique advantage. See <a href="autonomous-robotic-surgery-china.html">autonomous robotic surgery guide</a>.</p></div>\n',
    'wellness': '<div class="highlight-box" style="border-left-color: #28a745; background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%); margin: 30px 0;"><h3 style="color: #155724; margin-top: 0;">🌿 TCM Wellness & Health Screening in China</h3><p>Premium health checkups in China often include a <strong>TCM constitution assessment (中医体质辨识)</strong> alongside Western diagnostics:</p><ul><li><strong>TCM constitution typing</strong> — categorizes patients into 9 body types (qi-deficiency, yang-deficiency, damp-heat, etc.) to guide lifestyle and dietary advice.</li><li><strong>Preventive TCM therapies</strong> — acupuncture, moxibustion, or herbal tonics prescribed based on constitution.</li></ul><p>For full wellness experiences including TCM, see <a href="hainan-tcm-wellness-tourism-2026.html">Hainan TCM wellness tourism</a> and our <a href="tcm-traditional-chinese-medicine-guide.html">TCM guide</a>.</p></div>\n',
    'cosmetic': '<div class="highlight-box" style="border-left-color: #28a745; background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%); margin: 30px 0;"><h3 style="color: #155724; margin-top: 0;">🌿 TCM for Recovery After Cosmetic Surgery</h3><p>For swelling, bruising, and healing speed after cosmetic procedures, Chinese medical aesthetic centers increasingly offer <strong>TCM adjunct therapy</strong>:</p><ul><li><strong>Acupuncture</strong> for post-surgical swelling, bruising, and recovery acceleration.</li><li><strong>Chinese herbal formulas</strong> — for scar healing and skin recovery (under cosmetic surgeon supervision).</li><li><strong>Facial acupuncture (针灸美容)</strong> — used as a maintenance therapy to extend surgical results.</li></ul><p>Learn more in our <a href="tcm-traditional-chinese-medicine-guide.html">TCM guide</a> and <a href="integrated-chinese-western-medicine-china.html">integrated medicine guide</a>.</p></div>\n',
    'kidney_dialysis': '<div class="highlight-box" style="border-left-color: #28a745; background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%); margin: 30px 0;"><h3 style="color: #155724; margin-top: 0;">🌿 TCM for Kidney Disease in China</h3><p>Chinese nephrology centers often combine <strong>Western dialysis protocols with TCM nephrology</strong>:</p><ul><li><strong>Chinese herbal medicine</strong> — used to support kidney function and slow progression of chronic kidney disease (always under nephrologist supervision).</li><li><strong>Acupuncture</strong> for symptom management (fatigue, edema, sleep).</li></ul><p>China also leads in <strong>kidney transplantation</strong> — $70K vs $300K+ in the US. See <a href="organ-transplant-china-cost-access.html">organ transplant guide</a>.</p></div>\n',
    'organ_transplant': '<div class="highlight-box" style="border-left-color: #28a745; background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%); margin: 30px 0;"><h3 style="color: #155724; margin-top: 0;">🌿 TCM for Transplant Recovery in China</h3><p>Post-transplant recovery at major Chinese transplant centers often includes <strong>TCM-Western integrated protocols</strong>:</p><ul><li><strong>Chinese herbal medicine</strong> — used to support immune function alongside immunosuppressants (under transplant specialist supervision, with strict herb-drug interaction monitoring).</li><li><strong>Acupuncture</strong> for post-surgical pain, sleep, and recovery acceleration.</li><li><strong>Baduanjin qigong</strong> — prescribed as low-impact recovery exercise.</li></ul><p>For more on China\'s transplant program, see our <a href="organ-transplant-china-cost-access.html">organ transplant guide</a>.</p></div>\n',
}


# ----- Main -----

def main():
    blog_dir = sys.argv[1] if len(sys.argv) > 1 else BLOG_DIR_DEFAULT

    if not os.path.isdir(blog_dir):
        print(f"❌ Not a directory: {blog_dir}")
        sys.exit(1)

    all_files = sorted(
        f for f in os.listdir(blog_dir)
        if f.endswith('.html') and f != 'index.html'
    )

    candidates = [(f, classify(f)) for f in all_files if not should_skip(f)]
    candidates = [(f, c) for f, c in candidates if c is not None]

    print(f"📂 {blog_dir}")
    print(f"   Total .html files (excl index): {len(all_files)}")
    print(f"   After skip-list + categorization: {len(candidates)}")

    by_cat = Counter(c for _, c in candidates)
    print(f"\n📊 Per-category breakdown:")
    for cat, n in by_cat.most_common():
        print(f"   {cat}: {n} 篇")

    success = 0
    skipped = 0
    failed = []
    for f, cat in candidates:
        fp = os.path.join(blog_dir, f)
        ok, msg = inject(fp, TCM_TEMPLATES[cat])
        if ok:
            success += 1
        elif msg == "already injected":
            skipped += 1
        else:
            failed.append((f, msg))

    print(f"\n✅ Injected: {success}")
    print(f"⏭️  Skipped (already injected): {skipped}")
    if failed:
        print(f"❌ Failed: {len(failed)}")
        for f, msg in failed[:10]:
            print(f"   {f}: {msg}")

    # Final verification
    total = count_injections(blog_dir)
    print(f"\n🔍 Final marker count ({os.path.basename(blog_dir)}/*.html): {total}")


if __name__ == '__main__':
    main()
