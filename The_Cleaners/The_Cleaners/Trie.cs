using System;
using System.CodeDom;
using System.CodeDom.Compiler;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Security.Principal;
using System.Text;
using System.Threading.Tasks;
using System.Xml.Serialization;
using Org.BouncyCastle.Asn1;
using Org.BouncyCastle.Security;

namespace WordProcessing
{
    public enum PartOfSpeech
    {
        Noun,
        Preposition,
        Abrev,
        Conjunction,
        Article,
        Adjective,
        Verb,
        Adverb,
        Pronoun,
        Prefix,
        Suffix,
        Interjection,
        DudeThisIsNotRight
    }

    public class Trie
    {
        

        private class Node
        {
            public Node leftChildNode;
            public Node rightSiblingNode;
            public char key;
            public bool endWord;
            public List<PartOfSpeech> pos;

            public Node()
            {
                leftChildNode = null;
                rightSiblingNode = null;
                key = '\0';
                endWord = false;
                pos = null;
            }
        }

        private Node _inceptionNode;
        
        public Trie()
        {
            _inceptionNode = new Node();
        }


        /*
        public Trie(string path)
        {
            _inceptionNode = new Node();

            var words = System.IO.File.ReadAllLines(path);
            foreach (string word in words)
            {
                Add(word);
            }
        }
        */


        public void Add(string word, string poSpeech)
        {
            Node temp = _inceptionNode;
            foreach (char c in word)
            {
                if (temp.leftChildNode == null)
                {
                    temp.leftChildNode = new Node();
                    temp = temp.leftChildNode;
                    temp.key = c;
                }
                else temp = temp.leftChildNode;
                
                temp = _checkLevel(temp, c);

                if (temp.key != c)
                {
                    temp.rightSiblingNode = new Node();
                    temp = temp.rightSiblingNode;
                    temp.key = c;
                }
            }

            temp.endWord = true;
            temp.pos.Add(_speech(poSpeech));
        }

        public bool Contains(string word)
        {
            Node temp = _inceptionNode;
            foreach (char c in word)
            {
                if (temp.leftChildNode == null)
                {
                    return false;
                }
                else
                {
                    temp = temp.leftChildNode;
                    temp = _checkLevel(temp, c);
                    if (temp.key != c) return false;
                }
            }

            return temp.endWord;
        }

        private static PartOfSpeech _speech(string pos)
        {
            PartOfSpeech o;
            switch (pos)
            {
                case " plural noun ":
                case " noun ":
                    o = PartOfSpeech.Noun;
                    break;
                case " conj ":
                    o = PartOfSpeech.Conjunction;
                    break;
                case " adv ":
                    o = PartOfSpeech.Adverb;
                    break;
                case " prefix ":
                    o = PartOfSpeech.Prefix;
                    break;
                case " article ":
                    o = PartOfSpeech.Article;
                    break;
                case " adj ":
                    o = PartOfSpeech.Adjective;
                    break;
                case " modal verb ":
                case " verb ":
                    o = PartOfSpeech.Verb;
                    break;
                case " prep ":
                    o = PartOfSpeech.Preposition;
                    break;
                case " abbr ":
                    o = PartOfSpeech.Abrev;
                    break;
                case " interj ":
                    o = PartOfSpeech.Interjection;
                    break;
                case " pron ":
                    o = PartOfSpeech.Pronoun;
                    break;
                case " suffix ":
                    o = PartOfSpeech.Suffix;
                    break;
                default:
                    o = PartOfSpeech.DudeThisIsNotRight;
                    throw new Exception("Dude, this is not right");
            }

            return o;
        }

        private static Node _checkLevel(Node start, char c)
        {
            Node Uproot(Node n)
            {
                if (n.key == c || n.rightSiblingNode == null) return n;
                n = n.rightSiblingNode;
                Node t = Uproot(n);

                return t;
            }

            return Uproot(start);
        }
    }

    public static class TrieBuilder
    {
        private static readonly string[] _stringsList = { " abbr ", " adj ", " adv ", " article ", " conj ", " interj  ", " modal verb ", " noun ", " plural noun ", " prefix ", " prep ", " pron ", " suffix ", " verb " };
        public static Trie T = new Trie();

        public static void ParseThroughDictionary()
        {
            const string pathname =
                @"C:\Users\jaleh\Desktop\Predict Versions\PredictTheFuture0.1\The_Cleaners\The_Cleaners\dictionary.txt";

            var lines = File.ReadAllLines(pathname);
            var connection = new SQL.SQL("server=localhost;user=root;database=db1;port=3306;password=L0adingg...");

            foreach (string line in lines)
            {
                
            }
        }

        public static void GetFromDatabase()
        {
            throw new NotImplementedException();
        }

        public static void UpdateFromInternet()
        {
            throw new NotImplementedException();
        }

        internal static class _Helpers
        {

        }

        public static int _FindFirstOf(string pos, string line)
        {
            int location;

            for (location = 0; location < line.Length - pos.Length; location++)
            {
                if (pos.Equals(line.Substring(location, pos.Length)))
                    return location;
            }
            throw new Exception(String.Format("There is no instance of \n{0}\n in the line \n{1}", pos, line));
        }

        public static string[] _GetPosStrings(bool[] check)
        { 
            List<string> l = new List<string>();
            for (int ii = 0; ii < _stringsList.Length; ii++)
                if (check[ii]) l.Add(_stringsList[ii]);
            return l.ToArray();
        }

        _FindPOS
    }
}
