from langchain.document_loaders.csv_loader import CSVLoader
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain

from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY=os.environ["OPENAI_API_KEY"]

loader = CSVLoader(file_path='data/paper.csv')
documents = loader.load()

embeddings = OpenAIEmbeddings(openai_api_key = OPENAI_API_KEY)

db = FAISS.from_documents(documents, embeddings)

def retrieve_info(query):
  similar_response = db.similarity_search(query, k=3)
  page_contants_array = [doc.page_content for doc in similar_response]
  return page_contants_array


llm = ChatOpenAI(temperature=0, model='gpt-3.5-turbo-0125', openai_api_key = OPENAI_API_KEY)

template = """
You are a world class product matching specialist.
I will share a list of products, and you will find the best match of the products.

Below is the description of a product that needs to be matched:
{product_description}

Here is the list of products that we have information
{existing_products}

Please find the best matched products of existing_products only from product_description.
First compare these products on core specs that are relevant to this product, focus more on numeric features.
Compare both similar and different features in great detail and output in bullet points.
Then return a numeric similarity score between 0 and 1 based on the comparison to imply how similar they are.
Please find at least 3 of these kind of products.

Below is an example of output
1. Product name
Brand name
Store name
url
Key differences between 2 products:
- difference A
- difference B
- difference C
- ...
Similarity score: 0.9
"""

prompt = PromptTemplate(
    input_variables=["product_description", "existing_products"],
    template=template
)

chain = LLMChain(llm=llm, prompt = prompt)


odp_prd = """
Hammermill® Copy Plus® Copier Paper, Letter Size (8 1/2" x 11"), 5000 Total Sheets, 92 (U.S.) Brightness, 20 Lb, FSC® Certified, White, 500 Sheets Per Ream, Case Of 10 Reams

Hammermill Copy Plus paper is an economical copy paper designed for everyday use at offices large and small. Offering dependable performance on all office machines, you'll want to have plenty of this dependable paper on hand for everyday, general office use. ColorLok for bolder blacks, brighter colors and faster drying. Backed by the 99.99% Jam-Free Guarantee. Acid-free material prevents yellowing over time to ensure a long-lasting appearance.

Perfect for black and white printing, drafts and forms. - Hammermill is more than just paper.
99.99% JAM-FREE GUARANTEE - You can trust Hammermill paper quality, guaranteed.
COLORLOK TECHNOLOGY & ACID-FREE - Colors on Hammermill copy paper are 30% brighter.
blacks are up to 60% bolder, and inks dry 3 times faster for less smearing. Acid-free Hammermill paper also prevents printing and copier sheets from yellowing over time to ensure long-lasting archival quality.
RENEWABLE RESOURCE - Hammermill copy paper is Forest Stewardship Council (FSC) certified, contributing to “MR1 Performance” for paper and wood products under LEED.
Letter-size paper measures 8 1/2" x 11" to suit your printing needs.
Forest Stewardship Council® (FSC®) certified — made from wood/paper that comes from forests managed to rigorous environmental and social standards, supported by the world's leading conservation organizations.
Leadership forestry — from forests or sourcing programs that meet specific environmental standards, helping you support practices that better protect forests and the environment.

"""

existing_products = retrieve_info(odp_prd)
response = chain.run(product_description=odp_prd, existing_products=existing_products)


print(response)
