/* lyp_bridge.cs for lyp_bridge, lieying_plugin .net C# to python3 bridge, sceext <sceext@foxmail.com> 
 * version 0.1.5.0 test201508182222
 *
 * use io_one_line_only.dll	// class IOOneLineOnly
 * use Run.dll from lieying .net C# plugin	// namespace PluginFace
 *
 * lyp_bridge supported command
 *	exit		// exit lyp_brigde
 *	GetVersion	// get plugin's Version info
 *
 *	Config		// call plugin's method: void Config()
 *	ApplyConfig	// call plugin's method: void ApplyConfig()
 *	Update, path	// call plugin's method: string Update(string path)
 *	Parse, url	// call plugin's method: string Parse(string url)
 *	ParseURL, url, label, min, max
 *			// call plugin's method: string ParseURL(string url, string label, int min, int max)
 * TODO not support Search() now
 *	Search, text, start, page_size, sort_by, reverse
 *			// call plugin's method: string Search(string text, int start, int page_size, string sort_by, bool reverse)
 *
 * TODO not support get lieying_plugin .net port, PluginFace.PluginAttribute.Function info
 *
 * compile with
 *	csc -R:io_one_line_only.dll,PluginFace.dll -o -out:lyp_bridge.exe lyp_bridge.cs
 */

using System;
using System.Reflection;
// used for create domain
using System.Runtime.Remoting;

// add version info
[assembly: AssemblyVersion("0.1.5.0")]
[assembly: AssemblyFileVersion("0.1.5.0")]

namespace lyp_bridge {
	
	// io base class, use io_one_line_only
	public class IOb {
		
		// base input and output
		
		// get one request
		public static string[] get_one_req() {
			return IOOneLineOnly.decode(IOOneLineOnly.read());
		}
		
		// output info
		public static void o(string[] a) {
			IOOneLineOnly.write(IOOneLineOnly.encode(a));
		}
	}
	
	// reflect base class
	public class Rb {
		
		// load a .dll by filename
		public static Assembly load_dll(string filename) {
			// just load it
			return Assembly.LoadFrom(filename);
		}
		
		// get Types in a Assembly, process and throw ERROR
		public static Type[] get_types(Assembly input) {
			// try to get all Types in Assembly
			Type[] aa = new Type[0];
			Type[] aa_ok = new Type[0];
			Exception[] aa_err = new Exception[0];
			Exception err = new Exception("");
			bool flag_err = false;
			try {
				aa = input.GetTypes();
			} catch (ReflectionTypeLoadException e) {
				err = e;
				aa_ok = e.Types;
				aa_err = e.LoaderExceptions;
				flag_err = true;
			}
			// check result
			if (!flag_err) {
				// ok, all works done
				return aa;
			} else {
				// load failed, give more ERROR information
				string err_text = "";
				// make err_text
				err_text += "ERROR: get types failed\n";
				// add each err info
				for (int i = 0; i < aa_err.Length; i++) {
					err_text += "  ---> " + i.ToString() + " : " + aa_err[i].ToString() + "\n";
				}
				// create a Exception and throw it
				throw new Exception(err_text, err);	// ERROR process done
			}
		}
		
		// get a class by attribute name, and throw ERROR
		public static Type get_class_by_attr(Type[] aa, string attr_name) {
			// check each Type in aa
			for (int i = 0; i < aa.Length; i++) {
				Type one = aa[i];
				// check is class
				if (!one.IsClass) {
					continue;
				}
				// check attributes
				object attr = get_attr_by_name(one, attr_name);
				if (attr != null) {	// check result
					return one;	// done, OK
				}
			}
			// class not found, throw a ERROR
			throw new Exception("ERROR: can not found a class with attribute \"" + attr_name + "\" ");
		}
		
		// get a attribute by name, NOTE not throw ERROR
		public static object get_attr_by_name(Type a, string attr_name) {
			// get attributes
			object[] attr = a.GetCustomAttributes(true);
			// check each attributes
			for (int i = 0; i < attr.Length; i++) {
				object one = attr[i];
				Type at = one.GetType();
				// check attribute's name
				if (at.FullName == attr_name) {
					return one;	// done, OK
				}
			}
			return null;	// not found
		}
		
		// get a value of a property
		public static object get_value(object host, string prop_name) {
			// get property's info
			Type t = host.GetType();
			PropertyInfo p = t.GetProperty(prop_name);
			object raw_value = p.GetValue(host, null);
			return raw_value;	// done
		}
		
		// create a instance of a class
		public static object create_instance(Type b) {
			// just create it
			return Activator.CreateInstance(b);
		}
		
		// invoke a method of a class
		public static object call(object host, string method_name, object args) {
			// get Type first
			Type t = host.GetType();
			MethodInfo m = t.GetMethod(method_name);
			object ret = null;
			// check args
			if (args == null) {
				ret = m.Invoke(host, null);
			} else {
				object[] a = (object[])args;
				ret = m.Invoke(host, a);
			}
			return ret;	// done
		}
	}
	
	// class to support lieying_plugin's INotify
	public class MyNotify : PluginFace.INotify {
		
		// flag to enable output
		public static bool enable_output = false;
		
		// real output function
		private static void real_output(string text) {
			// check flag
			if (enable_output) {
				// do output, just write with IOb
				string[] o = new string[2];
				o[0] = "print";
				o[1] = text;
				IOb.o(o);
			}
		}
		
		// methods support the INotify
		public void Information(string str) {
			// add something before string
			string output = "INFO: " + str;
			// just output
			real_output(output);
		}
		
		public void Warning(string str) {
			string output = "WARNING: " + str;
			real_output(output);
		}
		
		public void Error(string str) {
			string output = "ERROR: " + str;
			real_output(output);
		}
	}
	
	// plugin class, to call plugin's Run.dll, the actually bridge
	public class Bridge {
		
		// global config
		public static string dll_name = "Run.dll";
		public static string attr_name = "PluginFace.PluginAttribute";
		
		// instance of plugin's main class, and main attribute
		private static object main_attr = null;
		private static object main_c = null;
		
		// plugin init function
		public static string init() {
			// load dll
			Assembly a = Rb.load_dll(dll_name);
			Type[] aa = Rb.get_types(a);	// get types
			// find main class
			Type c = Rb.get_class_by_attr(aa, attr_name);
			// get the main attribute
			main_attr = Rb.get_attr_by_name(c, attr_name);
			
			// create an instance of main class
			main_c = Rb.create_instance(c);
			// set INotify to main class
			MyNotify notify = new MyNotify();
			Rb.call(main_c, "SetNotifySink", new object[]{notify});
			
			// init done, return AppDomain.CurrentDomain.BaseDirectory
			return AppDomain.CurrentDomain.BaseDirectory;
		}
		
		// get plugin's Version info
		public static string GetVersion() {
			// get info from main attr
			object raw = Rb.get_value(main_attr, "Version");
			string version = (string)raw;
			return version;	// done
		}
		
		// call plugin's method: void Config()
		public static void Config() {
			MyNotify.enable_output = true;
			// just call main_c
			Rb.call(main_c, "Config", null);
		}
		
		// call plugin's method: void ApplyConfig()
		public static void ApplyConfig() {
			MyNotify.enable_output = true;
			Rb.call(main_c, "ApplyConfig", null);
		}
		
		// call plugin's method: string Update(string path)
		public static string Update(string path) {
			// enable output
			MyNotify.enable_output = true;
			object raw = Rb.call(main_c, "Update", new object[]{path});
			
			string ret = (string)raw;
			// check ret to FIX BUG
			if (ret == null) {
				ret = "";
			}
			return ret;
		}
		
		// call plugin's method: string Parse(string url)
		public static string Parse(string url) {
			// enable output
			MyNotify.enable_output = true;
			object raw = Rb.call(main_c, "Parse", new object[]{url});
			string ret = (string)raw;
			return ret;
		}
		
		// call plugin's method: string ParseURL(string url, string label, int min, int max)
		public static string ParseURL(string url, string label, int min, int max) {
			MyNotify.enable_output = true;
			// just call main_c, NOTE the method name is "ParseUrl"
			object raw = Rb.call(main_c, "ParseUrl", new object[]{url, label, min, max});
			string ret = (string)raw;
			return ret;
		}
		
		// call plugin's method: string Search(string text, int start, int page_size, string sort_by, bool reverse)
		public static string Search(string text, int start, int page_size, string sort_by, bool reverse) {
			MyNotify.enable_output = true;
			
			object raw = Rb.call(main_c, "Search", new object[]{text, start, page_size, sort_by, reverse});
			string ret = (string)raw;
			// check ret to FIX BUG
			if (ret == null) {
				ret = "";
			}
			return ret;
		}
	}
	
	// main class, start the program
	public class LypBridgeMain {
		
		// exit code
		public static int exit_code = 0;
		
		// output ERROR
		private static void print_err(Exception e, string name) {
			// disable output
			MyNotify.enable_output = false;
			
			string[] o = new string[3];
			o[0] = "ERROR";
			o[1] = "sub plugin " + name + " failed ";
			o[2] = e.ToString();
			IOb.o(o);
		}
		
		// do_one command
		private static bool do_one(string[] c) {
			// check command args length
			int c_len = c.Length;
			if (c_len < 1) {	// input ERROR
				// make a output
				string[] o = new string[3];
				o[0] = "ERROR";
				o[1] = "input command args length error ";
				o[2] = c_len.ToString();
				IOb.o(o);
				// not exit
				return false;
			}
			// get and check first arg
			string first = c[0];
			switch (first) {
			case "exit":	// exit command
				return true;	// should exit
			case "GetVersion":	// string GetVersion()
				{
					string ret = "[[ERROR]]";
					try {	// just call bridge and return result, with ERROR check
						ret = Bridge.GetVersion();
					} catch (Exception e) {	// just output ERROR info
						print_err(e, "GetVersion()");
						break;
					}
					// disable output
					MyNotify.enable_output = false;
					// output result
					string[] o = new string[2];
					o[0] = "";
					o[1] = ret;
					IOb.o(o);
				}
				break;
			case "Config":	// void Config()
				{
					try {
						Bridge.Config();
					} catch (Exception e) {
						print_err(e, "Config()");
						break;
					}
					MyNotify.enable_output = false;
					// output result
					string[] o = new string[1];
					o[0] = "";
					IOb.o(o);
				}
				break;
			case "ApplyConfig":	// void ApplyConfig()
				{
					try {
						Bridge.ApplyConfig();
					} catch (Exception e) {
						print_err(e, "ApplyConfig()");
						break;
					}
					MyNotify.enable_output = false;
					// output result
					string[] o = new string[1];
					o[0] = "";
					IOb.o(o);
				}
				break;
			case "Update":	// string Update(string path)
				{
					// get args info
					string path = c[1];
					string ret = "[[ERROR]]";
					try {
						ret = Bridge.Update(path);
					} catch (Exception e) {
						print_err(e, "Update(\"" + path + "\")");
						break;
					}
					MyNotify.enable_output = false;
					// output result
					string[] o = new string[2];
					o[0] = "";
					o[1] = ret;
					IOb.o(o);
				}
				break;
			case "Parse":	// string Parse(string url)
				{
					string url = c[1];
					string ret = "[[ERROR]]";
					try {
						ret = Bridge.Parse(url);
					} catch (Exception e) {
						print_err(e, "Parse(\"" + url + "\")");
						break;
					}
					MyNotify.enable_output = false;
					// output result
					string[] o = new string[2];
					o[0] = "";
					o[1] = ret;
					IOb.o(o);
				}
				break;
			case "ParseURL":	// string ParseURL(string url, string label, int min, int max)
				{
					string url = c[1];
					string label = c[2];
					string raw_min = c[3];
					string raw_max = c[4];
					int min = Int32.Parse(raw_min);
					int max = Int32.Parse(raw_max);
					string ret = "[[ERROR]]";
					try {
						ret = Bridge.ParseURL(url, label, min, max);
					} catch (Exception e) {
						print_err(e, "ParseURL(\"" + url + "\", \"" + label + "\", " + min.ToString() + ", " + max.ToString() + ")");
						break;
					}
					MyNotify.enable_output = false;
					// output result
					string[] o = new string[2];
					o[0] = "";
					o[1] = ret;
					IOb.o(o);
				}
				break;
			case "Search":	// string Search(string text, int start, int page_size, string sort_by, bool reverse)
				{	// TODO NOTE not support Search() now
					MyNotify.enable_output = false;
					
					string[] o = new string[2];
					o[0] = "ERROR";
					o[1] = "not support Search() now ";
					IOb.o(o);
				}
				break;
			default:	// output first arg error
				{
					string[] o = new string[3];
					o[0] = "ERROR";
					o[1] = "unknow command ";
					o[2] = first;
					IOb.o(o);
				}
				break;
			}
			return false;	// by default, not exit
		}
		
		// mainloop
		private static int mainloop() {
			// init plugin first, and process ERROR
			bool flag_err = false;
			string err_str = "";
			string init_info = "";
			try {
				init_info = Bridge.init();
			} catch (Exception e) {
				// save ERROR msg
				flag_err = true;
				err_str = e.ToString();
			}
			// check init result and print info
			if (flag_err) {
				string[] o = new string[3];
				o[0] = "ERROR";
				o[1] = "sub plugin init failed ";
				o[2] = err_str;
				IOb.o(o);
				// no more works to do, just exit
				return 1;
			} else {
				string[] o = new string[2];
				o[0] = "";
				o[1] = "[ OK ] lyp_bridge started. ";
				// add init_info
				if ((init_info != null) && (init_info != "")) {
					o[1] += "\n" + init_info;
				}
				IOb.o(o);
			}
			// do works until exit
			while (true) {
				// get one input command
				string[] i = IOb.get_one_req();
				// just do this request
				bool flag_exit = do_one(i);
				if (flag_exit) {
					return exit_code;
				}
			}
		}
		
		// exe this in new domain
		private static int exe_in_new_domain(string sub_domain_base_dir, string exe_name, string[] args) {
			// set domain setup info
			AppDomainSetup s = new AppDomainSetup();
			s.ApplicationBase = sub_domain_base_dir;
			// create domain
			AppDomain d = AppDomain.CreateDomain("lyp_bridge.host_sub_domain", null, s);
			// just exe in sub domain
			return d.ExecuteAssembly(exe_name, args);	// done
		}
		
		// main function, entry point of this program
		public static int Main(string[] a) {
			// check args
			if (a.Length > 0) {
				// get first arg as Bridge.dll_name
				string dll_name = a[0];
				Bridge.dll_name = dll_name;
			}
			if (a.Length > 2) {
				// get second arg as Bridge.domain_base_dir
				string domain_base_dir = a[1];
				string exe_self_name = a[2];
				// just execute exe in sub domain, only pass first arg
				return exe_in_new_domain(domain_base_dir, exe_self_name, new string[]{a[0]});
			}
			
			// just start mainloop
			return mainloop();
		}
	}
}

/* end lyp_bridge.cs */


