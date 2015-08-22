/* wb_proxy.cs, use webbrowser to load page with http proxy, sceext <sceext@foxmail.com> 2015.08 
 * version 0.0.2.0 test201508220212
 */

using System;
using System.Threading;
using System.Windows.Forms;

using SetProxy;

// wb_proxy main class
class WbProxy {
	
	// simple print function, for DEBUG
	private static void print(string text) {
		Console.WriteLine(text);
	}
	
	// create main window, set proxy, and create WebBrowser
	private static Form create(string url, string proxy) {
		
		// print log for DEBUG
		print("INFO: set http_proxy to \"" + proxy + "\" ");
		// set http proxy
		WinInetInterop.SetConnectionProxy(proxy);
		
		print("INFO: creating main window ");
		// create main window
		Form f = new Form();
		f.Text = "wb_proxy main window for IE ";	// set window title
		
		// create web browser
		WebBrowser wb = new WebBrowser();
		wb.Dock = DockStyle.Fill;	// set dock style of wb
		f.Controls.Add(wb);		// add it to Form
		
		print("INFO: loading page \"" + url + "\" ");
		// load page
		Uri uri = new Uri(url);
		wb.Url = uri;
		
		// show main window
		f.ResumeLayout(false);
		f.PerformLayout();
		
		return f; // done
	}
	
	[STAThread]	// main function
	public static int Main(string[] arg) {
		
		// get args from command line
		string proxy = arg[0];
		string url = arg[1];
		
		// just start test
		Form f = create(url, proxy);
		
		print("[ OK ] init done. ");
		// run the app
		Application.Run(f);
		
		return 0;	// done
	}
}

/* end wb_proxy.cs */


