\# DYNAMIC KNOWLEDGE BASE CHATBOT USING RAG



\## Student Name

Sujata Mali



\## 1. Project Title



Dynamic Knowledge Base Chatbot Using Retrieval-Augmented Generation (RAG)



\## 2. Objective



The objective of this project is to develop a chatbot that can dynamically expand its knowledge base by periodically checking specified information sources.



New information is converted into vector embeddings and stored in a ChromaDB vector database. When a user asks a question, the chatbot retrieves relevant information and uses Google Gemini to generate the response.



The system does not require retraining the language model when new information is added.



\## 3. Problem Statement



Traditional chatbots require model retraining or manual modification when new information becomes available.



This project solves this problem by separating the chatbot's knowledge from the language model. New information can be added to the knowledge source and automatically indexed in the vector database.



\## 4. Technologies Used



\- Python

\- Streamlit

\- Google Gemini API

\- Google GenAI SDK

\- ChromaDB

\- Retrieval-Augmented Generation

\- Vector Embeddings

\- Python-dotenv

\- Schedule



\## 5. System Architecture



Knowledge Source

&#x20;       |

&#x20;       v

Change Detection

&#x20;       |

&#x20;       v

Text Chunking

&#x20;       |

&#x20;       v

Gemini Embedding

&#x20;       |

&#x20;       v

ChromaDB Vector Database

&#x20;       |

&#x20;       v

User Question

&#x20;       |

&#x20;       v

Question Embedding

&#x20;       |

&#x20;       v

Similarity Search

&#x20;       |

&#x20;       v

Relevant Context

&#x20;       |

&#x20;       v

Google Gemini

&#x20;       |

&#x20;       v

Final Answer



\## 6. Project Components



\### app.py



Provides the Streamlit graphical user interface.



Features:



\- User question input

\- Answer display

\- Knowledge-base update button



\### rag.py



Implements the Retrieval-Augmented Generation process.



It:



1\. Receives the user question.

2\. Creates an embedding.

3\. Searches ChromaDB.

4\. Retrieves relevant documents.

5\. Sends the context to Gemini.

6\. Generates the final answer.



\### updater.py



Updates the vector database.



It:



1\. Reads source files.

2\. Calculates file hashes.

3\. Detects changes.

4\. Splits text into chunks.

5\. Generates embeddings.

6\. Stores the embeddings in ChromaDB.



\### scheduler.py



Automatically checks the knowledge source periodically.



The scheduler runs the update process at a fixed interval.



\### knowledge.txt



Contains the chatbot's knowledge.



New information can be added to this file without retraining the language model.



\## 7. Dynamic Updating Mechanism



The system uses file hashing to detect changes.



If the source file has not changed:



&#x20;   No changes detected



If the source file has changed:



&#x20;   New or updated information found



The updated information is then processed and stored in the vector database.



\## 8. Retrieval-Augmented Generation



RAG allows the chatbot to retrieve relevant information before generating an answer.



This improves the chatbot because it can use information that was added after the language model was trained.



\## 9. Vector Database



ChromaDB is used as the vector database.



The system stores:



\- Text chunks

\- Vector embeddings

\- Document IDs



When a user asks a question, the question embedding is compared with stored embeddings to retrieve relevant information.



\## 10. Dynamic Knowledge Demonstration



Initially, the knowledge base contained information such as:



"Customers can contact support through email."



The chatbot was able to answer:



Question:



How can I contact customer support?



Answer:



Customers can contact support through email.



New information was then added:



"Premium customers receive priority support."



After updating the vector database, the chatbot answered:



Question:



Who receives priority support?



Answer:



Premium customers receive priority support.



This demonstrates that new information can be incorporated without retraining the language model.



\## 11. Automatic Scheduler



The scheduler periodically checks the source files.



Example:



&#x20;   Every 1 minute

&#x20;         |

&#x20;         v

&#x20;   Check source

&#x20;         |

&#x20;         v

&#x20;   Detect changes

&#x20;         |

&#x20;      Yes/No

&#x20;         |

&#x20;         v

&#x20;   Update vector database



For production use, the checking interval can be changed to hourly or another suitable period.



\## 12. Streamlit Interface



The Streamlit application provides a simple interface for users.



Users can:



\- Enter questions

\- Receive answers

\- Manually update the knowledge base



\## 13. Testing



\### Test 1



Question:



How can I contact customer support?



Expected result:



Customers can contact support through email.



Result:



PASS



\### Test 2



Question:



Who receives priority support?



Expected result:



Premium customers receive priority support.



Result:



PASS



\### Test 3



Question:



How can customers request a refund?



Expected result:



Customers can request a refund through the customer support portal.



Result:



PASS



\### Test 4



New information was added to the knowledge source.



The updater detected the change and updated ChromaDB.



Result:



PASS



\### Test 5



The scheduler automatically detected modified source information.



Result:



PASS



\## 14. Advantages



\- No model retraining required.

\- Easy to update knowledge.

\- Uses semantic search.

\- Supports automatic updates.

\- Simple user interface.

\- Knowledge can be maintained separately from the model.



\## 15. Future Enhancements



Future versions can include:



\- PDF document ingestion

\- Website data ingestion

\- Multiple knowledge sources

\- Automatic web crawling

\- Database integration

\- Cloud deployment

\- Chat history

\- Authentication

\- Source citations

\- Advanced monitoring



\## 16. Expected Outcome



The final system provides a chatbot that automatically incorporates new information into its responses over time.



The knowledge base can be updated independently of the language model, making the system easier to maintain and scale.



\## 17. Conclusion



The project successfully demonstrates a Dynamic Knowledge Base Chatbot using RAG, Gemini, and ChromaDB.



The system detects changes in knowledge sources, generates embeddings, updates the vector database, retrieves relevant information, and generates answers using Gemini.



The scheduler further enables periodic automatic updates, satisfying the requirement for a chatbot that can continuously incorporate new information.

