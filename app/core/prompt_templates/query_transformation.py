query_transformation = """
You need to generate database query for data retrieval based on the following conversation between user and assistant.
You need to generate query that can be used to retrieve relevant information to generate answer to current user question.
The query should be a short sentence or phrase that include the information content that user wanna know.

Here is the conversation.
{conversation}

Here is the user's query.
{query}
"""