using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace The_Cleaners
{
    public class Clean
    {
        public string clean_html;

        public Clean(string html)
        {
            clean_html = _clean(html);
        }

        private string _clean(string html)
        {
            string s;
            int index = html.IndexOf('\"');
            s = html.Remove(0, index + 1);

            return s;
        }
    }
}
