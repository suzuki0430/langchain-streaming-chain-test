import logging
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.callbacks.base import BaseCallbackHandler
from dotenv import load_dotenv
from queue import Queue
from threading import Thread

load_dotenv()


class StreamingHandler(BaseCallbackHandler):
    def __init__(self, queue):
        self.queue = queue

    def on_llm_new_token(self, token, **kwargs):
        self.queue.put(token)

    def on_llm_end(self, response, **kwargs):
        self.queue.put(None)

    def on_llm_error(self, error, **kwargs):
        logging.error(f"Error in LLM: {error}")
        self.queue.put(None)


# 分割された出力をqueueにいれる
chat = ChatOpenAI(
    streaming=True,
    # callbacks=[StreamingHandler()]
)

prompt = ChatPromptTemplate.from_messages([
    ("human", "{content}")
])


class StreamingChain:
    def __init__(self, llm, prompt):
        self.llm_chain = LLMChain(llm=llm, prompt=prompt)
        self.thread = None

    def stream(self, input):
        queue = Queue()
        handler = StreamingHandler(queue)

        def task():
            # 内部的に __call__ メソッドを呼び出し、入力された内容（input）に基づいてLLMを起動し、その結果を生成するプロセスを開始する
            # self(input, callbacks=[handler])
            self.llm_chain(input, callbacks=[handler])

        # task 関数を別スレッドで実行する。.start() メソッドを呼び出すことで、スレッドが開始される。この実装により、self(input) の処理がバックグラウンドで実行される間に、メインスレッドは queue からトークンを取得し続けることができる
        self.thread = Thread(target=task)
        self.thread.start()

        try:
            while True:
                token = queue.get()
                if token is None:
                    break
                yield token  # yield token は、token を生成し、それを関数の呼び出し元に返すために使用される。この方法により、関数はジェネレータとして振る舞い、ストリーミング処理や遅延評価が可能になる
        finally:
            self.cleanup()

    def cleanup(self):
        if self.thread and self.thread.is_alive():
            self.thread.join()


chain = StreamingChain(llm=chat, prompt=prompt)

for output in chain.stream(input={"content": "Explain Pokémon in 100 characters"}):
    print(output)
