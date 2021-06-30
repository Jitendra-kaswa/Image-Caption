from flask import Flask,render_template,redirect,request
import caption_it

#__name__== __main__
app=Flask(__name__)


# @-> It is known as decorator
@app.route('/')
def hello():
	return render_template("index.html")

@app.route('/',methods=['POST'])
def caption_prediction():
	if request.method =="POST":
		#name=request.form['username']
		f=request.files['userfile']
		path="./static/{}".format(f.filename)
		f.save(path)
		caption = caption_it.caption_this_image(path)
		result_dic = {
		'image':path,
		'caption': caption
		}
	return render_template("index.html",your_result=result_dic)

if __name__ == '__main__':
	#app.debug=True # It is used to run the server autometically on save
	# or can use app.run(debug=True)
	app.run(debug=True,host='0.0.0.0',port=9696,threaded= False)