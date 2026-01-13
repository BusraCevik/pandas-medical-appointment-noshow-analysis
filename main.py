import os
from src.data_preparation import prepare_data

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
DOCS_DIR = os.path.join(BASE_DIR, 'docs')
OUTPUT_DIR = os.path.join(BASE_DIR, 'outputS')
SRC_DIR = os.path.join(BASE_DIR, 'src')


RAW_DATA_PATH = os.path.join(DATA_DIR, 'raw', "dataset.csv")
CLEANED_DATA_PATH = os.path.join(DATA_DIR, 'clean', "clean.csv")
FEATURES_DATA_PATH = os.path.join(DATA_DIR, 'featured',"featured.csv")

CSV_PATH = os.path.join(OUTPUT_DIR, 'csv')
FIGURES_PATH = os.path.join(OUTPUT_DIR, 'figures')

DASHBOARD_PATH = os.path.join(SRC_DIR, "dashboard.py")
DATA_PREPARATION_PATH = os.path.join(SRC_DIR, "data_preparation.py")
FEATURE_ENGINEERING_PATH = os.path.join(SRC_DIR, "feature_engineering.py")
ANALYSIS_PATH = os.path.join(SRC_DIR, "noshow_analysis.py")
VISUALIZATION_PATH = os.path.join(SRC_DIR, "visualization.py")



def main():
    prepare_data(RAW_DATA_PATH, CLEANED_DATA_PATH)





if __name__ == '__main__':
    main()
