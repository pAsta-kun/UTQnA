from flask import Flask, request, jsonify
from flask_cors import CORS
import pinecone
from openai.embeddings_utils import get_embedding
from tqdm import tqdm
import docx
import os
import openai
from APIKeys import pineconeKey as pineconeKey
from APIKeys import openAIKey as openAIKey
from langchain import OpenAI, ConversationChain, LLMChain, PromptTemplate
from langchain.memory import ConversationBufferWindowMemory 

app = Flask(__name__)
CORS(app)

openai.api_key = openAIKey
llm = OpenAI(openai_api_key=openAIKey)
os.environ["OPENAI_API_KEY"] = openAIKey
pinecone.init(
    api_key=pineconeKey,
    environment="us-west4-gcp-free"
)

# create or connect to index
index_name = "index"

if index_name not in pinecone.list_indexes():
    pinecone.create_index(index_name, dimension=1536)
# connect to index
index = pinecone.Index(index_name)

def search_docs(query):
    xq = openai.Embedding.create(input=query, engine="text-embedding-ada-002")['data'][0]['embedding']
    res = index.query([xq], top_k=3, include_metadata=True)
    chosen_text = []
    for match in res['matches']:
        chosen_text = match['metadata']
    return res['matches']


def construct_prompt(query):
    matches = search_docs(query)

    chosen_text = []
    for match in matches:
        chosen_text.extend(match['metadata']['text'])

    prompt = "Context: " + "\n".join(chosen_text)
    prompt += "\n\n"
    prompt += "Question: " + query
    prompt += "\n"
    print(prompt)
    return prompt

def answer_question(query):
    template = """
    Here's history of the past chat: {history}.
    Here's the users question along with some context to help you give an accurate answer: {human_input}.
    """
    prompt = PromptTemplate(
        input_variables=["history", "human_input"],
        template = template,
    )

    memory = ConversationBufferWindowMemory(memory_key="history", k=2)
    chatgpt_chain = LLMChain(
        llm=OpenAI(temperature=0),
        prompt=prompt,
        verbose=True,
        memory=memory,
    )
    output = chatgpt_chain.predict(human_input=construct_prompt(query))
    print(output)
    return output
    #prompt = construct_prompt(query)
    #res = openai.Completion.create(
    #    prompt=prompt,
    #    model="text-davinci-003",
    #    max_tokens=2000,
    #    temperature=0.4,
    #)
    #return res.choices[0].text

@app.route('/', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def handle_request():
    if request.method == 'GET':
        return 'EssAI Server'
    elif request.method == 'POST':
        requestData = request.get_json()  # Get the data from the POST request
        query = requestData['message']  # Extract the 'message' field
        response = answer_question(query)  # Generate the response using your answer_question function
        print("***************************" + response)
        return jsonify({"bot": response}) # Return the response as JSON

if __name__ == '__main__':
    app.run(port=5000)