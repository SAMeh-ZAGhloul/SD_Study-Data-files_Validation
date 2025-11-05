# SD Study Data Files Scanner and Analyzer

This repository contains a collection of Study Data (SD) files from clinical and nonclinical studies, along with a Jupyter notebook for scanning and analyzing these files.

## Overview

In the drug registration process, SD files refer to electronic data submissions containing structured datasets from nonclinical and clinical studies. These datasets follow standardized data models (CDISC standards) to allow regulatory agencies to efficiently review, validate, and analyze study results.

### Key Standards
- **SDTM** (Study Data Tabulation Model) - standardized structure for tabulated data
- **ADaM** (Analysis Data Model) - datasets for statistical analysis
- **SEND** (Standard for Exchange of Nonclinical Data) - for preclinical (animal) data

## Repository Contents

### Files
- `SD_Study-Data-files.ipynb` - Main Jupyter notebook for file scanning and analysis
- `SD_Study-Data-files.csv` - Generated summary table of analyzed files
- `SD_Study-Data-files.html` - HTML report (generated from notebook)
- `SD_Study-Data-files.pdf` - PDF documentation
- `sample_file_summary.xlsx` - Excel summary of files

### Validation Files
- `run_validation.py` - Python script for regulatory data validation
- `validation_README.md` - Detailed validation checklist and guidelines
- `validation_report.txt` - Latest validation report with pass/fail results
- `validation_results.csv` - Detailed validation results in CSV format
- `integrity_results.csv` - File integrity check results

### Data Files
- **Chemical Structure Files (.sdf)**: Molecular data files containing 3D structures, bonds, and properties
- **Clinical Datasets (.xpt)**: SAS XPORT files with study data (Demographics, Adverse Events, Lab Results)
- **ASN.1 Files (.asnt)**: Abstract Syntax Notation One files used in regulatory metadata
- **Other Files**: JSON, XML, PDF reports, and annotated CRFs

### Directory Structure
```
SD_Study-Data-files/
├── SD_Study-Data-files.ipynb
├── SD_Study-Data-files.csv
├── SD_Study-Data-files.html
├── SD_Study-Data-files.pdf
├── sample_file_summary.xlsx
├── run_validation.py
├── validation_README.md
├── validation_report.txt
├── validation_results.csv
├── integrity_results.csv
└── m5/
    └── 53-clin-stud-reports/
        └── study1234/
            └── datasets/
                ├── ae.csv / ae.xpt (Adverse Events)
                ├── dm.csv / dm.xpt (Demographics)
                ├── lb.csv / lb.xpt (Lab Results)
                ├── compound.sdf (Chemical structures)
                ├── *.asnt (ASN.1 metadata)
                ├── define.xml (Data definitions)
                └── *.pdf (Reports and CRFs)
```

## Requirements

To run the analysis notebook, install the following Python packages:

```bash
pip install rdkit-pypi pandas biopython pyreadstat
```

### Dependencies
- **RDKit**: For chemical structure analysis (.sdf files)
- **pandas**: Data manipulation and analysis
- **Biopython**: For ASN.1 and bioinformatics data
- **pyreadstat**: For reading SAS XPORT files (.xpt)

## Usage

1. Open `SD_Study-Data-files.ipynb` in Jupyter Notebook or JupyterLab
2. Run the cells sequentially to:
   - Scan the directory for files
   - Analyze .sdf files (molecular structures)
   - Analyze .xpt files (clinical datasets)
   - Analyze .asnt files (metadata)
   - Generate comprehensive summary table
3. The notebook will automatically save results to `SD_Study-Data-files.csv`

## Analysis Features

### SDF Files (.sdf)
- Molecular structure parsing
- Property extraction (molecular weight, atom/bond counts)
- SMILES generation
- Chemical descriptor calculation

### XPT Files (.xpt)
- Clinical data reading (SDTM format)
- Dataset structure analysis
- Statistical summaries
- Data preview and validation

### ASNT Files (.asnt)
- ASN.1 parsing
- XML metadata extraction
- Regulatory information parsing
- Study assessment data

## Validation

This repository includes comprehensive validation tools for regulatory data files to ensure compliance with FDA, EMA, and ICH eCTD technical specifications.

### Validation Requirements

Additional dependencies for validation:

```bash
pip install chardet
```

### Validation Checks Performed

#### SAS XPORT (.xpt) Files
- **Format Check**: Verifies Version 5 XPORT format
- **CDISC Compliance**: Ensures conformance to SDTM/ADaM domains
- **Required Variables**: Checks for mandatory variables (STUDYID, USUBJID, --SEQ)
- **Data Integrity**: Validates no null values in required fields

#### Structure Data Files (.sdf)
- **Structure Check**: Validates SDF format with proper molecule separators ($$$$)
- **Molecule Count**: Ensures valid molecules are present
- **Property Blocks**: Checks for required property data (> tags)
- **Connectivity**: Validates atom/bond connectivity using RDKit

#### ASN.1 Text (.asnt) Files
- **ASN.1 Structure**: Validates ASN.1 syntax and XML structure
- **Encoding**: Checks UTF-8/ASCII encoding compliance
- **Schema Compliance**: Verifies against regulatory schemas
- **Mandatory Fields**: Ensures required metadata fields are present

#### File Integrity Checks
- **File Size**: Validates files are within FDA eCTD limits (< 100MB)
- **File Existence**: Confirms all required files are present
- **Readability**: Ensures files can be opened and read

### Running Validations

Execute the validation script:

```bash
python run_validation.py
```

This will:
1. Scan the directory for .xpt, .sdf, and .asnt files
2. Perform comprehensive validation checks
3. Generate validation report and CSV results
4. Display summary statistics and detailed findings

### Validation Results Summary

**Latest Validation Report** (as of 2025-11-05):
- **Total Files Validated**: 9
- **PASS**: 30
- **FAIL**: 6
- **WARN**: 0
- **ERROR**: 0
- **Overall Compliance**: REVIEW REQUIRED

#### Key Findings:
- **XPT Files**: Format check failures (not XPORT format) for lb.xpt, ae.xpt, dm.xpt
- **SDF Files**: Invalid structure in compound.sdf, but valid structures in Structure2D and Conformer3D files
- **ASNT Files**: All ASN.1 structure validations passed, but assessment.asnt missing mandatory fields (StudyID, Reviewer, AssessmentDate)
- **File Integrity**: All files pass integrity checks (size, existence, readability)

## Pinnacle 21 Validation Results

Pinnacle 21 Community Validator (v4.1.0) was used to validate the XPT files against SDTM IG 3.4 (FDA) standards. The validator checks for compliance with CDISC SDTM standards, including required variables, data types, controlled terminology, and cross-domain relationships.

### Configuration Details
- **SDTM IG Version**: 3.4 (FDA)
- **CDISC SDTM CT Version**: 2025-09-26
- **UNII Version**: 2025-07-02
- **MED-RT Version**: 2025-09-02
- **Validation Engine**: FDA 2405.2
- **Define.xml**: Not provided (marked as missing in all reports)

**Note**: MedDRA and SNOMED dictionaries are not configured in the Community version, so adverse event coding and trial indication checks are not executed.

### Summary of Findings

#### Overall Issues
- **Missing define.xml**: All validations flagged missing define.xml file (DD0101 - Reject)
- **Missing Trial Summary (TS) domain**: Required for all submissions (SD1115 - Reject)
- **Missing other domains**: AE, LB, VS, EX, DS, SE, TA, TE domains flagged as missing
- **No rejects in processed domains**: The 3 XPT files processed without data rejects (0 rejects each)

#### AE Domain (ae.xpt) - Adverse Events
- **Records Processed**: 2
- **Major Issues**:
  - Missing required SDTM variables: AEDECOD, AESEQ, DOMAIN
  - Missing expected variables: AEACN, AEBDSYCD, AEBODSYS, AEENDTC, AEHLGT, AEHLGTCD, AEHLT, AEHLTCD, AELLT, AELLTCD, AEPTCD, AESER, AESOC, AESOCCD, AESTDTC
  - Missing regulatory expected variable: EPOCH
  - No timing variables present (SD1299)
- **Total Issues**: 20 metadata issues

#### DM Domain (dm.xpt) - Demographics
- **Records Processed**: 2
- **Major Issues**:
  - Missing required SDTM variables: COUNTRY, DOMAIN, SITEID, SUBJID
  - Missing expected variables: ACTARM, ACTARMCD, ACTARMUD, AGEU, ARM, ARMCD, ARMNRS, DTHDTC, DTHFL, RACE, RFENDTC, RFICDTC, RFPENDTC, RFSTDTC, RFXENDTC, RFXSTDTC
- **Total Issues**: 20 metadata issues

#### LB Domain (lb.xpt) - Laboratory Test Results
- **Records Processed**: 2
- **Major Issues**:
  - Missing required SDTM variables: DOMAIN, LBSEQ, LBTESTCD
  - Missing expected variables: LBCAT, LBDTC, LBLOBXFL, LBNRIND, LBORNRHI, LBORNRLO, LBORRES, LBORRESU, LBSTNRHI, LBSTNRLO, LBSTRESC, VISITNUM
  - Missing regulatory expected variable: EPOCH
  - No timing variables present (SD1299)
- **Total Issues**: 17 metadata issues

### Comparison with Python Validation

| Aspect | Python Validation | Pinnacle 21 Validation |
|--------|------------------|----------------------|
| **Format Check** | Fails - Files not in XPORT format | Not applicable - Assumes valid XPT structure |
| **SDTM Compliance** | Not checked | Comprehensive SDTM IG 3.4 validation |
| **Variable Presence** | Basic file readability | Detailed required/expected variable checks |
| **Domain Relationships** | Not checked | Cross-domain consistency validation |
| **Controlled Terminology** | Not checked | CT validation (limited by missing dictionaries) |
| **Metadata Validation** | Basic | Requires define.xml for full compliance |
| **Focus** | File integrity and basic structure | Regulatory submission readiness |

### Recommendations

1. **Convert to XPORT Format**: Address Python validation failures by ensuring files are in proper SAS XPORT v5 format
2. **Add Missing Variables**: Populate required SDTM variables in each domain
3. **Create define.xml**: Essential for regulatory submissions to define variable metadata
4. **Add Missing Domains**: Include TS, AE, LB, VS, EX, DS, SE, TA, TE domains as appropriate
5. **Configure Dictionaries**: For full validation, configure MedDRA and SNOMED in Pinnacle 21
6. **Timing Variables**: Ensure EPOCH and other timing variables are populated
7. **Cross-domain Consistency**: Validate relationships between domains (e.g., USUBJID consistency)

### Validation Output Files

- `validation_report.txt` - Human-readable validation report
- `validation_results.csv` - Detailed validation results for analysis
- `integrity_results.csv` - File integrity check results

### Validation Guidelines

For detailed validation checklists and regulatory requirements, see:
- `validation_README.md` - Comprehensive validation guidelines
- FDA eCTD Technical Specifications
- CDISC validation rules
- ICH guidelines for electronic submissions

## Output

The analysis generates a comprehensive CSV file (`SD_Study-Data-files.csv`) containing:
- File metadata
- Detailed analysis results for each file type
- Molecular properties (for .sdf)
- Dataset summaries (for .xpt)
- Metadata extraction (for .asnt)

## Data Sources

The data files in this repository are from:
- Clinical study reports (study1234)
- Chemical compound databases
- Regulatory submission datasets
- Nonclinical study data

## Notes

This repository contains sample data for educational and analysis purposes. For actual regulatory submissions, consult appropriate CDISC guidelines and regulatory requirements.
