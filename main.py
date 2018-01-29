from flask import Flask, request, render_template, redirect
from bettermtl2_flask import make2 as bmtlMake
from bettermtl2_flask import make as bmtlMake_legacy
from bettermtl2_flask import getPart as bmtlGetPart
from bettermtl2_flask import test as bmtlTest

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')
	
@app.route('/do', methods=['POST','GET'])
def handle():
	if request.method == "POST":
		return redirect(request.url_root+'do?url='+request.form['url'], code=302)
	elif request.method == "GET":
		leg = request.args.get('legacy', default="NOTHING")
		if leg == 'true':
			return bmtlMake_legacy(request.args.get('url', default="NOTHING"))	
			
		return bmtlMake(request.args.get('url', default="NOTHING"))	
		
		
@app.route('/getpart', methods=['GET'])
def getPart():
	p = request.args.get('part', default="NOTHING")
	f = request.args.get('total', default="NOTHING")
	url = request.args.get('url', default="NOTHING")
	id = request.args.get('id', default="NOTHING")
	return bmtlGetPart(url, int(p), int(f),id)
	
@app.route('/getTest', methods=['GET'])
def alpha():
	a = request.args.get('part', default="NOTHING")
	return 'Hello hello'
	
@app.route('/globalTest', methods=['GET'])
def globalTest():
	a = request.args.get('n', default="NOTHING")
	return bmtlTest(int(a))
	

	
	
	
	
if __name__ == '__main__':
	app.run(debug = True)