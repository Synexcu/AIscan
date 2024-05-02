import cv2
import numpy as np
import utils
# import sys
import argparse
# import libsql_experimental as libsql
from urllib.parse import urlparse, parse_qs
from subprocess import call
from caller import open_py_file
import subprocess
from AI import main
import json
from custom_encoder import NumpyEncoder

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(json_encoder=NumpyEncoder)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# url = "https://res.cloudinary.com/dszfasa7p/image/upload/v1714121161/py4tdockjqnkhs4fvnc4.jpg"

POSTS = [
    {
        'id': 1,
        'title': 'Post 1'
    },
    {
        'id': 2,
        'title': 'Post 2'
    },
    {
        'id': 3,
        'title': 'Post 3'
    },
]

@app.get('/ocr')
async def ocr(q: str = Query("bar", min_length=3), ans: str = Query(..., min_length=5), questions: int = Query(...), choices: int = Query(...)):
    # parsed_url = urlparse(image_url)
    # cloudinary_link = parsed_url.path
    # return {"cloudinary_link": cloudinary_link}

    results = {'ocr': [{'ocr': 'foo'}, 
                       {'ocr_link': {q}},
                       {'questions': {questions}},
                       {'choices': {choices}},
                       {'answers': {ans}}
                        ]}
    if q:
        # results.update({'q': q})
        ans = ans.replace(" ", "")
        q = q.replace("%2F", "/")
        q = q.replace("%3A", ":")

        # results.update({'answers': ans})
        myIndex, grading, score = main(q, questions, choices, ans)
        # results.update({'myIndex': myIndex})
        # results.update({'grading': grading})
        # results.update({'score': score})
        if myIndex is not None and grading is not None and score is not None:
            response = {
                'myIndex': myIndex,
                'grading': grading,
                'score': float(score)
            }
            return NumpyEncoder().encode(response)
        else:
            return {'error': 'Failed to process the image'}

    return results

@app.get('/health')
async def check():
    return {'Check health: health is good!'}

@app.get('/{id}')
async def get_one_post(id:int):
    post = [post for post in POSTS if post['id'] == id]
    return post[0]

# to run main.py server: uvicorn main:app --reload 