from llama_index import *
import os

def chatbot_response(msg):
# API Key, my free trial has expired, can you see if you get any free trial on your account?

    os.environ["OPENAI_API_KEY"] = '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'

    # data loader, see https://gpt-index.readthedocs.io/en/latest/how_to/data_connectors.html 
    # for connecting different data sources
    import PyPDF2
    documents = SimpleDirectoryReader('C:/Users/dchhagani/OneDrive - Seneca/Desktop/demo/static/files').load_data()

    # set maximum input size
    max_input_size = 3896
    # set number of output tokens
    num_outputs = 200
    # set maximum chunk overlap
    max_chunk_overlap = 100
    # set chunk size limit
    chunk_size_limit = 600

    prompt_helper = PromptHelper(max_input_size, 
                                num_outputs, 
                                max_chunk_overlap, 
                                chunk_size_limit=chunk_size_limit)

    service_context = ServiceContext.from_defaults(prompt_helper=prompt_helper)

    index = GPTSimpleVectorIndex.from_documents(documents, service_context = service_context)

    index.save_to_disk('index.json')

    index = GPTSimpleVectorIndex.load_from_disk('index.json')

    # this is the system message that we use for every query

    guide = "Answer the following question consisely and honestly,"    "do not mention context in your answer,"    "say you don't know if you are unsure of the answer.\n"

    # get the response message string given a question, you can iterate this on a DF column for survey answering

    response = index.query(guide + msg).response
    print(response)
    return response

#msg1 = "Does you company has database credential policy?"
#chatbot_response(msg1)

from flask import *
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'C:/Users/dchhagani/OneDrive - Seneca/Desktop/demo/static/files'

@app.route('/')
def main():
	return render_template("index.html")
def Submit():
	if request.method == "POST": 
		message = request.form.get('msg')
	return render_template('index.html', message=message)

@app.route('/upload', methods=['POST'])
def upload():
	if request.method == 'POST':

		# Get the list of files from webpage
		files = request.files.getlist("file")

		# Iterate for each file in the files List, and Save them
		for file in files:
			#file.save(file.filename)
			file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
		return "<h1>Files Uploaded Successfully.!</h1>"

@app.route('/submit', methods= ['POST','GET'])
def Submit():
	if request.method == "POST": 
		message = request.form["msg"]
		print(message)
		answer=chatbot_response(message)
	return render_template('index.html', answer=answer)
		
	#return render_template('index.html', answer=answer)

if __name__ == '__main__':
	app.run(debug=True)





