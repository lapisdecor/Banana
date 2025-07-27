from inputimeout import inputimeout, TimeoutOccurred
import numpy as np
from collections import defaultdict
import random

class SimpleLLM:
    def __init__(self):
        self.vocab = {}
        self.reverse_vocab = {}
        self.ngram_counts = defaultdict(int)
        self.n = 3  # Usaremos trigramas para este exemplo

    def train(self, text):
        # Tokenização simples
        tokens = text.lower().split()

        # Construir vocabulário
        for i, token in enumerate(tokens):
            if token not in self.vocab:
                self.vocab[token] = len(self.vocab)
                self.reverse_vocab[len(self.vocab) - 1] = token

        # Contar n-gramas
        for i in range(len(tokens) - self.n + 1):
            ngram = tuple(tokens[i:i + self.n])
            self.ngram_counts[ngram] += 1

    def predict_next_word(self, context):
        context = context.lower().split()
        if len(context) < self.n - 1:
            # Se o contexto for muito curto, adicionamos tokens de padding
            context = ['<start>'] * (self.n - 1 - len(context)) + context

        last_words = tuple(context[-(self.n - 1):])

        # Encontrar todos os n-gramas que começam com last_words
        possible = []
        for ngram, count in self.ngram_counts.items():
            if ngram[:self.n - 1] == last_words:
                possible.append((ngram[-1], count))

        if not possible:
            return None

        # Normalizar contagens para probabilidades
        words, counts = zip(*possible)
        probs = np.array(counts) / sum(counts)

        # Amostrar uma palavra baseada nas probabilidades
        return np.random.choice(words, p=probs)

    def generate_text(self, seed, length=10):
        result = seed.split()
        for _ in range(length):
            next_word = self.predict_next_word(' '.join(result[-(self.n - 1):]))
            if not next_word:
                break
            result.append(next_word)
        return ' '.join(result)


def end_program():
    exit()

def think():
    # use document saved to train the model
    print("Thinking... to stop press Ctrl-C and to end write stop. ")

    while True:
        try:

            # retrain LLM
            # this would actually train the local LLM while no a key is pressed
            with open("doc.txt") as f:
                text = f.read()

            llm.train(text)
            print(llm.generate_text(random.choice(text.split()), 5), end=' ')


        except KeyboardInterrupt:
            print('cancelled by user')  # overload
            break
    run()


def run_llm_prompt(user_input):
    answer = " esta seria a resposta da LLM para a questão " + user_input
    return answer

def make_answer(user_input):
    answer = run_llm_prompt(user_input)
    return answer

def run():
    # ask prompt
    while True:
        try:
            user_input = inputimeout(prompt='Tens 20 segundos para escrever uma coisa ou escrever stop para parar: ', timeout=20)
        except TimeoutOccurred:
            user_input = 'Time is up!'
            print(user_input)

        # answer
        print("Let me think...")
        if user_input == 'Time is up!':
            break
        if user_input == 'stop':
            print("Saindo...")
            break
        answer = make_answer(user_input)
        print(answer)
        # save input and answer to document
        with open("doc.txt", "w") as f:
            f.write(user_input)
            f.write(answer)
    if user_input == 'stop':
        end_program()
    think()


if __name__ == "__main__":
    llm = SimpleLLM()
    print("Quando a LLM começar a sonhar podes para-la com CTRL-C e depois escrever stop, senão volta a sonhar.")
    run()