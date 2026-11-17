from dotenv import load_dotenv
from collections import deque

import agent

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    load_dotenv()
    agent = agent.Agent("glm-5.3")

    context = []
    window = []
    while True:
        expression = input()
        if expression == "/exit":
            break

        if len(window) > 0:
            while window[-1].total_prompt_tokens > 500 and len(window) > 1:
                remove = window.pop(0)
                window[-1].total_prompt_tokens -= remove.batch_tokens_size
                context = context[remove.batch_size:]
        window.append(agent.run(message={"role": "user", "content": expression},
                                messages=context,
                                prompt_tokens=window[-1].total_prompt_tokens if len(window) > 0 else 0))

    print(context)
    print(window)
    # arr = ["err + qu", "1 + 2", "4+2", "+1-9", "1r-5"]
    # for i in arr:
    #     try:
    #         print(agent.calculator(i))
    #     except Exception as e:
    #         print(f"error: {e}")