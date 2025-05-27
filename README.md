# NLP
My own personal exploration using LLMs and NLP Concepts. A more in-depth rundown of each project coming soon



## Project Video to PPT

Since the explosion of LLMs, summarising content has remained an evergreen usecase. The extension to summarising youtube videos is incredibly useful because listening takes time. We can't skim through videos the way we skim through text. VideoPPT focuses on bringing LLM retrieval capabilities to multiple youtube videos.

The designs and concepts generated will be simple. This project operates on the assumption the presenter will fine-tune the script, design, and content based on their own presentation style. The focus is on building a good skeleton to get started.

Here's how it works 

- Takes in a youtube url and generates transcripts
- Using the indexed documents, the OpenAI LLM model will generate a structured presentation plan
- Load and generate a simple presentation using presentation-pptx 

More capabilities to be introduced:

1. Support for multiple youtube urls
2. Generating images 
3. Customise presentation length and target audience
4. Memory integration for re-prompting to generate the best possible content skeletons
