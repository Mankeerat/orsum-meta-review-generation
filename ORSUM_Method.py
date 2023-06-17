import backoff
import json
import openai
from openai.error import RateLimitError
openai.api_key = 'YOUR_API_KEY'


with open('ORSUM_test.jsonl') as f:
    data = [json.loads(line) for line in f]
len(data)


@backoff.on_exception(backoff.expo, RateLimitError)
def generator(d):
    disc = []
    disc1 = []
    disc2 = []
    disc3 = []
    disc4 = []

    messages = [
    {"role": "system", "content": "You are opinionbot and metareviewer for major conference."},
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

        messages.append({"role": "user", "content": "From the sentiments and aspects discussed in the reviews, what are the key strengths and weaknesses of this paper? Please cite corresponding reviewers and evidence" + st})
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7,
            max_tokens=100,
        )

        messages.append({"role": "assistant", "content": response.choices[0].message['content']})

    response_adv = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages + [{"role": "user", "content": "Identify the points of agreement and disagreement among the reviewers. Please include the corresponding reviewers and evidence."}],
        temperature=0.7,
        max_tokens=100,
    )

    messages.append({"role": "assistant", "content": response_adv.choices[0].message['content']})

    response_contro = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages + [{"role": "user", "content": "Considering the key sentiments from the reviews, the identified strengths and weaknesses, and the consensus and controversy among the reviewers, write a metareview with decision of acceptance/rejection."}],
        temperature=0.7,
        max_tokens=150,
    )

    messages.append({"role": "assistant", "content": response_contro.choices[0].message['content']})

    discussion = response_contro.choices[0].message['content']
    disc.append(discussion)

    response_mrt = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages + [{"role": "user", "content": "Are the most important advantages and disadvantages discussed in the above meta-review? Are the most important consensus and controversy discussed in the above meta-review? Is the above meta-review contradicting reviewers' comments? Is the above meta-review supporting the rejection decision? If not, how can it be improved?"}],
        temperature=0.7,
        max_tokens=150,
    )

    response_mrt = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages + [{"role": "user", "content": "using this discussion, write an accurate <200 words metareview with decision of acceptance/rejection."}],
        temperature=0.7,
        max_tokens=200,
    )

    discussion = response_mrt.choices[0].message['content']
    disc1.append(discussion)

    response_mrt = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages + [{"role": "user", "content": "Are the most important advantages and disadvantages discussed in the above meta-review? Are the most important consensus and controversy discussed in the above meta-review? Is the above meta-review contradicting reviewers' comments? Is the above meta-review supporting the rejection decision? If not, how can it be improved?"}],
        temperature=0.7,
        max_tokens=150,
    )

    response_mrt = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages + [{"role": "user", "content": "using this discussion, write an accurate <200 words metareview with decision of acceptance/rejection."}],
        temperature=0.7,
        max_tokens=200,
    )

    discussion = response_mrt.choices[0].message['content']
    disc2.append(discussion)

    response_mrt = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages + [{"role": "user", "content": "Are the most important advantages and disadvantages discussed in the above meta-review? Are the most important consensus and controversy discussed in the above meta-review? Is the above meta-review contradicting reviewers' comments? Is the above meta-review supporting the rejection decision? If not, how can it be improved?"}],
        temperature=0.7,
        max_tokens=150,
    )

    response_mrt = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages + [{"role": "user", "content": "using this discussion, write an accurate <200 words metareview with decision of acceptance/rejection."}],
        temperature=0.7,
        max_tokens=200,
    )

    discussion = response_mrt.choices[0].message['content']
    disc3.append(discussion)

    response_mrt = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages + [{"role": "user", "content": "Are the most important advantages and disadvantages discussed in the above meta-review? Are the most important consensus and controversy discussed in the above meta-review? Is the above meta-review contradicting reviewers' comments? Is the above meta-review supporting the rejection decision? If not, how can it be improved?"}],
        temperature=0.7,
        max_tokens=150,
    )
    response_mrt = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages + [{"role": "user", "content": "using this discussion, write an accurate <200 words metareview with decision of acceptance/rejection."}],
        temperature=0.7,
        max_tokens=200,
    )

    discussion = response_mrt.choices[0].message['content']
    disc4.append(discussion)

    return disc, disc1, disc2, disc3, disc4


major = []
major1 = []
major2 = []
major3 = []
major4 = []

for i in range(len(data)):
    print(i)
    result = generator(data[i])
    major.append(result[0])
    major1.append(result[1])
    major2.append(result[2])
    major3.append(result[3])
    major4.append(result[4])