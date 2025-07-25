from inputimeout import inputimeout, TimeoutOccurred
import keyboard

def end_program():
    exit()

def think():
    # use document saved to train the model
    print("Thinking... to stop press A")
    while True:
        if not keyboard.is_pressed('a'):
            # retrain LLM
            # this would actually train the local LLM while no a key is pressed
            # TODO
            pass
        else:
            break
    run()


def run_llm_prompt(user_input):
    answer = "this would be the LLM api answer for" + user_input
    return answer

def make_answer(user_input):
    answer = run_llm_prompt(user_input)
    return answer

def run():
    # ask prompt
    while True:
        try:
            user_input = inputimeout(prompt='You have 5 seconds to enter something: ', timeout=5)
        except TimeoutOccurred:
            user_input = 'Time is up!'
            print(user_input)

        # answer
        print("Let me think...")
        if user_input == 'Time is up!':
            break
        if user_input == 'stop':
            break
        answer = make_answer(user_input)
        print(answer)
        # save input and answer to document
        #TODO
    if user_input == 'stop':
        end_program()
    think()


if __name__ == "__main__":
    run()