/* wb_proxy.cs, use webbrowser to load page with http proxy, sceext <sceext@foxmail.com> 2015.08 
 * version 0.0.1.0 test201508220102
 */

using System;
using System.Threading;
using System.Windows.Forms;

using SetProxy;

// FIXME main test class
class Test {
	
	// simple print function
	private static void print(string text) {
		Console.WriteLine(text);
	}
	
	// main test function
	private static Form test(string url, string proxy) {
		
		// FIXME debug here
		print("DEBUG: got here 1, ready to set proxy to \"" + proxy + "\" ");
		
		// set http proxy
		WinInetInterop.SetConnectionProxy(proxy);
		
		// create a window
		Form f = new Form();
		f.Name = "wb_proxy";
		f.Text = "wb_proxy title test";
		
		// FIXME
		print("DEBUG: got here 2, set proxy done ");
		
		print("DEBUG: got here 3, ready to create WebBrowser ");
		// create web browser
		WebBrowser wb = new WebBrowser();
		
		// set dock of wb
		wb.Dock = DockStyle.Fill;
		
		// add it to Form
		f.Controls.Add(wb);
		wb.Show();	// show it
		
		print("DEBUG: got here 4, created web browser ");
		// load page
		Uri uri = new Uri(url);
		// FIXME
		print("DEBUG: got here 5, created uri ");
		wb.Url = uri;
		
		print("DEBUG: got here 6, set Url finished ");
		// FIXME maybe should do more
		
		// FIXME TODO try to show window
		f.ResumeLayout(false);
		f.PerformLayout();
		
		// done
		return f;
	}
	
	// function for BeginInvoke
	
	// main function
	[STAThread]
	public static int Main(string[] arg) {
		
		// get args from command line
		string proxy = arg[0];
		string url = arg[1];
		
		// just start test
		Form f = test(url, proxy);
		// show it
		f.Show();
		
		// run the window
		Application.Run(f);
		
		// FIXME just for DEBUG
		return 0;
	}
}

/* end wb_proxy.cs */


