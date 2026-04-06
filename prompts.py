from string import Template
import re

def identity(res):
    return res
    
class PromptTemplate(object):
    def __init__(self, head, template, post_process_fn):
        self.head = head
        self.prompt_template = template
        self.post_process_fn = post_process_fn

    def get_num_stages(self):
        return len(self.template)

    def get_template_str(self):
        template = []
        for temp in self.prompt_template:
            template.append(temp.safe_substitute())
        return template

    def fill(self):
        # match variable names: duration, narration, question, optionA, optionB, optionC, optionD, optionE, num_words
        prompt_filled = []

    

        for temp in self.prompt_template:
            prompt_filled.append(temp)
            
        return prompt_filled

class PromptFactory(object):
    def __init__(self):
        self.prompt_templates = self.build()
    
    def build(self):
        prompt_templates = {}
        
        prompt_templates['simple_prompting'] = PromptTemplate(
            head = "You are presented with a textual description of a video clip, it consists of captions of multiple objects and scene. Also, a score is given to the object and the scene description. Description with a higher score is the more important description for solving the problem. Your task is to answer a question related to this video, choosing the correct option out of five possible answers. Please provide the answer with a single-letter (A, B, C, D, E)" + \
                "It is crucial that you imagine the visual scene as vividly as possible to enhance the accuracy of your response." + \
                "Please provide a concise one-sentence explanation for your chosen answer. If you are uncertain about the correct option, select the one that seems closest to being correct.",
            template = ["###\n\nDescription\nScene: The boy is standing next to the bench and sprinkling water on the girl. The woman runs to the boy. The boy runs away. The boy comes back to the bench, and pick up the hose. The boy is sprinkiling to the camera.\n\nObject1: The boy is sparkling. The boy is running. The boy is standing. The boy picks up something. The boy sits down and stands up. The boy is sparkling. The boy is running. The boy is standing.\n\nObject2: The woman is avoiding. The woman is running. The woman raises hands. The woman is standing. The woman is running. \n\n---\n\nScores\nScene: 8\nObject1: 7\nObject2: 3\n\n---\n\nQuestion: why did the boy run near the bench after running back from the other side\n\nOptions:\nA: pick up the pipe\nB: catch the toy\nC: looking at tablet\nD: hit the drum set\nE: sit on bench\n\n---\n\nThe prediction, explanation, confidence is (please respond in the format of 'prediction: \n explanation: \n confidence: \n'):"],
            post_process_fn = identity
        )

        # # egoschema QA cap score
        # prompt_templates['cap_score'] = PromptTemplate(
        #     head = "You are presented with a textual description of a first view video clip, it consists of N sparsely sampled from the video (#C means the first person view, and #O indicates another). The ultimate goal is to answer a question related to this video, choosing the correct option out of five possible answers. Please provide the answer with a single-letter (A, B, C, D, E)" + \
        #                 "It is crucial that you imagine the visual scene as vividly as possible to enhance the accuracy of your response. After selecting your answer, rate your confidence level in this choice on a scale from 1 to 100, where 1 indicates low confidence and 100 signifies high confidence. " + \
        #                 "Please provide a concise one-sentence explanation for your chosen answer. If you are uncertain about the correct option, select the one that seems closest to being correct. " + \
        #                 "Meanwhile, could you provide a relevance score for each frame caption to evaluate their relevance with the query-answering process. The score is between 1,2,3, where 1 indicates low relevance and 3 signifies high relevance. Please return the relevance score in the format of a list of N scores.",
        #     template = [
        #         Template("Description: $narration \n\n###\n\n Questions: $question \n Options: \n A: $optionA \n B: $optionB \n C: $optionC \n D: $optionD \n E: $optionE \n\n###\n\n The prediction, explanation, confidence is (please response in the format of 'prediction: \n explanation: \n confidence: \n frame relevance: \n'):"),
        #     ],
        #     post_process_fn = update_relevance_response
        # )

        # # egoschema QA 
        # prompt_templates['qa_standard'] = PromptTemplate(
        #     head = "You are presented with a textual description of a video clip, it consists of frame captions sparsely sampled from the video. Your task is to answer a question related to this video, choosing the correct option out of five possible answers. Please provide the answer with a single-letter (A, B, C, D, E)" + \
        #                 "It is crucial that you imagine the visual scene as vividly as possible to enhance the accuracy of your response. After selecting your answer, rate your confidence level in this choice on a scale from 1 to 100, where 1 indicates low confidence and 100 signifies high confidence. " + \
        #                 "Please provide a concise one-sentence explanation for your chosen answer. If you are uncertain about the correct option, select the one that seems closest to being correct. ",
        #     template = [
        #         Template("Here are a few examples. \n${examplars} \n\n###\n\n  Description: $narration \n\n###\n\n Questions: $question \n Options: \n A: $optionA \n B: $optionB \n C: $optionC \n D: $optionD \n E: $optionE \n\n###\n\n The prediction, explanation, confidence is (please response in the format of 'prediction: \n explanation: \n confidence: \n '):"),
        #     ],
        #     post_process_fn = update_pred_response
        # )


        # # egoschema QA (raw captions as input) few-shot
        # prompt_templates['qa_standard_fewshot'] = PromptTemplate(
        #     head = "You are a helpful expert in first person view video analysis.",
        #     template = [
        #         Template("You are given some language descriptions of a first person view video. The video is $duration seconds long. You are also given a question and five potential choices. Your task is to answer with a correct choice based on the video descriptions. \nHere are a few examples. \n${examplars}\n\n Now answer this question.\nDescriptions: ${narration}.\n Question: ${question}\n A: ${optionA}.\n B: ${optionB}.\n C: ${optionC}.\n D: ${optionD}.\n E: ${optionE}.\n Answer: "),
        #     ],
        #     post_process_fn = first_char_as_answer
        # )
        
        # # egoschema QA (summary as input)
        # prompt_templates['qa_sum'] = PromptTemplate(
        #     head = "You are a helpful expert in first person view video analysis.",
        #     template = [
        #         Template("Please provide a single-letter answer (A, B, C, D, E) to the following multiple-choice question, and your answer must be one of the letters (A, B, C, D, or E). You must not provide any other response or explanation. You are given some language descriptions of a first person view video. The video is $duration seconds long. Here are the descriptions: $narration.\n You are going to answer a multiple choice question based on the descriptions, and your answer should be a single letter chosen from the choices.\n Here is the question: $question.\n Here are the choices.\n A: $optionA\n B: $optionB\n C: $optionC\n D: $optionD\n E: $optionE\n"),
        #     ],
        #     post_process_fn = first_char_as_answer
        # )

        # # egoschema sum (standard)
        # prompt_templates['sum_standard'] = PromptTemplate(
        #     head = "You are a helpful expert in first person view video analysis.",
        #     template = [
        #         Template('You are given some language descriptions of a first person view video. The video is $duration seconds long. Each sentence describes a ${clip_length}s clip. Here are the descriptions: $narration.\n Please give me a $num_words words summary.')
        #     ],
        #     post_process_fn = identity
        # )


        # # egoschema sum (q) orginal
        # prompt_templates['sum_q'] = PromptTemplate(
        #     head = "You are a helpful expert in first person view video analysis.",
        #     template = [
        #         Template('You are given some language descriptions of a first person view video. The video is $duration seconds long. Each sentence describes a ${clip_length}s clip. The descriptions are sequential and non-overlapping which cover the whole video exactly. Here are the descriptions: $narration.\n Please give me a $num_words words summary. When doing summarization, remember that your summary will be used to answer this multiple choice question: $question'),
        #     ],
        #     post_process_fn = identity
        # )

        # # egoschema sum (qa)
        # prompt_templates['sum_qa'] = PromptTemplate(
        #     head = "You are a helpful expert in first person view video analysis.",
        #     template = [
        #         Template('You are given some language descriptions of a first person view video. The video is $duration seconds long. Each sentence describes a ${clip_length}s clip. Here are the descriptions: $narration.\n Please give me a $num_words words summary. When doing summarization, remember that your summary will be used to answer this multiple choice question: $question\n Here are the choices.\n A: $optionA\n B: $optionB\n C: $optionC\n D: $optionD\n E: $optionE\n Do not answer this question directly. Instead, use the question and choices to guide your summary.')
        #     ],
        #     post_process_fn = identity
        # )

        # # egoschema QA zero-shot-CoT
        # prompt_templates['qa_zs-cot'] = PromptTemplate(
        #     head = "You are a helpful expert in first person view video analysis.",
        #     template = [
        #         Template("You are given some language descriptions of a first person view video. The video is $duration seconds long. Each sentence describes a ${clip_length}s clip. Here are the descriptions: $narration.\n You are going to answer a multiple choice question based on the descriptions, and your answer should be a single letter chosen from the choices.\n Here is the question: $question.\n Here are the choices.\n A: $optionA\n B: $optionB\n C: $optionC\n D: $optionD\n E: $optionE\n Before answering this question, let's think step by step."),
        #         Template("Please provide a single-letter answer (A, B, C, D, E) to the multiple-choice question, and your answer must be one of the letters (A, B, C, D, or E). You must not provide any other response or explanation. Your response should only contain one letter.")
        #     ],
        #     post_process_fn = first_char_as_answer
        # )

        # # egoschema QA plan-and-solve
        # prompt_templates['qa_plansolve'] = PromptTemplate(
        #     head = "You are a helpful expert in first person view video analysis.",
        #     template = [
        #         Template("You are given some language descriptions of a first person view video. The video is $duration seconds long. Each sentence describes a ${clip_length}s clip. Here are the descriptions: $narration.\n You are going to answer a multiple choice question based on the descriptions, and your answer should be a single letter chosen from the choices.\n Here is the question: $question.\n Here are the choices.\n A: $optionA\n B: $optionB\n C: $optionC\n D: $optionD\n E: $optionE\n To answer this question, let's first prepare relevant information and decompose it into 3 sub-questions. Then, let's answer the sub-questions one by one. Finally, let's answer the multiple choice question."),
        #         Template("Please provide a single-letter answer (A, B, C, D, E) to the multiple-choice question, and your answer must be one of the letters (A, B, C, D, or E). You must not provide any other response or explanation. Your response should only contain one letter.")
        #     ],
        #     post_process_fn = first_char_as_answer
        # )

        # # next-qa QA, intentQA QA
        # prompt_templates['qa_next'] = PromptTemplate(
        #     head = "You are a helpful expert in first person view video analysis.",
        #     template = [
        #         Template("Here are some examples:\n$examplars\n\n###\n\nPlease provide a single-letter answer (A, B, C, D, E) to the following multiple-choice question, and your answer must be one of the letters (A, B, C, D, or E). You must not provide any other response or explanation. If you are not sure, answer with the most likely answer. You are given some language descriptions of a first person view video. The video is 1 FPS and the descriptions are the captions every 2 frames. Each caption starts with the frame number.\nHere are the descriptions:\n$narration\n Here is the question: $question?\n Here are the choices:\n (A): $optionA\n (B): $optionB\n (C): $optionC\n (D): $optionD\n (E): $optionE\n"),
        #     ],
        #     post_process_fn = first_char_as_answer
        # )



        # # next-qa QA, intentQA QA relevance scoring
        # prompt_templates['next_rel'] = PromptTemplate(
        #     head = "You are presented with a textual description of a video, it consists of N frame captions sparsely sampled from the video (#C means the first person view, and #O indicates another). The ultimate goal is to answer a question related to this video, choosing the correct option out of five possible answers. Please provide the answer with a single-letter (A, B, C, D, E)" + \
        #                 "It is crucial that you imagine the visual scene as vividly as possible to enhance the accuracy of your response. After selecting your answer, rate your confidence level in this choice on a scale from 1 to 100, where 1 indicates low confidence and 100 signifies high confidence. " + \
        #                 "Please provide a concise one-sentence explanation for your chosen answer. If you are uncertain about the correct option, select the one that seems closest to being correct. " + \
        #                 "Meanwhile, could you provide a relevance score for each frame caption to evaluate their relevance with the query-answering process. The score is between 1,2,3, where 1 indicates low relevance and 3 signifies high relevance. Please return the relevance score in the format of a list of N scores.",
        #     template = [
        #         Template("Description: $narration \n\n###\n\n Questions: $question \n Options: \n A: $optionA \n B: $optionB \n C: $optionC \n D: $optionD \n E: $optionE \n\n###\n\n The prediction, explanation, confidence is (please response in the format of 'prediction: \n explanation: \n confidence: \n frame relevance: \n'):"),
        #     ],
        #     post_process_fn = update_relevance_response
        # )


        

        # # next-qa QA, intentQA QA  question answering
        # prompt_templates['next_neo'] = PromptTemplate(
        #     head = "You are presented with a textual description of a video, it consists of frame captions sparsely sampled from the video (#C means the first person view, and #O indicates another). The ultimate goal is to answer a question related to this video, choosing the correct option out of five possible answers. Please provide the answer with a single-letter (A, B, C, D, E)" + \
        #                 "It is crucial that you imagine the visual scene as vividly as possible to enhance the accuracy of your response. After selecting your answer, rate your confidence level in this choice on a scale from 1 to 100, where 1 indicates low confidence and 100 signifies high confidence. " + \
        #                 "Please provide a concise one-sentence explanation for your chosen answer. If you are uncertain about the correct option, select the one that seems closest to being correct. ",
        #     template = [
        #         Template("Description: $narration \n\n###\n\n Questions: $question \n Options: \n A: $optionA \n B: $optionB \n C: $optionC \n D: $optionD \n E: $optionE \n\n###\n\n The prediction, explanation, confidence is (please response in the format of 'prediction: \n explanation: \n confidence: \n'):"),
        #     ],
        #     post_process_fn = first_char_as_answer
        # )
        # # next-gqa GQA
        # prompt_templates['gqa'] = PromptTemplate(
        #     head = "You are a helpful expert in first person view video analysis.",
        #     template = [
        #         Template("I will provide video descriptions and one question about the video. The video is 1 FPS and the descriptions are the captions every 2 frames. Each caption starts with the frame number.\n To answer this question, what is the minimun frame interval to check?\n Follow this format: [frame_start_index, frame_end_index]. Do not provide any explanation.\n Here are the descriptions:\n$narration\n Here is the question: $question?\n Please follow the output format as follows:\n #Example1: [5, 19]\n #Example2: [30, 60]\n #Example3: [1, 10] and [50, 60]"),
        #     ],
        #     post_process_fn = get_intervals_as_list
        # )


        # # egoschema QA llama
        # B_INST, E_INST = "[INST]", "[/INST]"
        # B_SYS, E_SYS = "<<SYS>>\n", "\n<</SYS>>\n\n"
        # anchor = 'The most correct answer is ('
        # prompt_templates['qa_standard_llama'] = PromptTemplate(
        #     head = "",
        #     template = [
        #         Template(B_INST + B_SYS + "Please provide a single-letter answer (A, B, C, D, E) to the following multiple-choice question, and your answer must be one of the letters (A, B, C, D, or E). You must not provide any other response or explanation. You are given some language descriptions of a first person view video. The video is $duration seconds long. Each sentence describes a ${clip_length}s clip. The descriptions are sequential and non-overlapping which cover the whole video exactly." + E_SYS + 'Here are the descriptions:\n$narration\n Here is the question: $question.\n Here are the choices:\n (A): $optionA\n (B): $optionB\n (C): $optionC\n (D): $optionD\n (E): $optionE\n' + E_INST + anchor),
        #     ],
        #     post_process_fn = first_char_after_anchor(anchor)
        # )

        return prompt_templates

    def get(self, prompt_type):
        return self.prompt_templates[prompt_type]
