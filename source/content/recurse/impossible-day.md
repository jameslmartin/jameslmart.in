Title: Impossible Day at RC, LLM tooling crash course
Date: 2024-11-20 12:50
Category: recurse
Tags: tech, llm, langchain, recurse
Slug: llm-crash-course-one
Authors: james
Summary: Stepping through storing embeddings in a vector database for a popular algorithms textbook

For Impossible Day, I decided to attempt an entire research project that I've been kicking around. Document chat is 100% a solved problem. Modern "AI" tools can retrieve and summarize information from pretty much anything you can digitize. Most LLMs like the ones behind Chat-GPT or Llama are also trained on such huge corpuses of books and information, they probably already encompass whatever an individual has in their digital library.

I have a small collection of PDFs and ePub format books that I like to revisit or skim when I'm toying with a problem. While I prefer more analog methods of lookup, I've been curious how I might perform something like retrieval-augmented generation ([RAG](https://en.wikipedia.org/wiki/Retrieval-augmented_generation)) or document chat with my own library without the use of something like OpenAI or some other existing product.

What would it take to "homebrew" one of these pipelines? I decided to travel back to May 2015 to the semester of grad school I took a formal Machine Learning course to revisit matrix multiplication, mean pooling, and vectorization. My first objective was to generate embeddings for [Introduction to Algorithms](https://en.wikipedia.org/wiki/Introduction_to_Algorithms), aka CLRS, to eventually perform RAG on basic algorithm/data structure related questions.

My main intention of this project was to familiarize myself with the ever evolving state of LLM tooling rather than create something novel. I have a cursory understanding of some of the underlying concepts of LLMs, including embedding spaces and basic neural net architecture, but it's been almost a decade since I sat down and implemented any of it myself. I also knew that my first step would be to perform some sort of document chunking and convert those chunks to embeddings. I've found there are lots of tools off the shelf that can handle this entire process of storing embeddings for you, including the encoding of the document text itself.

I quickly found that:
1. There exists tools to read PDFs (or any document for that matter) into a Pydantic model that other tooling uses
2. There exists tools to then store those documents _as embeddings_ in a vector database, removing the need to create the embeddings beforehand.

Langchain has tooling to do both (1) and (2) and make it all play nicely with each other. However, langchain can box you into using text embedding models or tools from OpenAI or Cohere, which I felt was unnecessary, especially if you could just download a smaller but comparable model from Hugging Face and load it locally (given enough local compute, of course). I also wanted to explore (2) more deeply rather than just use some off-the-shelf-tool (like Pinecone or ChromaDB) and wanted to look into what it would take to create the embeddings, then store those embeddings myself in a vector database like pgvector. I knew to create those embeddings myself, I needed to break the problem down into a few more steps:

1. Create semantically rich document chunks by including metadata and linking to previous and next chunks. 
2. Use a pretrained LLM to tokenize the document chunks
3. Use a pretrained LLM to encode the tokenized chunks into the embedding space
4. Run a Postgres database locally (likely in a Docker container) and create a migration for the schema
5. Write a db client/db model and store embeddings in the vector database

The end goal would be to populate a locally running postgres database with embeddings. I work enough with postgres to know how to roll my own database client using something like psycopg or SqlAlchemy, but for Impossible Day, this seemed pretty tedious and not a good use of time. I also wasn't entirely clear on what the database model should actually look like, either. Enter another langchain tool, PGVector! This cut out so much time but learned that PGVector does not just store the vectors post-embedding, it will also create the embeddings for you. Langchain even includes a command to spin up a postgres Docker container in their documentation. After creating the container, it was time to get a connection to the database. The interface to spinning up a PGVector database looks like:

```python
from langchain_postgres.vectorstores import PGVector

collection_name = "librarian"
connection = "postgresql+psycopg://langchain:langchain@localhost:6024/langchain"

vector_store = PGVector(
    embeddings=embeddings, # We'll need to define this!!
    collection_name=collection_name,
    connection=connection,
    use_jsonb=True,
)
```

The `embeddings` parameter to PGVector has to be an implementation of this [class](https://python.langchain.com/api_reference/_modules/langchain_core/embeddings/embeddings.html#Embeddings). Off the shelf, you can use OpenAI embeddings or Cohere embeddings. Or... if you're following my path and want to use a model you have locally, you can implement the class yourself.

So first, I needed a tokenizer and a text embedding model:
```python
from transformers import AutoModel, AutoTokenizer
from langchain.document_loaders import PyPDFLoader #, PyPDFDirectoryLoader

nomic_1_5 = "nomic-ai/nomic-embed-text-v1.5"
embeddings_model = AutoModel.from_pretrained(nomic_1_5, trust_remote_code=True)
tokenizer = AutoTokenizer.from_pretrained(nomic_1_5)
embeddings_model.eval()
```

I'm pretty new to AutoModel and AutoTokenizers, so I spent a lot of time struggling to figure out what to do with the instances they return, but eventually I reached implementing my own Embeddings class. I extended the abstract base class linked above:

```python
from langchain_core.embeddings.embeddings import Embeddings
import torch
import torch.nn.functional as F


def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output[0]
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)


class CustomEmbeddings(Embeddings):
    def __init__(self, model, tokenizer):
        self._model = model
        self._tokenizer = tokenizer

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        embeddings = []
        # https://huggingface.co/nomic-ai/nomic-embed-text-v1.5
        for text in texts:
            encoded_chunk = self._tokenizer(text, padding=True, truncation=True, return_tensors='pt')
            with torch.no_grad():
                model_output = self._model(**encoded_chunk)
            pooled_embeddings = mean_pooling(model_output, encoded_chunk['attention_mask'])
            embeddings.append(torch.flatten(F.normalize(pooled_embeddings, p=2, dim=1)))
        return embeddings

    def embed_query(self, text: Document) -> list[float]:
        return self.embed_documents([text])[0]
```

With this `CustomEmbeddings`, I created an instance passing my local model and tokenizer. I could then pass that instance to my PGVector database like so:

```python
embeddings_for_pgvector = CustomEmbeddings(embeddings_model, tokenizer)

vector_store = PGVector(
    embeddings=embeddings_for_pgvector, # Aye, there's the rub!
    collection_name=collection_name,
    connection=connection,
    use_jsonb=True,
)
```

And then things... just work!!?? 
```python
# assuming documents is a list of [Document] objects
vector_store.add_documents(documents, ids=[uuid4() for doc in test_batch])
```

I stepped through the langchain PGVector code enough to make sense of the signature:
```python
def embed_documents(self, texts: list[str]) -> list[list[float]]:
    ...
``` 
`texts` in this case is the `page_content` pulled off the core Pydantic `Document` model that the langchain document loaders use. So the custom embeddings class doesn't have much control in creating more semantically rich chunks before creating embeddings, as it only has access to the textual page content. Though in this research project's case, we are only trying to store embeddings from a single document, so everything in the `texts` list will be from a single document.

One gotcha I found was that the insert that langchain does under the hood (with SqlAlchemy) can only convert a tensor with "one element" to a scalar. Using `normalize` on the embeddings and specifying `dim=1` on the embeddings that have been run through `mean_pooling` did yield a tensor with one dimension, but for some reason PGVector couldn't handle it. I used torch.flatten to reduce the tensor to a vector. In theory, this shouldn't effect the values or dimension of the vector, but I haven't tested it!

This did make PGVector happy, and I loaded all 1300 chunks of CLRS into a vector database. Then... a quick test!

```python
vector_store.similarity_search('efficiency of insert binary search tree', k=10)
```

Yields some documents related to the query:
```
Document(id='4c639a6a-1d8d-41e6-8f32-a4cec04d8290', metadata={'page': 314, 'source': '../knowledge_base/CLRS.pdf'}, page_content='294 Chapter 12 Binary Search Trees\n12.2-8\nProve that no matter what node we start at in a height- h binary search tree, k\nsuccessive calls to TREE -SUCCESSOR take O.k Ch/ time.\n12.2-9\nLet T be a binary search tree whose keys are distinct, letx be a leaf node, and lety\nbe its parent. Show that y:key is either the smallest key in T larger than x: key or\nthe largest key in T smaller than x: key.\n12.3 Insertion and deletion\nThe operations of insertion and deletion cause the dynamic set represented by a\nbinary search tree to change. The data structure must be modiﬁed to reﬂect this\nchange, but in such a way that the binary-search-tree property continues to hold.\nAs we shall see, modifying the tree to insert a new element is relatively straight-\nforward, but handling deletion is somewhat more intricate.\nInsertion\nTo insert a new value /ETBinto a binary search tree T ,w eu s et h ep r o c e d u r eTREE -\nINSERT .T h e p r o c e d u r e t a k e s a n o d e´ for which ´: key D /ETB, ´: left D NIL ,\nand ´: right DNIL .I tm o d i ﬁ e sT and some of the attributes of´ in such a way that\nit inserts ´ into an appropriate position in the tree.\nTREE -INSERT .T; ´/\n1 y DNIL\n2 x DT:root\n3 while x €NIL\n4 y Dx\n5 if ´: key <x :key\n6 x Dx: left\n7 else x Dx: right\n8 ´: p Dy\n9 if y == NIL\n10 T:root D´ // tree T was empty\n11 elseif ´: key <y :key\n12 y:left D´\n13 else y:right D´')
```

Clearly, the document loader needs some optimizing and we could clean up the text in the document chunks but we're pretty close!
