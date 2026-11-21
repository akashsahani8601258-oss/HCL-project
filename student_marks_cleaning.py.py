"""
Student Marks Prediction - Data Cleaning Source Code
----------------------------------------------------
How to run:
1. Keep this Python file and student_marks_uncleaned.csv in the same folder.
2. Install dependencies: pip install pandas numpy
3. Run: python student_marks_cleaning.py

Output:
- student_marks_cleaned.csv
"""

import pandas as pd
import numpy as np

INPUT_FILE = "student_marks_uncleaned.csv"
OUTPUT_FILE = "student_marks_cleaned.csv"


def clean_student_marks(input_file=INPUT_FILE, output_file=OUTPUT_FILE):
    # Load the uncleaned dataset
    df = pd.read_csv(input_file)

    print("Original dataset shape:", df.shape)
    print("\nMissing values before cleaning:\n", df.isnull().sum())

    # Remove extra spaces and standardize text columns
    text_columns = ["Student_Name", "Gender", "Result"]
    for column in text_columns:
        df[column] = df[column].astype("string").str.strip()

    # Standardize Gender values
    gender_map = {
        "male": "Male",
        "m": "Male",
        "female": "Female",
        "f": "Female"
    }
    df["Gender"] = df["Gender"].str.lower().map(gender_map)

    # Convert numeric columns; invalid text becomes NaN
    numeric_columns = [
        "Attendance_Percentage",
        "Study_Hours_Per_Day",
        "Previous_Semester_Marks",
        "Assignments_Completed",
        "Internal_Marks",
        "Final_Exam_Marks"
    ]

    # Handle percentage values such as '105%'
    df["Attendance_Percentage"] = (
        df["Attendance_Percentage"]
        .astype("string")
        .str.replace("%", "", regex=False)
    )

    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    # Replace out-of-range values with NaN
    df.loc[~df["Attendance_Percentage"].between(0, 100), "Attendance_Percentage"] = np.nan
    df.loc[~df["Study_Hours_Per_Day"].between(0, 24), "Study_Hours_Per_Day"] = np.nan
    df.loc[~df["Previous_Semester_Marks"].between(0, 100), "Previous_Semester_Marks"] = np.nan
    df.loc[~df["Assignments_Completed"].between(0, 10), "Assignments_Completed"] = np.nan
    df.loc[~df["Internal_Marks"].between(0, 30), "Internal_Marks"] = np.nan
    df.loc[~df["Final_Exam_Marks"].between(0, 70), "Final_Exam_Marks"] = np.nan

    # Fill missing numeric values with column medians
    for column in numeric_columns:
        df[column] = df[column].fillna(df[column].median())

    # Fill missing categorical values with the mode (or a fallback)
    for column in ["Gender", "Result"]:
        mode_values = df[column].mode(dropna=True)
        fill_value = mode_values.iloc[0] if not mode_values.empty else "Unknown"
        df[column] = df[column].fillna(fill_value)

    # Standardize Result values
    result_map = {
        "pass": "Pass",
        "p": "Pass",
        "fail": "Fail",
        "f": "Fail"
    }
    df["Result"] = df["Result"].str.lower().map(result_map).fillna("Unknown")

    # Remove duplicate records
    df = df.drop_duplicates()

    # Remove duplicate Student_ID values, keeping the first occurrence
    df = df.drop_duplicates(subset=["Student_ID"], keep="first")

    # Save cleaned dataset
    df.to_csv(output_file, index=False)

    print("\nCleaned dataset shape:", df.shape)
    print("\nMissing values after cleaning:\n", df.isnull().sum())
    print(f"\nCleaned file saved as: {output_file}")


if __name__ == "__main__":
    clean_student_marks()
