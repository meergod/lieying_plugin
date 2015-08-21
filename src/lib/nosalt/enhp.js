/* enhp.js, enhp : Easy node.js HTTP Proxy, sceext <sceext@foxmail.com> 2015.08 
 * version 0.0.5.0 test201508220741
 *
 * NOTE please run this proxy server with
 *	node --harmony enhp.js
 * to enable use of ECMAScript6
 */
'use strict';	// use ECMAScript6

/* require import */
const http = require('http');
const url = require('url');

// global vars

const etc = {};	// global config info obj
etc.port = 18080;	// http proxy server will listen this port, default is 18080
etc.flag_debug = false;

/* functions */

// log functions
	function server_log(req, raw_url) {
		// get info
		const method = req.method;
		const req_url = req.url;
		
		// make log text
		let t = 'request: ' + method + ' ' + req_url;
		
		// do log
		console.log(t);
	}
	
	// log when got response
	function server_log_res(req_url, res) {
		// check flag_debug
		if (!etc.flag_debug) {
			return;
		}
		
		const code = res.statusCode;
		// make log text
		let t = 'res: ' + code + ' ' + req_url;
		// do log
		console.log(t);
	}

// process incoming request
	function server_on_req(req, res) {
		// get request info
		const req_method = req.method;	// looks like GET
		const req_url = req.url;	// looks like http://www.sogou.com/
		const req_header = req.headers;	// request HTTP headers
		// just parse request url with url
		const req_info = url.parse(req_url);
		// add more info to req_info
		req_info.method = req_method;
		req_info.headers = req_header;
		// proxy start request, and set proxy response listener
		const proxy = http.request(req_info, function (imsg) {
			// imsg : IncommingMessage
			
			// print log
			server_log_res(req_url, imsg);
			
			// get res info
			const res_code = imsg.statusCode;
			const res_msg = imsg.statusMessage;
			const res_header = imsg.headers;
			// write head to res
			res.writeHead(res_code, res_msg, res_header);
			
			// process returned data by set event listeners
			imsg.on('data', function (chunk) {
				res.write(chunk);
			});
			imsg.on('end', function () {
				res.end();
			});
		
		});
		// set event listeners for post data
		req.on('data', function (chunk) {
			proxy.write(chunk);
		});
		req.on('end', function () {
			proxy.end();
		});
		
		// just a very simple log
		server_log(req, req_url);
	}

// start http proxy server, port : to listen
	function start_server(port) {
		// create server
		const server = http.createServer(server_on_req);
		server.listen(port);	// start server
		return server;	// done
	}

// get args from command line
	function get_args(raw) {
		let rest = raw;
		while (rest.length > 0) {
			let one = rest[0];
			rest = rest.slice(1);
			switch (one) {
			case '--debug':	// should turn on debug flag
				etc.flag_debug = true;
				break;
			default:	// this should be the port
				try {
					let port = parseInt(one);
					etc.port = port;
				} catch (e) {
				}	// just ignore it
			}
		}	// process command line args done
	}

// main function
	function main() {
		// get command options
		get_args(process.argv.slice(2))
		// just start server
		let port = etc.port;
		start_server(port);
		// print one line log after init OK
		console.log('[ OK ] enhp server started listen ' + port + ' ');
	}

// exports is not needed for main scripts, just start from main
	main();

/* end p.js */


