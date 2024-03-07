import gradio as gr
from transformers import pipeline

get_completion = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

#def get_completion(input):
##    try:
 #       output = get_completion(input)
 #       return output[0]['summary_text']
 #   except Exception as e:
 #       return str(e)

text1 = ('''The tower is 324 metres (1,063 ft) tall, about the same height
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

text2 = ('''Carl Sagan was an American astronomer, planetary scientist, cosmologist, astrophysicist, astrobiologist, author, and science communicator. 
        His best known scientific contribution is research on extraterrestrial life, including experimental demonstration of the production of amino acids from basic chemicals by radiation. 
        Sagan assembled the first physical messages sent into space: the Pioneer plaque and the Voyager Golden Record, universal messages that could potentially be understood by any extraterrestrial intelligence that might find them. 
        Sagan argued the now-accepted hypothesis that the high surface temperatures of Venus can be attributed to and calculated using the greenhouse effect. 
        Sagan published more than 600 scientific papers and articles and was author, co-author or editor of more than 20 books. He wrote many popular science books, such as The Dragons of Eden, which won the Pulitzer Prize for General Non-Fiction in 1978.
        
        In addition, he co-wrote and narrated the award-winning 1980 television series Cosmos: A Personal Voyage, which became the most-watched series in the history of American public television.
        ''')

def summarize(input: str) -> str:
    output = get_completion(input)
    return output[0]['summary_text']

def create_summarization_tab():
    gr.close_all()
    tab = gr.Interface(fn=summarize, 
                    inputs=[gr.Textbox(label="Text to summarize", lines=6)],
                    outputs=[gr.Textbox(label="Result")],
                    title="Text summarization with distilbart-cnn",
                    description="Summarize any text using the `sshleifer/distilbart-cnn-12-6` model under the hood!",
                    examples=[text1, text2]
                   )
    return tab