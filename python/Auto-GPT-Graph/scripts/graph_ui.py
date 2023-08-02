from flask import Flask, render_template
import json
import random
import commands as cmd
import memory as mem
import data
import chat
from colorama import Fore, Style
from spinner import Spinner
import time
import speak
from config import Config
from json_parser import fix_and_parse_json
from ai_config import AIConfig
import traceback
import yaml


def print_to_console(
        title,
        title_color,
        content,
        speak_text=False,
        min_typing_speed=0,
        max_typing_speed=0):
    global cfg
    if speak_text and cfg.speak_mode:
        speak.say_text(f"{title}. {content}")
    print(title_color + title + " " + Style.RESET_ALL, end="")
    if content:
        if isinstance(content, list):
            content = " ".join(content)
        words = content.split()
        for i, word in enumerate(words):
            print(word, end="", flush=True)
            if i < len(words) - 1:
                print(" ", end="", flush=True)
            typing_speed = random.uniform(min_typing_speed, max_typing_speed)
            time.sleep(typing_speed)
            # type faster after each word
            min_typing_speed = min_typing_speed * 0.95
            max_typing_speed = max_typing_speed * 0.95
    print()

def print_assistant_thoughts(assistant_reply):
    global ai_name
    global cfg
    result = {}

    try:
        # Parse and print Assistant response
        assistant_reply_json = fix_and_parse_json(assistant_reply)

        # Check if assistant_reply_json is a string and attempt to parse it into a JSON object
        if isinstance(assistant_reply_json, str):
            try:
                assistant_reply_json = json.loads(assistant_reply_json)
            except json.JSONDecodeError as e:
                print_to_console("Error: Invalid JSON\n", Fore.RED, assistant_reply)
                assistant_reply_json = {}

        assistant_thoughts_reasoning = None
        assistant_thoughts_plan = None
        assistant_thoughts_speak = None
        assistant_thoughts_criticism = None
        assistant_thoughts = assistant_reply_json.get("thoughts", {})
        assistant_thoughts_text = assistant_thoughts.get("text")

        if assistant_thoughts:
            assistant_thoughts_reasoning = assistant_thoughts.get("reasoning")
            assistant_thoughts_plan = assistant_thoughts.get("plan")
            assistant_thoughts_criticism = assistant_thoughts.get("criticism")
            assistant_thoughts_speak = assistant_thoughts.get("speak")

        print_to_console(f"{ai_name.upper()} THOUGHTS:", Fore.YELLOW, assistant_thoughts_text)
        print_to_console("REASONING:", Fore.YELLOW, assistant_thoughts_reasoning)

        result['thoughts'] = assistant_thoughts_text
        result['reasoning'] = assistant_thoughts_reasoning

        if assistant_thoughts_plan:
            print_to_console("PLAN:", Fore.YELLOW, "")
            # If it's a list, join it into a string
            if isinstance(assistant_thoughts_plan, list):
                assistant_thoughts_plan = "\n".join(assistant_thoughts_plan)
            elif isinstance(assistant_thoughts_plan, dict):
                assistant_thoughts_plan = str(assistant_thoughts_plan)

            # Split the input_string using the newline character and dashes
            lines = assistant_thoughts_plan.split('\n')
            for line in lines:
                line = line.lstrip("- ")
                print_to_console("- ", Fore.GREEN, line.strip())

            result['plans'] = lines

        result['criticism'] = assistant_thoughts_criticism

        print_to_console("CRITICISM:", Fore.YELLOW, assistant_thoughts_criticism)
        # Speak the assistant's thoughts
        if cfg.speak_mode and assistant_thoughts_speak:
            speak.say_text(assistant_thoughts_speak)

    except json.decoder.JSONDecodeError:
        print_to_console("Error: Invalid JSON\n", Fore.RED, assistant_reply)

    # All other errors, return "Error: + error message"
    except Exception as e:
        call_stack = traceback.format_exc()
        print_to_console("Error: \n", Fore.RED, call_stack)

    return result

def load_variables(config_file="config.yaml"):
    # Load variables from yaml file if it exists
    try:
        with open(config_file) as file:
            config = yaml.load(file, Loader=yaml.FullLoader)
        ai_name = config.get("ai_name")
        ai_role = config.get("ai_role")
        ai_goals = config.get("ai_goals")
    except FileNotFoundError:
        ai_name = ""
        ai_role = ""
        ai_goals = []

    # Prompt the user for input if config file is missing or empty values
    if not ai_name:
        ai_name = input("Name your AI: ")
        if ai_name == "":
            ai_name = "Entrepreneur-GPT"

    if not ai_role:        
        ai_role = input(f"{ai_name} is: ")
        if ai_role == "":
            ai_role = "an AI designed to autonomously develop and run businesses with the sole goal of increasing your net worth."

    if not ai_goals:
        print("Enter up to 5 goals for your AI: ")
        print("For example: \nIncrease net worth, Grow Twitter Account, Develop and manage multiple businesses autonomously'")
        print("Enter nothing to load defaults, enter nothing when finished.")
        ai_goals = []
        for i in range(5):
            ai_goal = input(f"Goal {i+1}: ")
            if ai_goal == "":
                break
            ai_goals.append(ai_goal)
        if len(ai_goals) == 0:
            ai_goals = ["Increase net worth", "Grow Twitter Account", "Develop and manage multiple businesses autonomously"]
         
    # Save variables to yaml file
    config = {"ai_name": ai_name, "ai_role": ai_role, "ai_goals": ai_goals}
    with open(config_file, "w") as file:
        documents = yaml.dump(config, file)

    prompt = data.load_prompt()
    prompt_start = """Your decisions must always be made independently without seeking user assistance. Play to your strengths as an LLM and pursue simple strategies with no legal complications."""

    # Construct full prompt
    full_prompt = f"You are {ai_name}, {ai_role}\n{prompt_start}\n\nGOALS:\n\n"
    for i, goal in enumerate(ai_goals):
        full_prompt += f"{i+1}. {goal}\n"

    full_prompt += f"\n\n{prompt}"
    return full_prompt


app = Flask(__name__)

cfg = Config()
# cfg.set_smart_llm_model(cfg.fast_llm_model) # GPT-3.5

# Initialize variables
full_message_history = []
result = None
prompt = None
# Make a constant:
user_input = "Determine which next command to use, and respond using the format specified above:"

@app.route("/")
def index():
    global full_message_history, result, prompt
    global ai_name

    ai_name = "사업가-GPT"
    # ai_role = "AI와 메타버스를 활용한 플랫폼 사업을 기획하고 수행하기 위한 인공지능입니다."
    # ai_goals = [
    #     "연 매출 100억 달성",
    #     "월 평균 사용자 100만명 달성"
    # ]

    ai_role = "나의 자산을 증가시키기위한 사업을 자동으로 개발하고 운영하기 위해 고안된 인공지능입니다."
    ai_goals = ["기업 총 가치를 높이기", "트위터 계정 팔로워 수 증가", "다양한 비즈니스를 자동으로 개발하고 관리하기"]

    config = AIConfig(ai_name, ai_role, ai_goals)
    config.save()

    prompt = config.construct_full_prompt()

    print('******************************')
    print(prompt)
    print('******************************')

    full_message_history = []
    result = None

    return render_template("index.html")

@app.route("/think", methods=["POST"])
def think():
    with Spinner("Thinking... "):
        assistant_reply = chat.chat_with_ai(
            prompt,
            user_input,
            full_message_history,
            mem.permanent_memory,
            cfg.fast_token_limit)

    # Print Assistant thoughts
    reply = print_assistant_thoughts(assistant_reply)

    # Get command name and arguments
    command_name, arguments = cmd.get_command(assistant_reply)
    result = f"Command {command_name} returned: {cmd.execute_command(command_name, arguments)}"

    # Check if there's a result from the command append it to the message history
    full_message_history.append(chat.create_chat_message("system", result))
    print_to_console("SYSTEM: ", Fore.YELLOW, result)

    return reply

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860, debug=False)
