import os
from pathlib import Path
# from util import *
# from eval import *
# from dataset import get_dataset
from prompts import PromptFactory
from model import get_model
from tqdm import tqdm
# from pprint import pprint


def launch():
    # configure prompt
    prompter = PromptFactory().get('simple_prompting')

    # get model
    model = get_model(model_name='gpt-4o-mini-2024-07-18', temperature=0.0, api_key='')
    model.set_post_process_fn(prompter.post_process_fn)
    prompt = prompter.fill()
    pred, info = model.forward(prompter.head, prompt)
    
    print(f"pred: {pred}\n\n")
    print(f"info: {info}")

if __name__ == '__main__':
    launch()
