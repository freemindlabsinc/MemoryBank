import gradio as gr
from transformers import pipeline

text = ('''The tower is 324 metres (1,063 ft) tall, about the same height
        as an 81-storey building, and the tallest structure in Paris. 
        Its base is square, measuring 125 metres (410 ft) on each side. 
        During its construction, the Eiffel Tower surpassed the Washington 
        Monument to become the tallest man-made structure in the world,
        a title it held for 41 years until the Chrysler Building
        in New York City was finished in 1930. It was the first structure 
        to reach a height of 300 metres. Due to the addition of a broadcasting 
        aerial at the top of the tower in 1957, it is now taller than the 
        Chrysler Building by 5.2 metres (17 ft). Excluding transmitters, the 
        Eiffel Tower is the second tallest free-standing structure in France 
        after the Millau Viaduct.''')

get_completion = pipeline("ner", model="dslim/bert-base-NER")

def merge_tokens(tokens):
    merged_tokens = []
    for token in tokens:
        if merged_tokens and token['entity'].startswith('I-') and merged_tokens[-1]['entity'].endswith(token['entity'][2:]):
            # If current token continues the entity of the last one, merge them
            last_token = merged_tokens[-1]
            last_token['word'] += token['word'].replace('##', '')
            last_token['end'] = token['end']
            last_token['score'] = (last_token['score'] + token['score']) / 2
        else:
            # Otherwise, add the token to the list
            merged_tokens.append(token)

    return merged_tokens

def ner(input):
    output = get_completion(input)#, parameters=None, ENDPOINT_URL=API_URL)
    merged_tokens = merge_tokens(output)
    return {"text": input, "entities": merged_tokens}

text2 = ('''Carl Sagan was an American astronomer, planetary scientist, cosmologist, astrophysicist, astrobiologist, author, and science communicator. 
        His best known scientific contribution is research on extraterrestrial life, including experimental demonstration of the production of amino acids from basic chemicals by radiation. 
        Sagan assembled the first physical messages sent into space: the Pioneer plaque and the Voyager Golden Record, universal messages that could potentially be understood by any extraterrestrial intelligence that might find them. 
        Sagan argued the now-accepted hypothesis that the high surface temperatures of Venus can be attributed to and calculated using the greenhouse effect. 
        Sagan published more than 600 scientific papers and articles and was author, co-author or editor of more than 20 books. He wrote many popular science books, such as The Dragons of Eden, which won the Pulitzer Prize for General Non-Fiction in 1978.
        
        In addition, he co-wrote and narrated the award-winning 1980 television series Cosmos: A Personal Voyage, which became the most-watched series in the history of American public television.
        ''')

def create_entity_recognition_tab():
    gr.close_all()
    tab = gr.Interface(fn=ner,
                    inputs=[gr.Textbox(label="Text to find entities", lines=2)],
                    outputs=[gr.HighlightedText(label="Text with entities")],
                    title="NER with dslim/bert-base-NER",
                    description="Find entities using the `dslim/bert-base-NER` model under the hood!",
                    allow_flagging="never",
                    examples=[
                        "My name is Andrew, I'm building DeeplearningAI and I live in California", 
                        "My name is Poli, I live in Vienna and work at HuggingFace",
                        text2])

    return tab