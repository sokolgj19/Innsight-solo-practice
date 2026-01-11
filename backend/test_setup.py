"""Test script to verify setup"""
import sys
import pandas as pd
import pymongo
import flask
import nltk

print("="*50)
print("✅ SETUP VERIFICATION")
print("="*50)
print(f"Python: {sys.version}")
print(f"Pandas: {pd.__version__}")
print(f"PyMongo: {pymongo.__version__}")
print(f"Flask: {flask.__version__}")
print(f"NLTK: {nltk.__version__}")
print("="*50)
print("🎉 SUCCESS! All packages installed!")
print("="*50)
