from flask import Flask, render_template

app = Flask(
	__name__,
	template_folder='templates',
	static_folder='static'
)

@app.route('/')
def base_page():
	return render_template(
		'index.html'


	)


@app.route('/2')
def page_2():
	
	return render_template('site_2.html')


if __name__ == "__main__": 
	app.run(host='0.0.0.0')