
# 🧪 Regulatory Data Validation Checklist

This document provides a detailed checklist for validating `.xpt`, `.sdf`, and `.asnt` files before regulatory submission.  
It ensures **completeness, integrity, and compliance** with **FDA**, **EMA**, and **ICH eCTD** technical specifications.

---

## 🧾 1. SAS XPORT (.xpt) — Clinical Study Datasets

### ✅ Structural & Format Checks
- Confirm file is in **Version 5 XPORT format**.
- Verify datasets conform to **CDISC SDTM or ADaM domains**.
- Ensure all variables have:
  - Correct labels and formats.
  - Expected variable names per the define.xml.
- Check that `--SEQ`, `USUBJID`, and `STUDYID` are unique and non-null.

### 🧰 Validation Tools
```bash
pip install pyreadstat pandas
python -c "import pyreadstat; df, meta = pyreadstat.read_xport('dm.xpt'); print(meta.file_format)"
```

Or use **Pinnacle 21 Community** for CDISC validation (FDA-recommended).

### ⚠️ Common Issues
- Missing define.xml or domain metadata.
- Non-standard variable naming.
- Encoding errors in variable labels.

---

## ⚗️ 2. Structure Data Files (.sdf) — Chemical Compounds

### ✅ Structural Checks
- Each molecule must start with a header and end with `$$$$`.
- Validate 2D/3D coordinates, atom, and bond count consistency.
- Verify property blocks (e.g., `>  <PUBCHEM_COMPOUND_CID>`) are well-formed.

### 🧰 Validation Tools
```bash
pip install rdkit
python -m rdkit.Chem.SDWriter compound.sdf
```

Or use **Open Babel**:
```bash
obabel compound.sdf -O check.mol -v
```

### ⚠️ Common Issues
- Missing `$$$$` terminator.
- Invalid atom/bond connectivity.
- Corrupted or non-SDF ASCII encoding.

---

## 📜 3. ASN.1 Text (.asnt) — Regulatory Metadata

### ✅ Structural Checks
- Must follow **Abstract Syntax Notation One (ASN.1)** structure.
- Ensure character encoding is UTF-8 or ASCII.
- Validate against schema (if available).

### 🧰 Validation Tools
```bash
pip install pyasn1
python -c "from pyasn1.codec.der.decoder import decode; open('assessment.asnt','rb').read()"
```

Or use **asn1tools** to validate against specification:
```bash
asn1tools compile spec.asn --decode assessment.asnt
```

### ⚠️ Common Issues
- Schema mismatch or invalid OID.
- Missing mandatory objects or field values.
- Encoding issues.

---

## 🧮 4. General Submission Integrity Checks

| Category | Validation Item | Tool/Method |
|-----------|-----------------|--------------|
| File Presence | All required domains exist | Manual or script check |
| Define.xml | Valid XML schema | XML validator |
| Metadata Sync | define.xml variables = dataset variables | Pinnacle 21 |
| Data Integrity | No nulls in required fields | pandas check |
| File Size | Each file < FDA eCTD limits | OS file check |
| Encoding | UTF-8 for text-based files | chardet or file utility |

---

## ⚙️ 5. Recommended Folder Structure
```
m5/
 └── 53-clin-stud-reports/
     └── study1234/
         ├── datasets/
         │   ├── dm.xpt
         │   ├── ae.xpt
         │   ├── lb.xpt
         │   └── define.xml
         ├── compound.sdf
         ├── assessment.asnt
         └── validation_README.md
```

---

## 🧩 Final Checklist Before Submission
- [ ] All `.xpt` files validated via Pinnacle 21.
- [ ] `define.xml` references verified.
- [ ] Chemical structures validated via RDKit or Open Babel.
- [ ] ASN.1 structure validated for correctness.
- [ ] Folder structure matches eCTD module layout.
- [ ] All files named and dated according to submission guidelines.

---

**Prepared for internal use in QA and Regulatory Data Management workflows.**  
© 2025 — Drug Data Validation Reference Package
