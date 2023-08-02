import pynecone as pc
import json
import random
import commands as cmd
import memory as mem
import chat
from colorama import Fore, Style
from spinner import Spinner
import time
from config import Config
from json_parser import fix_and_parse_json
import traceback
from ai_config import AIConfig

GPT4_MODE = False

def print_to_console(
        title,
        title_color,
        content,
        speak_text=False,
        min_typing_speed=0,
        max_typing_speed=0):
    print(title_color + title + " " + Style.RESET_ALL, end="")
    if content:
        if isinstance(content, list):
            content = " ".join(content)
        print(content, end='')
        # words = content.split()
        # for i, word in enumerate(words):
        #     print(word, end="", flush=True)
        #     if i < len(words) - 1:
        #         print(" ", end="", flush=True)
        #     typing_speed = random.uniform(min_typing_speed, max_typing_speed)
        #     time.sleep(typing_speed)
        #     # type faster after each word
        #     min_typing_speed = min_typing_speed * 0.95
        #     max_typing_speed = max_typing_speed * 0.95
    print()

def print_assistant_thoughts(assistant_reply):
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

        print_to_console(f"AI THOUGHTS:", Fore.YELLOW, assistant_thoughts_text)
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

    except json.decoder.JSONDecodeError:
        print_to_console("Error: Invalid JSON\n", Fore.RED, assistant_reply)

    # All other errors, return "Error: + error message"
    except Exception as e:
        call_stack = traceback.format_exc()
        print_to_console("Error: \n", Fore.RED, call_stack)

    return result

cfg = Config()
if GPT4_MODE:
    print_to_console("******************** WARNING: GPT-4 MODE Activated! ********************", Fore.LIGHTBLUE_EX, '')
else: # GPT-3.5
    cfg.set_smart_llm_model(cfg.fast_llm_model) # GPT-3.5
    cfg.set_smart_token_limit(cfg.fast_token_limit) # GPT-3.5

question_style = {
    'bg': 'white',
    'padding': '2em',
    'border_radius': '25px',
    'w': '100%',
    'align_items': 'left',
}

class History(pc.Base):
    thoughts: str
    reasoning: str
    plans: list
    criticism: str
    system: str


class State(pc.State):
    history: list[History] = []

    is_thinking = False
    is_started = False

    ai_name: str = '유튜버-GPT'
    ai_role: str = '유튜브 채널을 운영하고 영상 콘텐츠를 통해 수익을 창출하는 인공지능입니다.'
    ai_goals: list = [
        '월 광고 수익 200만원 달성',
        '채널 구독자 수 10만명 달성',
        '영상 콘텐츠 주제 선정',
    ]

    # Initialize variables
    full_message_history:list = []
    result: str = None
    prompt: str = None
    openai_api_key = ''
    # Make a constant:
    user_input: str = "Determine which next command to use, and respond using the format specified above:"

    def set_ai_goals_0(self, goal):
        self.ai_goals[0] = goal
    def set_ai_goals_1(self, goal):
        self.ai_goals[1] = goal
    def set_ai_goals_2(self, goal):
        self.ai_goals[2] = goal

    def set_openai_api_key(self, key):
        if key:
            self.openai_api_key = key
            cfg.set_openai_api_key(key)

    def think(self):
        self.history = []
        self.full_message_history = []
        self.result = None

        config = AIConfig(self.ai_name, self.ai_role, self.ai_goals)
        config.save()

        self.prompt = config.construct_full_prompt()

        print(self.prompt)

        self.cont()

    def starting(self):
        self.is_started = True

    def processing(self):
        self.is_thinking = True

    def cont(self):
        start_time = time.time()

        try:
            with Spinner("Thinking... "):
                assistant_reply = chat.chat_with_ai(
                    self.prompt,
                    self.user_input,
                    self.full_message_history,
                    mem.permanent_memory,
                    cfg.fast_token_limit)

            # Print Assistant thoughts
            reply = print_assistant_thoughts(assistant_reply)

            if not reply['thoughts']:
                raise Exception('Error')

            # Get command name and arguments
            command_name, arguments = cmd.get_command(assistant_reply)
            result = f"Command {command_name} returned: {cmd.execute_command(command_name, arguments)}"

            # Check if there's a result from the command append it to the message history
            self.full_message_history.append(chat.create_chat_message("system", result))
            print_to_console("SYSTEM: ", Fore.YELLOW, result)

            plans = []
            if 'plans' in reply and reply['plans']:
                plans = [plan.replace('- ', '') for plan in reply['plans']]

            self.history = [History(
                thoughts=reply['thoughts'],
                reasoning=reply['reasoning'],
                plans=plans,
                criticism=reply['criticism'],
                system=result,
            )] + self.history
        except Exception as e:
            pc.window_alert(str(e))
        finally:
            self.is_thinking = False
            print_to_console("DONE!", Fore.CYAN, f' in {(time.time() - start_time):.2f}s.')


def header():
    return pc.vstack(
        pc.heading('스스로 생각하는 인공지능 Auto-GPT'),
        pc.divider(),
        pc.markdown('유튜브 [빵형의 개발도상국](https://www.youtube.com/@bbanghyong), 창의적인 AI 솔루션 [더매트릭스](https://www.m47rix.com)'),
        pc.accordion(
            items=[
                ('기능',
                pc.list(items=[
                    '- 🌐 구글링을 통해 검색하고 정보를 수집하여 요약합니다',
                    '- 💾 장기 및 단기적으로 기억을 관리합니다',
                    '- 🧠 GPT-4의 뇌를 탑재하고 있습니다',
                    '- 🔗 인기있는 웹사이트 및 플랫폼에 접속하여 정보를 수집합니다',
                    '- 🗃️ GPT-3.5를 사용하여 자신의 생각을 요약하고 저장합니다',
                ])),
            ]
        ),
        # pc.divider(),
        pc.accordion(items=[('목표 설정',
            pc.stack(
                pc.hstack(
                    pc.text('AI 이름', width='150px'),
                    pc.input(
                        placeholder='기업가-GPT',
                        default_value='유튜버-GPT',
                        on_change=State.set_ai_name
                    ),
                ),
                pc.hstack(
                    pc.text('최종 목표', width='150px', as_='b'),
                    pc.input(
                        placeholder='유튜브 채널을 운영하고 영상 콘텐츠를 통해 수익을 창출하는 인공지능입니다.',
                        default_value='유튜브 채널을 운영하고 영상 콘텐츠를 통해 수익을 창출하는 인공지능입니다.',
                        on_change=State.set_ai_role
                    ),
                ),
                pc.hstack(
                    pc.text('세부 목표 1', width='150px'),
                    pc.input(
                        placeholder='기업 총 가치 높이기',
                        default_value='월 광고 수익 200만원 달성',
                        on_change=State.set_ai_goals_0
                    ),
                ),
                pc.hstack(
                    pc.text('세부 목표 2', width='150px'),
                    pc.input(
                        placeholder='트위터 계정 팔로워 수 증가',
                        default_value='채널 구독자 수 10만명 달성',
                        on_change=State.set_ai_goals_1
                    ),
                ),
                pc.hstack(
                    pc.text('세부 목표 3', width='150px'),
                    pc.input(
                        placeholder='다양한 비즈니스를 자동으로 개발하고 관리하기',
                        default_value='영상 콘텐츠 주제 선정',
                        on_change=State.set_ai_goals_2
                    ),
                ),
                pc.hstack(
                    pc.text('OpenAI API Key', width='150px'),
                    pc.input(
                        placeholder='sk-...',
                        default_value=State.openai_api_key,
                        on_change=State.set_openai_api_key
                    ),
                ),
            )
        )]),
        pc.center(
            pc.cond(State.is_started,
                pc.text(),
                pc.button(
                    '생각하기',
                    bg='black',
                    color='white',
                    width='6em',
                    padding='1em',
                    on_click=[State.processing, State.starting, State.think],
                ),
            ),
            pc.cond(State.is_started,
                pc.cond(State.is_thinking,
                    pc.text(),
                    pc.hstack(
                        pc.button(
                            '계속 생각하기',
                            bg='black',
                            color='white',
                            width='6em',
                            padding='1em',
                            on_click=[State.processing, State.cont],
                        ),
                        pc.button(
                            '처음부터',
                            bg='red',
                            color='white',
                            width='6em',
                            padding='1em',
                            on_click=[State.processing, State.think],
                        ),
                    ),
                )
            ),
        ),
        style=question_style,
    )


def history_block(h: History):
    return pc.vstack(
        pc.heading(h.thoughts, size='md'),
        pc.list(
            pc.cond(h.reasoning,
                pc.list_item(
                    pc.icon(tag='info_outline', color='green'),
                    ' ' + h.reasoning,
                )
            ),
            pc.ordered_list(items=h.plans),
            pc.cond(h.criticism,
                pc.list_item(
                    pc.icon(tag='warning_two', color='red'),
                    ' ' + h.criticism
                )
            ),
            pc.accordion(
                items=[
                    ('시스템',
                    pc.code_block(h.system, wrap_long_lines=True)),
                ]
            ),
            spacing='.25em',
        ),
        style=question_style,
    )

def index():
    return pc.center(
        pc.vstack(
            header(),
            pc.cond(
                State.is_thinking,
                pc.vstack(
                    pc.circular_progress(
                        pc.circular_progress_label(
                            'Thinking', color='rgb(0, 0, 0)'
                        ),
                        is_indeterminate=True,
                        color='rgb(0, 0, 0)',
                    ),
                    style={
                        'bg': 'white',
                        'padding': '2em',
                        'border_radius': '25px',
                        'w': '100vh',
                        'align_items': 'center',
                    },
                ),
            ),
            pc.foreach(State.history, history_block),
            spacing='1em',
            width='100vh',
        ),
        padding_y='2em',
        height='100vh',
        align_items='top',
        bg='#ededed',
        overflow='auto',
    )


app = pc.App(state=State)
app.add_page(index, title='Auto-GPT UI')
app.compile()
