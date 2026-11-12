import json

from openai import OpenAI, APIStatusError

ALLOWED = set("0123456789+-*/(). ")

# CALC_SCHEMA = {"type": "function",
#                "function": {"name": "calculator", "description": "Вычисляет арифметическое выражение",
#                             "parameters": {"type": "object", "properties": {"expression": {"type": "string"}},
#                                            "required": ["expression"]}}}

PRODUCTS = {"milk": 1.3, "meat": 5, "corn": 0.6, "onion": 0.9}


def calculator(expression: str) -> str:
    if not expression or not all(ch in ALLOWED for ch in expression):
        return "error: invalid expression"
    try:
        return str(eval(expression))
    except Exception as e:
        return f"error: {e}"


def get_price(product: str) -> str:
    price = PRODUCTS.get(product, 0)

    if price == 0:
        return "not found price for {}".format(product)

    return str(price)


TOOLS = {"calculator": calculator, "get_price": get_price}
SCHEMA = []

def fill_tools():
    global SCHEMA
    try:
        with open("TOOLS.json", "r", encoding="utf-8") as file:
            SCHEMA = json.load(file)
    except FileNotFoundError:
        print("Error: The file was not found.")
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format - {e}")


class Agent:
    def __init__(self, model: str):
        self.client = OpenAI()
        self.model = model
        fill_tools()

    def run(self, messages: list[dict]) -> list[dict]:

        for step in range(5):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    tools=SCHEMA
                )
            except APIStatusError as e:
                print("Status:", e.status_code)
                print("Response:", e.response.text)
                raise
            msg = response.choices[0].message
            messages.append(msg.model_dump(exclude_none=True))

            if not msg.tool_calls:
                print("Result:", msg.content)
                break
            for call in msg.tool_calls:
                args = json.loads(call.function.arguments)
                result = TOOLS[call.function.name](**args)
                print(f"[step {step}] {call.function.name}({args}) -> {result}")
                messages.append({"role": "tool", "tool_call_id": call.id, "content": result})

        return messages
