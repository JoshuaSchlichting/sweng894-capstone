import sys, os

# Add the app path to sys.path
# Since conftest.py is in root, we'll add <root>/app/
sys.path.insert(0, 
    os.path.dirname(os.path.abspath(__file__))
    + '/../app'
)
