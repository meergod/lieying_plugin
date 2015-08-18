/* open_page.js for nosalt_271; open web page in slimerjs, and show loaded resources
 * version 0.1.0.0 test201508190326
 */

// use strict mode for ECMAScript6
'use strict';

// require import modules
const webpage = require('webpage');
const system = require('system');

// global vars
let flag_debug = false;

// example URL to get
// http://cache.video.qiyi.com/vms?key=fvip&src=1702633101b340d8917a69cf8a4b8c7c&tvId=387504400&vid=bb6f4735e09b0245dfd566328e8d62cd&vinfo=1&tm=1795&enc=df24f77cc24e89fb505f1a98cccf152c&qyid=c4f933ae3cf87f11f2a2ff1a2769c453&puid=&authKey=bbd1f4e04846be80515a6299290e3c45&um=0&thdk=&thdt=&rs=1&tn=0.9687893758527935

const re_target_url = '&src=1702633101b340d8917a69cf8a4b8c7c&';

/* functions */

// log function
	function log(text) {
		// check flag_debug
		if (flag_debug) {
			console.log(text);
			return false;
		}
		return true;
	}

// open page and show loaded resources
	function open_page(url) {
		let page = webpage.create();
		
		// make regexp first
		let re = new RegExp(re_target_url);
		
		// for record time
		let start_load_page_time;
		
		// listen page to load resources
		page.onResourceRequested = function (requestData, networkRequest) {
			// get request info
			let id = requestData.id;
			let req_url = requestData.url;
			// just print it
			log(id + ' # ' + req_url);
			
			// check needed URL and process
			if (re.test(req_url)) {	// OK, yes, it is !!
				// print and output result
				print_result(requestData, start_load_page_time);
				// done, just exit slimerjs
				phantom.exit();
			}
		};
		
		// load page
		page.open(url, function (status) {
			// just show status
			log(' :: load page status [' + status + '] ');
		});
		
		// save time now
		start_load_page_time = Date.now();
		
		// print log
		log(' :: loading page \"' + url + '\"');
	}

// print and output result
	function print_result(req_data, start_time) {
		let id = req_data.id;
		let url = req_data.url;
		let header = req_data.headers;
		
		// gen used time
		let now = Date.now();
		let used_ms = now - start_time;
		let used_s = used_ms / 1e3;
		
		// make info obj
		let out = {
			id : id, 
			url : url, 
			time_s : used_s, 	// used time_s from start load page
			//header : header, 
			// NOTE print headers is no use, no Cookie in headers
		};
		// print as json
		// make text
		let t = JSON.stringify(out, null, '    ');
		console.log('\n' + t + '\n');
	}

// main function
	function main() {
		// get args from command line
		let args = system.args.slice(1);
		
		// get url to load
		let url = args[0];
		
		// load page
		open_page(url);
	}

// exports NOTE no need to do

// start from main
	main();

/* end open_page.js */


