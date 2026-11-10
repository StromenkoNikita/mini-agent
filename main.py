from dotenv import load_dotenv

import agent

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    load_dotenv()
    agent = agent.Agent("glm-5.3")
    print(agent.run("Сколько будет 37*49+12?"))

    # arr = ["err + qu", "1 + 2", "4+2", "+1-9", "1r-5"]
    # for i in arr:
    #     try:
    #         print(agent.calculator(i))
    #     except Exception as e:
    #         print(f"error: {e}")