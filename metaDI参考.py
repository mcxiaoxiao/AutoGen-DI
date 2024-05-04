import asyncio
import sys
import json
from metagpt.logs import logger
from metagpt.roles.di.data_interpreter import DataInterpreter

from metagpt.utils.recovery_util import save_history
import faiss
import numpy as np
import csv

import requests
async def main(requirement: str = ""):
    
    embedding_dim = 1536

    # 加载 Faiss 索引
    index_file = "faiss_index.index"

    index = faiss.read_index(index_file)

    # 加载 QA 数据
    qa_data_file = "qa_data.csv"

    # 定义函数获取嵌入向量
    def get_embedding(text, model="text-embedding-ada-002"):
        url = "https://api.openai.com/v1/embeddings"
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer sk-xxxxx"
        }
        data = {
            "input": text,
            "model": model
        }
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response_data = response.json()
        embedding = response_data['data'][0]['embedding']
        return embedding
    

    # 定义函数根据当前问题查找答案
    def search_answer(question, index, questions, answers):
        question_embedding = get_embedding(question)
        question_embedding = np.array([question_embedding]).astype('float32')  # 将查询向量转换为二维数组

        # 在 Faiss 索引中搜索最相似的嵌入向量
        top_k = 1  # 返回前1个最相似的结果
        _, indices = index.search(question_embedding, top_k)

        # 根据索引获取相似的答案
        result = []
        for idx in indices[0]:
            question = questions[idx]
            answer = answers[idx]
            result.append((question, answer))

        return result

    # 读取 QA 数据并存储问题和答案
    questions = []
    answers = []

    with open(qa_data_file, "r") as f:
        reader = csv.reader(f)
        next(reader)  # 跳过标题行
        for row in reader:
            question = row[0]
            answer = row[1]
            questions.append(question)
            answers.append(answer)

    # 示例使用
    question = requirement
    results = search_answer(question, index, questions, answers)

    examples = ""

    # 将问题和答案添加到字符串中
    for question, answer in results:
        examples += "Question: " + question + "\n"
        examples += "Answer: " + answer + "\n\n"

    di = DataInterpreter(react_mode="react", tools=["PredictFd","PredictCyl"])
    rsp = await di.run(requirement+"\n/*以下是可以参考的相关问题和代码案例*/\n"+examples)
    logger.info(rsp)
    save_history(role=di)


if __name__ == "__main__":
    requirement = "画个图，展示3天内光伏发电量和风电发电量的预测数据变化情况。图片标题注明日期范围其中标题中日期要用-隔开的"

    asyncio.run(main(requirement))
