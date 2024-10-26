# Loading Libraries 
import os
import json
import faiss

from llama_index.core import Document, VectorStoreIndex, SimpleDirectoryReader, StorageContext
from llama_index.vector_stores.faiss import FaissVectorStore

def get_articles(text):
    """ This function splits the regulation text into documents (articles) but also keeps additional information in metafata """
    docs = []

    # Split the text in chapters based on the ^^^ marker
    chapters = text.split('^^^')               
    for chapter in chapters:
        if not chapter:
            continue 
        lines = chapter.split('\n')
        chapter_title = lines[0].strip("^^^")  
        
        # Split the text in articles based on the @@@ marker
        articles = chapter.split('@@@')
        # Delete the first item which refers to the Chapter
        del articles[0]                        
        
        # Remove empty strings and strip whitespace
        articles = [article.strip() for article in articles if article.strip()]

        # Prepare the final list of articles
        for article in articles:
            
            lines = article.split('\n')
            
            # Remove empty lines and strip whitespace
            lines = [line.strip() for line in lines if line.strip()]

            # Extract the article number and title from the first line
            firstline  = lines[0].strip()  # the first sentence of each article is of "Article x" form
            number = firstline.split()[1].strip()   # Assumes format "Article X" to get the number of the article
            article_title = lines[1].strip()  
            
            if "Article" in firstline:      
                content = '\n'.join(lines[2:]).strip()  # Extract the article content from the third line and the nect
                doc = Document(
                    text=content, 
                    metadata={"Chapter_Title": chapter_title, 
                              "Article_Title": article_title,
                             "Article_Number": number, 
                             },
                    excluded_embed_metadata_keys=["Article_Number"],# Exclude article number not to affect text interpretation 
                    excluded_llm_metadata_keys=["Article_Number"]
                    )
                docs.append(doc)
    return docs

# Loading Files
file_path = "./source/SCA_2018_10_Scource.docx"
original_documents = SimpleDirectoryReader(input_files=[file_path]).load_data() 
source_text = original_documents[0].text

# Creating separate documewnts per article
documents = get_articles(source_text)

# dimensions of text-ada-embedding-002
d = 1536
faiss_index = faiss.IndexFlatL2(d)

# Embedding the text of documents
vector_store = FaissVectorStore(faiss_index=faiss_index)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(documents, 
                                        storage_context=storage_context,
                                        show_progress=True,
                                        )

# save embedded data to disk
index.storage_context.persist("./FAISS storage/")