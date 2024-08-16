import:py from mtllm.llms {OpenAI}
import:py from exa_py {Exa}
import:py os;
import:py from loguru {logger}
import:py from rich.console {Console}
import:py time;

glob exa = Exa(os.getenv("EXA_API_KEY"));
glob llm = OpenAI(model_name="gpt-4o-mini");
glob console = Console(width=100);

obj SearchResult {
    has title: str, url: str, summary: 'Comprehensive summary with minimum amount of words': str;
}

can 'Search the Internet and Get Relevant Information'
search(query: str) -> list[SearchResult] {
    can 'Summarize the Content with respect to the query.'
    summarize_content(content: list[str], query: str) -> 'Comprehensive summary with minimum amount of words': str
    by llm(context=["Ignoring the irrelevant information, summarize the content with respect to the query."]);

    with console.status(f"Searching the Web... {query}") {
        exa_results = exa.search_and_contents(query, <>type="neural", use_autoprompt=True, num_results=4, highlights=True);
    }
    with console.status("Reading the Web...") {
        return [
            {
                "title": result.title,
                "url": result.url,
                "content": summarize_content(result.highlights, query)
            } for result in exa_results.results
        ];
    }
}



obj Answer {
    has question_asked: str, related_sources: list[str], answer: str;
}

can 'Summarize the Chat History'
summarize_chat_history(chat_history: list[Answer]) -> 'Summary': str by llm();

can 'Get Answer to the Question, Consider the summary of chat history if given'
get_answer(question: str, chat_history_summary: str = "") -> Answer
by llm(method="ReAct", tools=[search], context=["If the question can be answered with your knowledge, answer it. Otherwise, search the web."]);

with entry: __main__ {
    console.print("\nPerplexcity AI Clone\nType 'exit' to exit the chat.", style="bold blue");
    chat_history = [];
    while True {
        console.print();
        console.rule("Question");
        question = console.input("Ask me a anything: ");
        if question == "exit" {break;}

        start_time = time.time();
        chat_summary = summarize_chat_history(chat_history) if chat_history else "";
        answer = get_answer(question, chat_summary);
        chat_history.append(answer);
        end_time = time.time();
        
        console.rule(f"Answer (Took {end_time - start_time} seconds)");
        console.print(answer.answer);
        if answer.related_sources {
            console.rule("Related Sources");
            console.print(" | ".join(answer.related_sources));
        }
    }
}