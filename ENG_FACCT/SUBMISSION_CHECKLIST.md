# FAccT 2026 Submission Checklist

**Paper:** DeepBridge Fairness: From Research to Regulation
**Deadline:** January 13, 2026 (Abstract: January 8, 2026)

---

## 🔴 CRITICAL ITEMS (Must Complete Before Submission)

### Page Limit
- [ ] **Paper is ≤14 pages** (excluding references)
  - Current: ~34 pages (NEEDS CONDENSING)
  - Action required: Reduce content by ~20 pages
  - References have no limit

### Anonymization (Double-Blind Review)
- [x] Template configured with `anonymous` option
- [x] Author names removed from main.tex
- [x] Affiliations removed
- [x] GitHub URLs anonymized
- [x] Documentation URLs anonymized
- [ ] Verify no self-citations reveal identity
- [ ] Remove PDF metadata: `make strip-metadata`
- [ ] Manual check: search PDF for "Gustavo", "Paulo", "Haase", "Silva", "Banco do Brasil"

---

## 🟡 IMPORTANT ITEMS

### LaTeX Template
- [x] Using `\documentclass[manuscript, review, anonymous]{acmart}`
- [x] Bibliography style: `ACM-Reference-Format`
- [x] Line numbers enabled (review mode)
- [x] Single column format (manuscript mode)
- [x] Copyright info removed for submission
- [x] Conference info cleared

### Required Sections
- [x] Abstract included (before \maketitle)
- [x] CCS Concepts included and valid
- [x] Keywords included (8 keywords)
- [ ] All sections complete (Introduction through Conclusion)

### Bibliography
- [x] Using ACM-Reference-Format.bst
- [ ] Fix 32 BibTeX warnings
  - Missing volume/number fields
  - Missing publisher/address
  - Missing page numbers
- [ ] All citations have complete entries
- [ ] No broken citation keys

---

## 🟢 RECOMMENDED ITEMS

### Content Quality
- [ ] Abstract is compelling and concise (~300 words max)
- [ ] Introduction clearly states contributions
- [ ] Related Work distinguishes from existing tools
- [ ] Methodology is clear and reproducible
- [ ] Results support all claims
- [ ] Discussion addresses limitations
- [ ] Conclusion summarizes impact

### Figures and Tables
- [ ] All figures are referenced in text
- [ ] All figures are legible (readable when printed)
- [ ] All tables use `booktabs` package
- [ ] Captions are descriptive and standalone
- [ ] No identifying information in figures

### Code Listings
- [ ] Code examples are properly formatted
- [ ] Syntax highlighting works correctly
- [ ] Examples support the narrative

### Writing Quality
- [ ] Spell check completed
- [ ] Grammar check completed
- [ ] Consistent terminology throughout
- [ ] No overly strong claims without evidence
- [ ] Professional tone maintained

---

## 📋 Pre-Submission Technical Checks

### Compilation
```bash
# Full compilation
make full

# Expected output: PDF with 14 pages + references
make info
```

- [ ] Compiles without errors
- [ ] Bibliography generates correctly
- [ ] All references appear in text
- [ ] Cross-references work (\ref, \cite)

### Anonymization Verification
```bash
# Check for identifying info
make anonymize

# Expected: No author names, no direct GitHub links
```

- [ ] No author names in .tex files
- [ ] No identifying URLs
- [ ] No acknowledgments section
- [ ] No funding information

### PDF Metadata
```bash
# Check metadata
pdfinfo main.pdf

# Remove if needed
make strip-metadata
```

- [ ] Author field is empty
- [ ] No identifying creator information
- [ ] Title is appropriate

---

## 📤 Submission Process

### Before Submission

1. **Condensation Phase** (Highest Priority)
   - [ ] Review each section for redundancy
   - [ ] Move technical details to appendix
   - [ ] Consolidate results tables
   - [ ] Reduce figure sizes if possible
   - [ ] Target: 14 pages of content

2. **Final Review**
   - [ ] Read entire paper start to finish
   - [ ] Check all claims are supported
   - [ ] Verify figures match descriptions
   - [ ] Check table data is accurate

3. **Technical Verification**
   - [ ] `make full` completes successfully
   - [ ] `make check` shows no critical errors
   - [ ] `make anonymize` finds no identifying info
   - [ ] `make info` confirms ≤14 pages

4. **Archive Creation**
   - [ ] `make archive` to create submission package
   - [ ] Verify archive contains all necessary files
   - [ ] Test compilation from archive

### Submission Day (January 13, 2026)

1. **Upload to OpenReview**
   - [ ] Create/login to OpenReview account
   - [ ] Navigate to FAccT 2026 submission portal
   - [ ] Upload main PDF
   - [ ] Upload source files (.tar.gz from `make archive`)

2. **Metadata Entry**
   - [ ] Enter title exactly as in paper
   - [ ] Enter abstract (copy from .tex)
   - [ ] Enter keywords
   - [ ] Select subject areas (match CCS concepts)

3. **Supplementary Materials** (Optional)
   - [ ] Additional experiments
   - [ ] Extended results tables
   - [ ] Code examples
   - [ ] Video demonstration

4. **Final Checks**
   - [ ] PDF renders correctly in browser
   - [ ] All fields are complete
   - [ ] No identifying information visible
   - [ ] Submission confirmation received

---

## 🔧 Quick Commands Reference

```bash
# Compile paper
make full

# Check status
make info

# Verify anonymization
make anonymize

# Remove metadata
make strip-metadata

# Check for errors
make check

# Create submission archive
make archive

# Clean auxiliary files
make clean
```

---

## 📞 Emergency Contacts

- **Template Issues:** acmtexsupport@aptaracorp.com
- **Submission Portal:** program-chairs@facctconference.org
- **General Questions:** https://facctconference.org/2026/faq.html

---

## 📊 Current Status

| Item | Status | Priority |
|------|--------|----------|
| Template configured | ✅ Done | Critical |
| Translation complete | ✅ Done | Critical |
| Anonymization | ✅ Done | Critical |
| **Page limit (14 pages)** | ❌ **34 pages** | **🔴 CRITICAL** |
| Bibliography warnings | ⚠️ 32 warnings | Important |
| Final review | ⏳ Pending | Important |
| Archive creation | ⏳ Pending | Important |

---

## ⏰ Timeline to Deadline

**Days remaining until January 13, 2026:**
- Abstract deadline: January 8 (5 days before paper)
- Paper deadline: January 13

**Recommended schedule:**
- **Week 1-2 (Now):** Condense to 14 pages, fix bibliography
- **Week 3:** Final review, anonymization check
- **Week 4:** Create archive, test submission
- **Jan 8:** Submit abstract
- **Jan 13:** Submit full paper

---

**Last updated:** December 8, 2025
**Next action:** CONDENSE PAPER TO 14 PAGES (currently 34 pages)
