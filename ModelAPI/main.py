import pip
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import time
import json

#import BertlargeModel
import Seq2SeqModel


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class QnAItem(BaseModel):
    question: str
    model: str
    reviews: str


@app.post("/qna/")
async def qna(qnaItem: QnAItem):
    t0 = time.time()

    if qnaItem.model == "BiDAF":
        answer = BiDAFModel.question_answer(
            qnaItem.question, qnaItem.reviews)
    elif qnaItem.model == "DistilBERT":
        answer = DistilBERTModel.question_answer(
            qnaItem.question, qnaItem.reviews)
    elif qnaItem.model == "Longformer":
        answer = LongformerModel.question_answer(
            qnaItem.question, qnaItem.reviews)
    elif qnaItem.model == "RoBERTa":
        answer = RoBERTaModel.question_answer(
            qnaItem.question, qnaItem.reviews)
    elif qnaItem.model == "Seq2Seq":
        answer = Seq2SeqModel.question_answer(
            qnaItem.question, qnaItem.reviews)
    elif qnaItem.model == "Unsupervised":
        answer = UnsupervisedModel.question_answer(
            qnaItem.question, qnaItem.reviews)
    else:
        answer = BertlargeModel.question_answer(
            qnaItem.question, qnaItem.reviews)

    t1 = time.time()
    total = t1-t0

    resp = {"model": qnaItem.model, 'question': qnaItem.question,
            'answer': answer, "time": total}

    return resp
