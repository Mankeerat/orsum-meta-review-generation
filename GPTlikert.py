@backoff.on_exception(backoff.expo, RateLimitError)
def generator(d):
    disc = []
    sts = ''
    messages = [
    {"role": "system", "content": "you are a metareviewer"},
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
    messages.append({"role": "user", "content": """Imagine you are a human metareviewer now. You will write metareviews for a conference. Please follow these steps:
1. Carefully read the reviews, and be aware of the information it contains.
2. Generate a metareview based on three dimensions: 'Discussion Involvement', 'Opinion Faithfulness' and 'Decision Consistency'. 
Definitions are as follows:
(1) Discussion Involvement: Discuss the paper's strengths and weaknesses, as well as agreements and disagreements among reviewers,
(2) Opinion Faithfulness: Do not contradict reviewers' comments,
(3) Decision Consistency: Accurately reflect the final decisions.
Reviews: """ + sts})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages + [{"role": "user", "content": "Generate the Metareview"}],
        temperature=0,
        max_tokens=200,
    )
    disc.append(response.choices[0].message['content'])
    return disc
