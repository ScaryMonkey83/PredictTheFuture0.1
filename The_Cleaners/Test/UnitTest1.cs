using System;
using Microsoft.VisualStudio.TestTools.UnitTesting;

using The_Cleaners;
using WordProcessing;

namespace Trie
{
    [TestClass]
    public class Build
    {
        [TestMethod]
        public void DoesFindFirstOfWork()
        {
            var s = WordProcessing.TrieBuilder._FindFirstOf(" noun ",
                "a / e/, A noun the first letter of the alphabet, abbreviate / ə bri viet / verb 1.to shorten");

            Assert.AreEqual(10,s);
        }

        [TestMethod]
        public void BuildFromParse()
        {
            WordProcessing.TrieBuilder.ParseThroughDictionary();
        }
    }
}
