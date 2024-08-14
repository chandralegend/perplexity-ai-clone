import:py from mtllm.llms {OpenAI}
import:py from exa_py {Exa}
import:py os;
import:py from loguru {logger}

glob exa = Exa(os.getenv("EXA_API_KEY"));
glob llm = OpenAI(model_name="gpt-4o-mini");

obj SearchResult {
    has title: str, url: str, summary: 'Comprehensive summary with minimum amount of words': str;
}

can 'Search the Internet and Get Relevant Information'
search(query: str) -> list[SearchResult] {
    logger.info(f"Searching for: {query}");

    can 'Summarize the Content with respect to the query.'
    summarize_content(content: str, query: str) -> 'Comprehensive summary with minimum amount of words': str
    by llm(context=["Ignoring the irrelevant information, summarize the content with respect to the query."]);

    exa_results = exa.search_and_contents(query, <>type="neural", use_autoprompt=True, num_results=4, text=True);

    return [
        {
            "title": result.title,
            "url": result.url,
            "content": summarize_content(result.text, query)
        } for result in exa_results.results
    ];
}

obj Answer {
    has question_asked: str, related_sources: list[str], answer: str;
}

can 'Summarize the Chat History'
summarize_chat_history(chat_history: list[Answer]) -> 'Summary': str by llm();

can 'Get Answer to the Question, Consider the summary of chat history if given'
get_answer(question: str, chat_history_summary: str = "") -> Answer
by llm(method="ReAct", tools=[search]);

with entry {
    chat_history = [];
    while True {
        question = input("Ask a question: ");
        if question == "exit" {
            break;
        }
        chat_summary = summarize_chat_history(chat_history) if chat_history else "";
        logger.info(f"Chat summary: {chat_summary}");
        answer = get_answer(question, chat_summary);
        chat_history.append(answer);

        print("Related sources: ", answer.related_sources);
        print("Answer: ", answer.answer);
    }
}