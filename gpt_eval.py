@backoff.on_exception(backoff.expo, RateLimitError)
def generator(d, i):
    disc = []
    sts = ''
    messages = [
    {"role": "system", "content": "you are an evaluator and you will only output one number on scale of 1 to 5 and nothing else. you cannot generate any non-numeric thing"},
    ]
    for y in range(len(d["Review"])):
        try:
            st = d["Review"][y]["review"]
            word_list = st.split(" ")
            if len(word_list) > 300:
                word_list = word_list[:300]
                st = ' '.join(word_list)
        except:
            continue
    
        sts += st
    candidate = instruct[i][0]
    messages.append({"role": "user", "content": """You will be given one metareview written for reviews by committee on a paper. Your task is to rate the metareview on one metric.
Please make sure you read and understand these instructions carefully. Please keep this
document open while reviewing, and refer to it as needed.
Evaluation Criteria:
Quality of Metareview (1-5) - the collective quality of all sentences. We align this dimension with
the DUC quality question of structure and coherence whereby ”the metareview should be
well-structured and well-organized. The metareview should always discuss disadvantages and advantages or a paper and have a clear scope of accept/reject decision. The metareview should have concrete evidence from the papers reviews and concerete comments as well.”
Evaluation Steps:
1. Read the reviews carefully and identify the main topic and key points.
2. Read the metareview and compare it to the reviews. Check if the metareview covers the main
topic, discusses advantages and disadvantages, if the most important advantages and disadvantages discussed in the above meta-review, if the most important advantages and disadvantages discussed in the above meta-review, if the most important consensus and controversy discussed in the above meta-review, if the above meta-review contradicting reviewers' comments, if the above meta-review supporting the acceptance/rejection decision, and if it presents them in a clear and logical order.
3. Assign a score for quality of metareview on a scale of 1 to 5, where 1 is the lowest and 5 is the highest
based on the Evaluation Criteria. Source Text: """ + sts + "Metareview: " + candidate + "Evaluation Form (scores ONLY): - "})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages + [{"role": "user", "content": "Now give me the rating from 1 - 5 as a number only"}],
        temperature=0,
        max_tokens=1,
    )
    disc.append(response.choices[0].message['content'])
    disc.append(response.choices[0].message['content'])
    print(response.choices[0].message['content'])
    return disc
