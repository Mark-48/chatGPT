import gradio as gr
from revChatGPT.V1 import Chatbot
import glob, os

access_token = None


def parse_text(text):
    lines = text.split("\n")
    for i, line in enumerate(lines):
        if "```" in line:
            items = line.split("`")
            if items[-1]:
                lines[i] = f'<pre><code class="{items[-1]}">'
            else:
                lines[i] = f"</code></pre>"
        else:
            if i > 0:
                lines[i] = "<br/>" + line.replace(" ", "&nbsp;")
    return "".join(lines)


def configure_chatgpt(info):
    access_token = info
    config = {}
    config.update({"access_token": access_token})

    global chatgpt
    chatgpt = Chatbot(config=config)


def ask(prompt):
    message = ""
    for data in chatgpt.ask(prompt):
        message = data["message"]
    return parse_text(message)


def query_chatgpt(inputs, history, message):
    history = history or []
    output = ask(inputs)
    history.append((inputs, output))
    return history, history, ""


def initialize_prompt(prompt_type, history):
    history = history or []

    if prompt_type:
        prompt_file = "./prompts/" + str(prompt_type) + ".txt"

        with open(prompt_file, "r") as f:
            prompt = f.read()
        output = ask(prompt)
        history.append(("<ORIGINAL PROMPT>", output))

    return history, history


def display_prompt(show, prompt_type):
    if not prompt_type:
        show = False
        return "Error - prompt not selected"

    else:
        if show:
            prompt_file = "./prompts/" + str(prompt_type) + ".txt"

            with open(prompt_file, "r") as f:
                prompt = f.read()

            return prompt
        else:
            return ""


with gr.Blocks() as demo:
    gr.Markdown("""<h3><center>ChatGPT + Robotics</center></h3>""")
    gr.Markdown(
        """This is a companion app to the work [ChatGPT for Robotics: Design Principles and Model Abilities](https://aka.ms/ChatGPT-Robotics).<br>
        This space allows you to work with ChatGPT to get it to generate code for robotics tasks, such as get a robot arm to manipulate objects, or have a drone fly around in a 3D world.<br>  
        See [README](https://huggingface.co/spaces/microsoft/ChatGPT-Robotics/blob/main/README.md) for detailed instructions."""
    )

    if not access_token:
        gr.Markdown("""<h4>Login to ChatGPT</h4>""")
        with gr.Row():
            with gr.Group():
                info = gr.Textbox(placeholder="Enter access token here (from https://chat.openai.com/api/auth/session)", label="ChatGPT Login")
                with gr.Row():
                    login = gr.Button("Login")
                    login.click(configure_chatgpt, inputs=[info])

    l = os.listdir("./prompts")
    li = [x.split(".")[0] for x in l]

    gr.Markdown("""<h4>Initial Prompt for ChatGPT</h4>""")
    prompt_type = gr.components.Dropdown(
        li,
        label="Select sample prompt",
        value=None,
        info="Choose a prompt based on the robot/scenario you're interested in (e.g. pick airsim or real_drone to start a drone scenario)",
    )

    show_prompt = gr.Checkbox(label="Display prompt")
    prompt_display = gr.Textbox(interactive=False, label="Prompt")
    show_prompt.change(fn=display_prompt, inputs=[show_prompt, prompt_type], outputs=prompt_display)

    initialize = gr.Button(value="Initialize")

    gr.Markdown("""<h4>Conversation</h4>""")
    chatgpt_robot = gr.Chatbot()
    message = gr.Textbox(
        placeholder="Enter query",
        label="",
        info='Talk to ChatGPT and ask it to help with specific tasks! For example, "take off and reach an altitude of five meters"',
    )

    state = gr.State()

    initialize.click(fn=initialize_prompt, inputs=[prompt_type, state], outputs=[chatgpt_robot, state])

    message.submit(query_chatgpt, inputs=[message, state], outputs=[chatgpt_robot, state, message])

    demo.launch()