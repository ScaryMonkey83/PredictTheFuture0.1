using System;
using System.Data;

using MySql.Data;
using MySql.Data.MySqlClient;

namespace SQL
{
    public class SQL
    {
        private MySqlConnection _connection;

        public SQL(string connStr)
        {
            _connection = _Connect(connStr);
        }

        // Creates sql connection
        //
        //  INPUTS: sql query string,      sql
        //
        // IT IS UP TO THE CLIENT TO CLOSE THE CONNECTION IT RECIEVES WITH Close()
        private MySqlConnection _Connect(string connStr)
        {
            // string connStr = "server=localhost;user=root;database=db1;port=3306;password=L0adingg...";
            MySqlConnection conn = new MySqlConnection(connStr);
            conn.Open();
            return conn;
        }

        // Closes the private connection
        public void Close()
        {
            _connection.Close();
        }

        // Inserts a word - part of speech combination into database
        //
        // INPUTS: word,                    word
        //         part of speech,          pos
        public void InsertWordPair(string word, string pos)
        {
            try
            {

                string procedure = "insert_word_POS";
                MySqlCommand cmd = new MySqlCommand(procedure, _connection);
                cmd.CommandType = CommandType.StoredProcedure;

                cmd.Parameters.AddWithValue("@word", word);
                cmd.Parameters.AddWithValue("@pos", pos);

                cmd.ExecuteReader();
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.ToString());
            }
        }
    }
}
