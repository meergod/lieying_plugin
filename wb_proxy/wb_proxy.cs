/* wb_proxy.cs, use webbrowser to load page with http proxy, sceext <sceext@foxmail.com> 2015.08 
 * version 0.0.1.0 test201508220102
 */

using System;
using System.Windows.Forms;

using SetProxy;

// FIXME main test class
class Test {
	
	// main test function
	private static void test(string url, string proxy) {
		// set http proxy
		WinInetInterop.SetConnectionProxy(proxy);
		
		// create web browser
		WebBrowser wb = new WebBrowser();
		// load page
		Uri uri = new Uri(url);
		wb.Url = uri;
		
		// FIXME maybe should do more
		
	}
	
	// main function
	public static int Main(string[] arg) {
		
		// get args from command line
		string proxy = arg[0];
		string url = arg[1];
		
		// just start test
		test(url, proxy);
		
		// FIXME just for DEBUG
		return 0;
	}
}

/* end wb_proxy.cs */


