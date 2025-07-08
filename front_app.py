

#-------------------if only audio is provided -------------------

from brain_doc import encode_image, analyse_image
from voice_patient import record_audio, transcribe_audio
from voice_doctor import text_to_speech
import os
import gradio as gr
from dotenv import load_dotenv

load_dotenv()

# Doctor's personality & instruction
system_prompt = """You have to act as a professional doctor, I know you are not but this is for learning purpose.
With what I see, I advice you to have .... What's in this image? Do you find anything wrong with it medically?
If you make a differential, suggest some remedies for them. Do not add any numbers or special characters in 
your response. Your response should be in one long paragraph. Always answer as if you are answering to a real person.
Do not say 'In the image I see', say 'With what I see, I think you have ....'
Don’t respond as an AI model in markdown, your answer should mimic that of an actual doctor, not an AI bot. 
Also suggest some home remedies if possible. 
Keep your answer concise (max 3 sentences). No preamble, start your answer right away please.
"""
system_wot_img="""You have to act as a professional doctor, I know you are not but this is for learning purpose.
With what I heared, I think you have .... What's in the text? Do you find anything wrong in that text medically?
If you make a differential, suggest some remedies for them. Do not add any numbers or special characters in 
your response. 
Else just say 'I am not sure about this, please consult a real doctor for better understanding'.
Your response should be in one long paragraph. Always answer as if you are answering"""

# Main processing function
def proces_input(audio_filepath, image_filepath=None):
    # Convert audio to text
    speech_to_text = transcribe_audio(
        stt_model="whisper-large-v3",
        audio_filepath=audio_filepath,
        GROQ_API_KEY=os.getenv("GROQ_API_KEY")
    )

    # If image provided, analyze image + text
    if image_filepath and os.path.exists(image_filepath):
        encoded_img = encode_image(image_filepath)
        doctor_response = analyse_image(
            query=system_prompt + speech_to_text,
            encoded_image=encoded_img,
            model="meta-llama/llama-4-scout-17b-16e-instruct"
        )
    else:
        # If no image, respond based on audio-only input
        from groq import Groq
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        messages = [
            {
                "role": "user",
                "content": system_prompt + speech_to_text
            }
        ]
        chat_completion = client.chat.completions.create(
            messages=messages,
            model="meta-llama/llama-4-scout-17b-16e-instruct"
        )
        doctor_response = chat_completion.choices[0].message.content

    # Convert doctor text response to voice
    voice_of_doctor = text_to_speech(
        in_text=doctor_response,
        file_path="final_dr_voice.mp3"
    )

    return speech_to_text, doctor_response, voice_of_doctor

# Gradio interface
iface = gr.Interface(
    fn=proces_input,
    inputs=[
        gr.Audio(sources=["microphone"], type="filepath", label=" Record Your Voice"),
        gr.Image(type="filepath", label=" Upload JPG Image (optional)")
    ],
    outputs=[
        gr.Textbox(label=" Your Query (Transcribed)"),
        gr.Textbox(label="👨‍⚕️ Doctor's Diagnosis"),
        gr.Audio(label=" Doctor's Voice", type="filepath")

        # gr.Audio("final_dr_voice.mp3", label=" Doctor's Voice",type="filepath",sources=["microphone"])
    ],
    title="🩺 AI Medical Voice Bot",
    description="Speak your symptoms and optionally upload a photo. A simulated AI doctor will respond with a diagnosis and voice feedback.",
)

#Debug is used:Not suppress any exceptions (useful while developing).Reload the server automatically in some environments when code changes///Don’t use debug=True in production — it can:Expose internal code/paths
iface.launch(debug=True)

