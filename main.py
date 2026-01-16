import os
from src.data_preparation import prepare_data
from src.feature_engineering import create_featured_dataset
from src.noshow_analysis import noshow_analysis
from src.visualization import generate_visualizations
from src.dashboard import build_noshow_dashboard




BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
DOCS_DIR = os.path.join(BASE_DIR, 'docs')
OUTPUT_DIR = os.path.join(BASE_DIR, 'outputs')
SRC_DIR = os.path.join(BASE_DIR, 'src')


RAW_DATA_PATH = os.path.join(DATA_DIR, 'raw', "dataset.csv")
CLEANED_DATA_PATH = os.path.join(DATA_DIR, 'clean', "clean.csv")
FEATURED_DATA_PATH = os.path.join(DATA_DIR, 'featured',"featured.csv")

CSV_PATH = os.path.join(OUTPUT_DIR, 'csv')
FIGURES_PATH = os.path.join(OUTPUT_DIR, 'figures')
DASHBOARD_HTML_PATH = os.path.join(DOCS_DIR, "index.html")

DASHBOARD_PATH = os.path.join(SRC_DIR, "dashboard.py")
DATA_PREPARATION_PATH = os.path.join(SRC_DIR, "data_preparation.py")
FEATURE_ENGINEERING_PATH = os.path.join(SRC_DIR, "feature_engineering.py")
ANALYSIS_PATH = os.path.join(SRC_DIR, "noshow_analysis.py")
VISUALIZATION_PATH = os.path.join(SRC_DIR, "visualization.py")



def main():
    prepare_data(RAW_DATA_PATH, CLEANED_DATA_PATH)
    create_featured_dataset(CLEANED_DATA_PATH,FEATURED_DATA_PATH)
    noshow_analysis(FEATURED_DATA_PATH, CSV_PATH)
    generate_visualizations(CSV_PATH, FIGURES_PATH)
    build_noshow_dashboard(CSV_PATH, FEATURED_DATA_PATH, DASHBOARD_HTML_PATH)




if __name__ == '__main__':
    main()
