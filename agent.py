import json

from openai import OpenAI

ALLOWED = set("0123456789+-*/(). ")

CALC_SCHEMA = {"type": "function",
               "function": {"name": "calculator", "description": "Вычисляет арифметическое выражение",
                            "parameters": {"type": "object", "properties": {"expression": {"type": "string"}},
                                           "required": ["expression"]}}}


def calculator(expression: str) -> str:
    if not expression or not all(ch in ALLOWED for ch in expression):
        return "error: invalid expression"
    try:
        return str(eval(expression))
    except Exception as e:
        return f"error: {e}"


TOOLS = {"calculator": calculator}


class Agent:
    def __init__(self, model: str):
        self.client = OpenAI()
        self.model = model

    def run(self, messages: list[dict]) -> list[dict]:

        for step in range(5):
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=[CALC_SCHEMA]
            )
            msg = response.choices[0].message
            messages.append(msg)

            if not msg.tool_calls:
                print("Result:", msg.content)
                break
            for call in msg.tool_calls:
                args = json.loads(call.function.arguments)
                result = TOOLS[call.function.name](**args)
                print(f"[step {step}] {call.function.name}({args}) -> {result}")
                messages.append({"role": "tool", "tool_call_id": call.id, "content": result})

        return messages