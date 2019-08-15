import sys
sys.path.append(r"C:\Users\jaleh\Desktop\Predict Versions\PredictTheFuture0.1\The_Cleaners\The_Cleaners\bin\Debug")
import clr
clr.AddReference(r"The_Cleaners")
from WordProcessing import TrieBuilder

from Scrape.StripNShit import StripNShit

if __name__ == '__main__':
    TrieBuilder.ParseThroughDictionary()