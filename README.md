Relevance-Feedback
==================

This is an implement of an information retrieval system that exploits user-provided relevance feedback to improve the search results returned by Bing. The relevance feedback mechanism is based on the seminal paper "Singhal: Modern Information Retrieval: A Brief Overview, IEEE Data Engineering Bulletin, 2001". A copy of the research paper can be found here: http://www.cs.columbia.edu/~gravano/cs6111/Readings/singhal.pdf

User queries are often ambiguous. For example, a user who issues a query [jaguar] might be after documents about the car or the animal, and—in fact—search engines like Bing and Google return pages on both topics among their top 10 results for the query. In this project, we have designed and implemented a query-reformulation system to disambiguate queries and—hopefully—improve the relevance of the query results that are produced. Here’s how the system works:

1. It receives as input a user query, which is simply a list of words, and a value—between 0 and 1—for the target “precision@10” (i.e., for the precision that is desired for the top-10 results for the query, which is the fraction of pages that are relevant out of the top-10 results).
2.We retrieve the top-10 results for the query from Bing, using the Bing Search API, using the default value for the various Bing parameters, without modifying these default values.
3. We present these results to the user, so that the user can mark all the web pages that are relevant to the intended meaning of the query among the top-10 results. For each page in the query result, we display its title, URL, and description returned by Bing.

If the precision@10 of the results from Step 2 for the relevance judgments of Step 3 is greater than or equal to the target value, then we stop. If the precision@10 of the results is zero, then also we stop. Otherwise, we use the pages marked as relevant to automatically (i.e., with no further human input at this point) derive new words that are likely to identify more relevant pages. We modify the current user query by adding to it the newly derived words in the best possible order, as determined in Step 4, and go to Step 2.
