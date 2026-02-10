import pandas as pd
import re

def clean_package_name(name):
    """
    Cleans a single package name by removing versions, suffixes, and special characters.
    """
    if pd.isna(name) or name is None:
        return name
    
    # 1. Basic normalization
    name = str(name).strip().lower()
    
    # 2. Remove versions in parentheses, e.g., "pandas (2.0.1)" -> "pandas"
    name = re.sub(r'\s*\([^)]*\)\s*$', '', name)
    
    # 3. Remove version numbers and revisions, e.g., "lib-v1.2" -> "lib"
    # Matches patterns like -1.0, .v2, _rev3
    version_pattern = r'[-_.](?:v?\d[\w.\-!,+]*|r\d+|rev\d+)$'
    name = re.sub(version_pattern, '', name)
    
    # 4. Remove development suffixes (alpha, beta, rc, dev, etc.)
    qualifier_pattern = r'[-_.](?:dev|devel|alpha|beta|rc|pre|post|final|snapshot|nightly|unreleased|unofficial|master)$'
    name = re.sub(qualifier_pattern, '', name)
    
    # 5. Clean up trailing special characters
    name = re.sub(r'[-_.]+$', '', name)
    
    # 6. Remove redundant naming like "package-package"
    name = re.sub(r'^([a-z0-9._-]+)-\1$', r'\1', name)
    
    return name

def standardize_and_clean(file_path, year):
    """
    Main function to unify 2016 and 2025 formats.
    """
    # 1. Load Data based on year schema
    if year == "2016":
        df = pd.read_csv(file_path)
        # Use the specific columns from your 2016 sample
        df = df[['package_name', 'requirement']]
    
    elif year == "2025":
        # Handle the extra comma/index if present
        df = pd.read_csv(file_path, index_col=0 if ',' in open(file_path, 'r').read(10) else None)
        # Map 2025 'package' to 'package_name' to match 2016
        df = df.rename(columns={'package': 'package_name'})
        df = df[['package_name', 'requirement']]
    
    else:
        raise ValueError(f"Year {year} is not supported in standardize_and_clean")

    # 2. Apply the cleaning helper - now correctly applies to individual strings
    df['package_name'] = df['package_name'].apply(clean_package_name)
    df['requirement'] = df['requirement'].apply(clean_package_name)
    
    # 3. Final polish: Remove rows that became empty or NaN after cleaning
    df = df.dropna(subset=['package_name', 'requirement'])
    
    # Remove self-loops (where a package depends on itself)
    df = df[df['package_name'] != df['requirement']]
    
    return df