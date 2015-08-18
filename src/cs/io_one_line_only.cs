/* io_one_line_only.cs, io_one_line_only for C#, sceext <sceext@foxmail.com> 
 * version 0.1.0.0 test201508190323
 */

using System;

// add version info
[assembly: AssemblyVersion("0.1.0.0")]
[assembly: AssemblyFileVersion("0.1.0.0")]

// #define FLAG_DEBUG

/* main class */

public class IOOneLineOnly {
	
	// io encode function
	public static string encode(string[] raw_text_list) {
		string[] raw = (string[])raw_text_list.Clone();
		// check null list
		if (raw.Length < 1) {
			return "";
		}
		// pre-process each raw text
		int len_raw = raw.Length;
		for (int i = 0; i < len_raw; i++) {
			string t = raw[i];
			// process this text
			
			// keep all '\' chars to be safe
			t = t.Replace("\\", "\\\\");
			// NOTE fix '\r' or '\r\n'
			t = t.Replace("\r\n", "\n");
			t = t.Replace("\r", "\n");
			// process multi-lines text
			t = t.Replace("\n", "\\n");
			
			// process one text done
			raw[i] = t;
		}
		// join all text to finish encode
		string out_ = String.Join("\\0", raw);
		out_ += "\\0";	// add one more \0 after last line
		// done
		return out_;
	}
	
	// io decode function
	public static string[] decode(string raw_text) {
		// check null decode
		if (raw_text == "") {
			return new string[0];
		}
		// normal decode, should scan each char
		string[] out_ = new string[0];
		int flag_ = 0;
		string t = "";
		// get each char in raw_text
		int raw_len = raw_text.Length;
		for (int i = 0; i < raw_len; i++) {
			string c = raw_text.Substring(i, 1);
			// check flag
			if (flag_ == 1) {
				flag_ = 0;	// turn off flag first
				// check chars
				if (c == "\\") {
					t += "\\";	// should be \ char
				} else if (c == "n") {
					t += "\n";	// should be '\n' char
				} else if (c == "0") {	// \0, should start a new text
					// add t to out
					int out_len = out_.Length;
					Array.Resize(ref out_, out_len + 1);
					out_[out_len] = t;
					// reset text
					t = "";
				} else {	// as a normal char
					t += c;
				}
			} else {	// check set flag
				if (c == "\\") {
					flag_ = 1;	// should turn on flag
				} else {
					t += c;	// append as a normal char
				}
			}
		}
		// NOTE do not add last line
		return out_;	// done
	}
	
	// stdin readline and stdout writeline
	public static string read() {
		return Console.In.ReadLine();
	}
	
	public static void write(string text) {
		Console.Out.WriteLine(text);
		Console.Out.Flush();	// flush now
	}

#if FLAG_DEBUG
	// test functions
	
	// print content of a array
	private static void print_array(string[] a) {
		int a_len = a.Length;
		for (int i = 0; i < a_len; i++) {
			string t = a[i];
			write(i + " : " + t);
		}
	}
	
	// compare 2 array content if same
	private static bool cmp_array(string[] a, string[] b) {
		// check length first
		int a_len = a.Length;
		int b_len = b.Length;
		if (a_len != b_len) {
			return false;
		}
		// check each element
		for (int i = 0; i < a_len; i++) {
			if (a[i] != b[i]) {
				return false;
			}
		}
		// cmp done, is same
		return true;
	}
	
	// before get input, print some text
	private static string read(string text) {
		Console.Out.Write(text);
		Console.Out.Flush();
		// get input
		return read();
	}
	
	// exit command is ':exit'
	public static void test() {
		string exit_c = ":exit";
		// test until got exit command
		while (true) {
			// get input
			string[] i = new string[0];
			// get input until got start test command
			string start_c = ":test";
			while (true) {
				string one = read(":");
				if (one == start_c) {
					break;
				} else if (one == exit_c) {	// check exit command
					return;
				}
				// append this line to input array
				int i_len = i.Length;
				Array.Resize(ref i, i_len + 1);
				i[i_len] = one;
			}
			// just start test
			string result = encode(i);
			// print result
			write(result);
			
			// test decode
			write(":: test decode");
			string[] test = decode(result);
			// print result and auto cmp if decode works right
			print_array(i);
			print_array(test);
			
			// check result
			if (cmp_array(i, test)) {
				write(":: result [ OK ]");
			} else {
				write(":: result ERROR ");
			}
		}
		// test done
	}
	
	// for debug
	// main to start program to test
	public static int Main() {
		// just start test
		test();
		// test done
		return 0;
	}
#endif
}

/* end io_one_line_only.cs */


