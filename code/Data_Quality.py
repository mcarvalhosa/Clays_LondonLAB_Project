import pandas as pd
import numpy as np
from datetime import datetime

def analyze_data_quality(file_path):
    """
    Perform comprehensive data quality checks on the booking dataset.
    
    Parameters:
    -----------
    file_path : str
        Path to the CSV file containing the booking data.
    
    Returns:
    --------
    None
        Prints analysis results to the console.
    """
    print("=" * 80)
    print("BOOKING DATA QUALITY ANALYSIS")
    print("=" * 80)
    
    # Load the dataset
    try:
        df = pd.read_csv(file_path)
        print(f"\nSuccessfully loaded dataset with {df.shape[0]} rows and {df.shape[1]} columns.")
    except Exception as e:
        print(f"Error loading file: {str(e)}")
        return
    
    # 1. Basic Information
    print("\n" + "=" * 40)
    print("1. BASIC DATASET INFORMATION")
    print("=" * 40)
    print(f"Number of records: {df.shape[0]}")
    print(f"Number of columns: {df.shape[1]}")
    
    # 2. Data Types Analysis
    print("\n" + "=" * 40)
    print("2. DATA TYPES ANALYSIS")
    print("=" * 40)
    
    # Print data types for each column
    dtypes = pd.DataFrame(df.dtypes, columns=['Data Type'])
    dtypes.index.name = 'Column Name'
    print("\nColumn data types:")
    print(dtypes.to_string())
    
    # Check for columns that might have incorrect data types
    date_columns = [col for col in df.columns if any(keyword in col.lower() for keyword in ['date', 'time', 'at'])]
    numeric_columns = [col for col in df.columns if any(keyword in col.lower() for keyword in ['cost', 'charge', 'price', 'amount', 'size', 'days'])]
    boolean_columns = [col for col in df.columns if any(keyword in col.lower() for keyword in ['is', 'was', 'has', 'available', 'completed', 'selected', 'required', 'applied'])]
    
    # Report potential data type issues
    print("\nPotential data type issues:")
    for col in date_columns:
        if df[col].dtype == 'object':
            print(f"- '{col}' might be a date but is stored as {df[col].dtype}")
    
    for col in numeric_columns:
        if df[col].dtype == 'object':
            print(f"- '{col}' might be numeric but is stored as {df[col].dtype}")
    
    for col in boolean_columns:
        if df[col].dtype not in ['bool', 'boolean']:
            print(f"- '{col}' might be boolean but is stored as {df[col].dtype}")
    
    # 3. Missing Values Analysis
    print("\n" + "=" * 40)
    print("3. MISSING VALUES ANALYSIS")
    print("=" * 40)
    
    # Calculate missing values by column
    missing_values = df.isnull().sum().sort_values(ascending=False)
    missing_percent = (df.isnull().sum() / len(df) * 100).sort_values(ascending=False)
    missing_df = pd.DataFrame({'Count': missing_values, 'Percent': missing_percent})
    
    # Total missing values
    total_missing = missing_values.sum()
    total_cells = df.size
    print(f"Total missing values: {total_missing} out of {total_cells} cells ({total_missing/total_cells*100:.2f}%)")
    
    # Columns with missing values
    missing_columns = missing_df[missing_df['Count'] > 0]
    if len(missing_columns) > 0:
        print(f"\nColumns with missing values ({len(missing_columns)}):")
        print(missing_columns.to_string())
    else:
        print("\nNo missing values found in any column.")
    
    # Highlight columns with high percentage of missing values
    critical_missing = missing_df[missing_df['Percent'] > 20]
    if len(critical_missing) > 0:
        print(f"\nColumns with critical missing rates (>20%):")
        print(critical_missing.to_string())
    
    # 4. Duplicate Records Analysis
    print("\n" + "=" * 40)
    print("4. DUPLICATE RECORDS ANALYSIS")
    print("=" * 40)
    
    # Check for complete duplicates
    duplicates = df.duplicated().sum()
    print(f"Complete duplicate rows: {duplicates} ({duplicates/len(df)*100:.2f}%)")
    
    # Check for potential duplicate bookings
    if 'Booking ID' in df.columns:
        booking_id_dupes = df['Booking ID'].duplicated().sum()
        print(f"Duplicate Booking IDs: {booking_id_dupes}")
    
    if 'Reservation ID' in df.columns:
        reservation_id_dupes = df['Reservation ID'].duplicated().sum()
        print(f"Duplicate Reservation IDs: {reservation_id_dupes}")
    
    # 5. Outlier Detection
    print("\n" + "=" * 40)
    print("5. OUTLIER DETECTION")
    print("=" * 40)
    
    # Function to detect outliers using IQR method
    def detect_outliers(df, column):
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)]
        return outliers, lower_bound, upper_bound, len(outliers) / len(df) * 100
    
    # Check for outliers in key numeric columns
    key_numeric_cols = ['Party Size', 'Search Days Ahead', 'Reservation Days Ahead', 
                        'Total Cost ($)', 'Reservation Cost ($)']
    
    for col in key_numeric_cols:
        if col in df.columns and pd.api.types.is_numeric_dtype(df[col]):
            try:
                outliers, lb, ub, pct = detect_outliers(df, col)
                print(f"\nOutliers in '{col}':")
                print(f"- Lower bound: {lb:.2f}, Upper bound: {ub:.2f}")
                print(f"- Number of outliers: {len(outliers)} ({pct:.2f}%)")
                if len(outliers) > 0 and len(outliers) < 10:
                    print("- Sample outlier values:", outliers[col].head().tolist())
            except Exception as e:
                print(f"Could not analyze outliers for '{col}': {str(e)}")
    
    # 6. Value Consistency Checks
    print("\n" + "=" * 40)
    print("6. VALUE CONSISTENCY CHECKS")
    print("=" * 40)
    
    # Check for consistency in categorical columns with low cardinality
    categorical_cols = df.select_dtypes(include=['object']).columns
    for col in categorical_cols:
        unique_count = df[col].nunique()
        # Only check columns with reasonable number of categories
        if 1 < unique_count < 20:
            print(f"\nAnalyzing consistency for '{col}' ({unique_count} unique values):")
            
            # Get all unique values and their counts
            value_counts = df[col].value_counts()
            print(f"- Value distribution: {dict(value_counts)}")
            
            # Check for potential inconsistencies (case, spaces, etc.)
            values = df[col].dropna().astype(str).unique()
            normalized_values = [val.lower().strip() for val in values]
            if len(set(normalized_values)) < len(values):
                print("- WARNING: Possible inconsistencies detected (case/spacing differences)")
                
                # Find groups of similar values
                value_groups = {}
                for i, val in enumerate(values):
                    norm_val = normalized_values[i]
                    if norm_val in value_groups:
                        value_groups[norm_val].append(val)
                    else:
                        value_groups[norm_val] = [val]
                
                # Print groups with multiple variations
                for norm_val, variations in value_groups.items():
                    if len(variations) > 1:
                        print(f"  Similar values: {variations}")
    
    # 7. Date Range Validation
    print("\n" + "=" * 40)
    print("7. DATE RANGE VALIDATION")
    print("=" * 40)
    
    # Check date columns for range validity
    for col in date_columns:
        if col in df.columns:
            try:
                # Try to convert to datetime if not already
                if df[col].dtype != 'datetime64[ns]':
                    date_series = pd.to_datetime(df[col], errors='coerce')
                else:
                    date_series = df[col]
                
                # Check if conversion worked
                if date_series.isnull().all():
                    print(f"'{col}' could not be converted to dates - invalid format")
                    continue
                    
                # Get min and max dates
                min_date = date_series.min()
                max_date = date_series.max()
                
                print(f"\nDate range for '{col}':")
                print(f"- Minimum date: {min_date}")
                print(f"- Maximum date: {max_date}")
                
                # Check for future dates if this might be an issue
                current_date = pd.Timestamp.now()
                future_dates = date_series[date_series > current_date]
                if len(future_dates) > 0:
                    print(f"- WARNING: {len(future_dates)} future dates detected ({len(future_dates)/len(df)*100:.2f}%)")
                
                # Check for very old dates (potential errors)
                very_old = date_series[date_series.dt.year < 2000]
                if len(very_old) > 0:
                    print(f"- WARNING: {len(very_old)} dates before year 2000 detected (possible errors)")
                
            except Exception as e:
                print(f"Could not analyze dates for '{col}': {str(e)}")
    
    # 8. Numeric Fields Validation
    print("\n" + "=" * 40)
    print("8. NUMERIC FIELDS VALIDATION")
    print("=" * 40)
    
    # Check numeric columns for valid ranges and statistical distribution
    for col in numeric_columns:
        if col in df.columns:
            try:
                # Try to convert to numeric if not already
                if not pd.api.types.is_numeric_dtype(df[col]):
                    # If the column contains currency, try to clean it first
                    if '$' in str(df[col].iloc[0]):
                        num_series = df[col].astype(str).str.replace('$', '').str.replace(',', '').astype(float)
                    else:
                        num_series = pd.to_numeric(df[col], errors='coerce')
                else:
                    num_series = df[col]
                
                # Basic statistics
                stats = num_series.describe()
                print(f"\nStatistics for '{col}':")
                print(f"- Count: {stats['count']}")
                print(f"- Mean: {stats['mean']:.2f}")
                print(f"- Std Dev: {stats['std']:.2f}")
                print(f"- Min: {stats['min']:.2f}")
                print(f"- 25%: {stats['25%']:.2f}")
                print(f"- Median: {stats['50%']:.2f}")
                print(f"- 75%: {stats['75%']:.2f}")
                print(f"- Max: {stats['max']:.2f}")
                
                # Check for negative values in columns that should be positive
                if 'cost' in col.lower() or 'price' in col.lower() or 'amount' in col.lower() or 'size' in col.lower():
                    neg_count = (num_series < 0).sum()
                    if neg_count > 0:
                        print(f"- WARNING: {neg_count} negative values detected in '{col}' ({neg_count/len(df)*100:.2f}%)")
                
                # Check for zero values
                zero_count = (num_series == 0).sum()
                if zero_count > 0:
                    print(f"- Zero values: {zero_count} ({zero_count/len(df)*100:.2f}%)")
                
            except Exception as e:
                print(f"Could not analyze numeric field '{col}': {str(e)}")
    
    # 9. Logical Consistency Checks
    print("\n" + "=" * 40)
    print("9. LOGICAL CONSISTENCY CHECKS")
    print("=" * 40)
    
    # Check logical relationships that should hold in the data
    
    # Example: If a reservation has packages, package cost should be > 0
    if 'Packages' in df.columns and 'Packages Cost ($)' in df.columns:
        packages_mask = df['Packages'].notna() & (df['Packages'] != '')
        zero_package_cost = df[packages_mask & (df['Packages Cost ($)'] == 0)]
        if len(zero_package_cost) > 0:
            print(f"WARNING: {len(zero_package_cost)} reservations have packages but zero package cost")
    
    # Example: Total cost should be sum of components
    if all(col in df.columns for col in ['Total Cost ($)', 'Reservation Cost ($)', 'Packages Cost ($)', 'Add Ons Cost ($)']):
        # Calculate sum of components
        df['Calculated Total'] = df['Reservation Cost ($)'] + df['Packages Cost ($)'] + df['Add Ons Cost ($)']
        if 'Promo Code Discount ($)' in df.columns:
            df['Calculated Total'] = df['Calculated Total'] - df['Promo Code Discount ($)']
        
        # Compare with stated total
        df['Cost Difference'] = abs(df['Total Cost ($)'] - df['Calculated Total'])
        inconsistent_costs = df[df['Cost Difference'] > 0.01]  # Allow for rounding
        
        if len(inconsistent_costs) > 0:
            print(f"WARNING: {len(inconsistent_costs)} reservations have inconsistent total costs")
            print(f"- Average discrepancy: ${inconsistent_costs['Cost Difference'].mean():.2f}")
            
    # 10. Summary of Findings
    print("\n" + "=" * 40)
    print("10. DATA QUALITY SUMMARY")
    print("=" * 40)
    
    # Count issues by category
    issues = []
    
    # Missing values issues
    missing_cols_count = len(missing_df[missing_df['Count'] > 0])
    critical_missing_count = len(missing_df[missing_df['Percent'] > 20])
    if missing_cols_count > 0:
        issues.append(f"- {missing_cols_count} columns with missing values")
    if critical_missing_count > 0:
        issues.append(f"- {critical_missing_count} columns with critical missing rates (>20%)")
    
    # Duplicate issues
    if duplicates > 0:
        issues.append(f"- {duplicates} duplicate rows detected")
    if 'Booking ID' in df.columns and df['Booking ID'].duplicated().sum() > 0:
        issues.append(f"- {df['Booking ID'].duplicated().sum()} duplicate Booking IDs")
    
    # Add other issue categories as needed
    
    # Print summary
    if issues:
        print("The following data quality issues were identified:")
        for issue in issues:
            print(issue)
    else:
        print("No significant data quality issues were identified.")
    
    print("\n" + "=" * 80)
    print("DATA QUALITY ANALYSIS COMPLETE")
    print("=" * 80)