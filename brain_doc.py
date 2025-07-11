import os
import base64
from groq import Groq
from dotenv import load_dotenv
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")


#Change image in requireed format
#testing:image_path="acne.jpg"
def encode_image(image_path):
    image_file=open(image_path, "rb")
    return base64.b64encode(image_file.read()).decode("utf-8")
   
#Step model_Create using GROQ

# query="What is wrong with face?"
# model="meta-llama/llama-4-scout-17b-16e-instruct"

def analyse_image(query,encoded_image,model):
    client =Groq()
    messages=[
    {
        "role":"user",
        "content":[
            {
                "type":"text",
                "text":query
            },
            {
                "type":"image_url",
                "image_url":{
                    "url":f"data:image/jpeg;base64,{encoded_image}",
                },
            },
        ],
    }
    ]
    #using this message sent to groq model
    chat_completion = client.chat.completions.create(
        messages=messages,
        model=model
    )
    return chat_completion.choices[0].message.content

