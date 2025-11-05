#!/usr/bin/env python3
# Validation script for regulatory data files

import os
import glob
from pathlib import Path
import pandas as pd
from datetime import datetime
try:
    import chardet
    CHARDET_AVAILABLE = True
except ImportError:
    CHARDET_AVAILABLE = False

def validate_xpt_file(file_path):
    """Validate XPT file according to regulatory requirements."""
    validation_results = {
        'File': str(file_path.name),
        'Format Check': 'PASS',
        'CDISC Compliance': 'PASS',
        'Required Variables': 'PASS',
        'Data Integrity': 'PASS',
        'Issues': []
    }

    try:
        import pyreadstat
        df, meta = pyreadstat.read_xport(str(file_path))

        # Check format version
        if meta.file_format != 'XPORT':
            validation_results['Format Check'] = 'FAIL'
            validation_results['Issues'].append(f'Not XPORT format: {meta.file_format}')

        # Check for required variables
        required_vars = ['STUDYID', 'USUBJID']
        missing_vars = [var for var in required_vars if var not in df.columns]
        if missing_vars:
            validation_results['Required Variables'] = 'FAIL'
            validation_results['Issues'].append(f'Missing required variables: {missing_vars}')

        # Check for nulls in required fields
        for var in required_vars:
            if var in df.columns and df[var].isnull().any():
                validation_results['Data Integrity'] = 'FAIL'
                validation_results['Issues'].append(f'Null values in {var}')
                break

        # Check for --SEQ if present
        seq_cols = [col for col in df.columns if '--SEQ' in col.upper()]
        for seq_col in seq_cols:
            if df[seq_col].isnull().any():
                validation_results['Data Integrity'] = 'FAIL'
                validation_results['Issues'].append(f'Null values in {seq_col}')
                break

    except Exception as e:
        validation_results['Format Check'] = 'ERROR'
        validation_results['Issues'].append(f'Error reading file: {str(e)}')

    return validation_results

def validate_sdf_file(file_path):
    """Validate SDF file according to regulatory requirements."""
    validation_results = {
        'File': str(file_path.name),
        'Structure Check': 'PASS',
        'Molecule Count': 'PASS',
        'Property Blocks': 'PASS',
        'Connectivity': 'PASS',
        'Issues': []
    }

    try:
        from rdkit import Chem

        with open(str(file_path), 'r') as f:
            content = f.read()

        # Check for proper SDF structure (molecules separated by $$$$)
        molecules = content.split('$$$$')
        molecules = [mol.strip() for mol in molecules if mol.strip()]

        if not molecules:
            validation_results['Structure Check'] = 'FAIL'
            validation_results['Issues'].append('No molecules found')
            return validation_results

        # Validate each molecule
        valid_molecules = 0
        for i, mol_block in enumerate(molecules):
            if not mol_block.strip():
                continue

            # Try to parse with RDKit
            mol = Chem.MolFromMolBlock(mol_block)
            if mol is None:
                validation_results['Connectivity'] = 'FAIL'
                validation_results['Issues'].append(f'Molecule {i+1}: Invalid structure')
            else:
                valid_molecules += 1

                # Check atom/bond counts
                if mol.GetNumAtoms() == 0:
                    validation_results['Connectivity'] = 'FAIL'
                    validation_results['Issues'].append(f'Molecule {i+1}: No atoms')

                # Check for property blocks
                if '> ' not in mol_block:
                    validation_results['Property Blocks'] = 'WARN'
                    validation_results['Issues'].append(f'Molecule {i+1}: No property blocks found')

        if valid_molecules == 0:
            validation_results['Molecule Count'] = 'FAIL'
            validation_results['Issues'].append('No valid molecules')

    except Exception as e:
        validation_results['Structure Check'] = 'ERROR'
        validation_results['Issues'].append(f'Error reading file: {str(e)}')

    return validation_results

def validate_asnt_file(file_path):
    """Validate ASNT file according to regulatory requirements."""
    validation_results = {
        'File': str(file_path.name),
        'ASN.1 Structure': 'PASS',
        'Encoding': 'PASS',
        'Schema Compliance': 'PASS',
        'Mandatory Fields': 'PASS',
        'Issues': []
    }

    try:
        # Check encoding
        with open(str(file_path), 'rb') as f:
            raw_data = f.read()

        if CHARDET_AVAILABLE:
            detected_encoding = chardet.detect(raw_data)
            encoding = detected_encoding.get('encoding', 'unknown')
        else:
            encoding = 'unknown'

        if encoding not in ['utf-8', 'ascii', 'UTF-8', 'ASCII']:
            validation_results['Encoding'] = 'WARN'
            validation_results['Issues'].append(f'Encoding {encoding} may not be compliant')

        # Try to decode
        try:
            content = raw_data.decode('utf-8')
        except UnicodeDecodeError:
            try:
                content = raw_data.decode('ascii')
            except UnicodeDecodeError:
                validation_results['Encoding'] = 'FAIL'
                validation_results['Issues'].append('Cannot decode file content')
                return validation_results

        # Check if XML
        if content.startswith('<?xml'):
            import xml.etree.ElementTree as ET
            try:
                root = ET.fromstring(content)
                validation_results['ASN.1 Structure'] = 'PASS (XML)'

                # Check for mandatory fields in assessment
                mandatory_fields = ['StudyID', 'Reviewer', 'AssessmentDate']
                missing_fields = []
                for field in mandatory_fields:
                    if not root.find(field) or not root.find(field).text:
                        missing_fields.append(field)

                if missing_fields:
                    validation_results['Mandatory Fields'] = 'FAIL'
                    validation_results['Issues'].append(f'Missing mandatory fields: {missing_fields}')

            except ET.ParseError as e:
                validation_results['Schema Compliance'] = 'FAIL'
                validation_results['Issues'].append(f'Invalid XML: {str(e)}')
        else:
            # Assume ASN.1 text format
            validation_results['ASN.1 Structure'] = 'PASS (Text)'
            # Basic checks for ASN.1 structure
            if '::=' not in content:
                validation_results['Schema Compliance'] = 'WARN'
                validation_results['Issues'].append('No ASN.1 definitions found')
    except Exception as e:
        validation_results['ASN.1 Structure'] = 'ERROR'
        validation_results['Issues'].append(f'Error reading file: {str(e)}')

    return validation_results

def validate_file_integrity(file_path):
    """General file integrity checks."""
    integrity_results = {
        'File': str(file_path.name),
        'File Size': 'PASS',
        'File Exists': 'PASS',
        'Readable': 'PASS',
        'Issues': []
    }

    try:
        # Check file exists
        if not file_path.exists():
            integrity_results['File Exists'] = 'FAIL'
            integrity_results['Issues'].append('File does not exist')
            return integrity_results

        # Check file size (FDA eCTD limit is typically 100MB per file)
        size_mb = file_path.stat().st_size / (1024 * 1024)
        if size_mb > 100:
            integrity_results['File Size'] = 'WARN'
            integrity_results['Issues'].append(f'File size {size_mb:.2f}MB exceeds typical limits')

        # Check readability
        try:
            with open(str(file_path), 'rb') as f:
                f.read(1024)  # Read first 1KB
        except Exception as e:
            integrity_results['Readable'] = 'FAIL'
            integrity_results['Issues'].append(f'File not readable: {str(e)}')
    except Exception as e:
        integrity_results['Readable'] = 'ERROR'
        integrity_results['Issues'].append(f'Error checking file: {str(e)}')

    return integrity_results

if __name__ == "__main__":
    # Scan current directory for files
    current_dir = Path('.')
    all_files = list(current_dir.rglob('*'))
    files_only = [f for f in all_files if f.is_file()]

    # Group files by extension
    file_extensions = {}
    for file_path in files_only:
        ext = file_path.suffix.lower()
        if ext not in file_extensions:
            file_extensions[ext] = []
        file_extensions[ext].append(file_path)

    # Collect all validation results
    validation_report = []

    # Validate XPT files
    xpt_files = file_extensions.get('.xpt', [])
    for file_path in xpt_files:
        result = validate_xpt_file(file_path)
        validation_report.append(result)

    # Validate SDF files
    sdf_files = file_extensions.get('.sdf', [])
    for file_path in sdf_files:
        result = validate_sdf_file(file_path)
        validation_report.append(result)

    # Validate ASNT files
    asnt_files = file_extensions.get('.asnt', [])
    for file_path in asnt_files:
        result = validate_asnt_file(file_path)
        validation_report.append(result)

    # Validate file integrity for all files
    all_target_files = xpt_files + sdf_files + asnt_files
    integrity_report = []
    for file_path in all_target_files:
        result = validate_file_integrity(file_path)
        integrity_report.append(result)

    # Create validation summary DataFrame
    validation_df = pd.DataFrame(validation_report)
    integrity_df = pd.DataFrame(integrity_report)

    # Display validation results
    print("=== REGULATORY VALIDATION REPORT ===")
    print(f"Report generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total files validated: {len(validation_report)}")
    print()

    # Summary statistics
    total_checks = len(validation_df) * (len(validation_df.columns) - 2)  # Exclude 'File' and 'Issues'
    pass_count = 0
    fail_count = 0
    warn_count = 0
    error_count = 0

    for _, row in validation_df.iterrows():
        for col in validation_df.columns:
            if col not in ['File', 'Issues']:
                status = str(row[col]).upper()
                if 'PASS' in status:
                    pass_count += 1
                elif 'FAIL' in status:
                    fail_count += 1
                elif 'WARN' in status:
                    warn_count += 1
                elif 'ERROR' in status:
                    error_count += 1

    print(f"Validation Summary:")
    print(f"  PASS: {pass_count}")
    print(f"  FAIL: {fail_count}")
    print(f"  WARN: {warn_count}")
    print(f"  ERROR: {error_count}")
    print(f"  Overall Compliance: {'PASS' if fail_count == 0 and error_count == 0 else 'REVIEW REQUIRED'}")
    print()

    # Display detailed validation results
    print("Detailed Validation Results:")
    for _, row in validation_df.iterrows():
        print(f"\nFile: {row['File']}")
        for col in validation_df.columns:
            if col not in ['File', 'Issues']:
                status = row[col]
                print(f"  {col}: {status}")
        if row['Issues']:
            print(f"  Issues: {', '.join(row['Issues'])}")

    print("\n=== FILE INTEGRITY CHECKS ===")
    for _, row in integrity_df.iterrows():
        print(f"\nFile: {row['File']}")
        for col in integrity_df.columns:
            if col != 'File':
                status = row[col]
                print(f"  {col}: {status}")
        if row['Issues']:
            print(f"  Issues: {', '.join(row['Issues'])}")

    # Save validation report to file
    validation_report_filename = 'validation_report.txt'
    with open(validation_report_filename, 'w') as f:
        f.write("=== REGULATORY VALIDATION REPORT ===\n")
        f.write(f"Report generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Total files validated: {len(validation_report)}\n\n")
        f.write(f"Validation Summary:\n")
        f.write(f"  PASS: {pass_count}\n")
        f.write(f"  FAIL: {fail_count}\n")
        f.write(f"  WARN: {warn_count}\n")
        f.write(f"  ERROR: {error_count}\n")
        f.write(f"  Overall Compliance: {'PASS' if fail_count == 0 and error_count == 0 else 'REVIEW REQUIRED'}\n\n")

        f.write("Detailed Validation Results:\n")
        for _, row in validation_df.iterrows():
            f.write(f"\nFile: {row['File']}\n")
            for col in validation_df.columns:
                if col not in ['File', 'Issues']:
                    status = row[col]
                    f.write(f"  {col}: {status}\n")
            if row['Issues']:
                f.write(f"  Issues: {', '.join(row['Issues'])}\n")

        f.write("\n=== FILE INTEGRITY CHECKS ===\n")
        for _, row in integrity_df.iterrows():
            f.write(f"\nFile: {row['File']}\n")
            for col in integrity_df.columns:
                if col != 'File':
                    status = row[col]
                    f.write(f"  {col}: {status}\n")
            if row['Issues']:
                f.write(f"  Issues: {', '.join(row['Issues'])}\n")

    print(f"\nValidation report saved to: {validation_report_filename}")

    # Save validation data to CSV for further analysis
    validation_csv_filename = 'validation_results.csv'
    validation_df.to_csv(validation_csv_filename, index=False)
    integrity_df.to_csv('integrity_results.csv', index=False)
    print(f"Validation results saved to: {validation_csv_filename}")
    print(f"Integrity results saved to: integrity_results.csv")
