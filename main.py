from STT import STT
import NLP
import actions
import TTS
from time import perf_counter as time

if __name__ == "__main__":
    
    # Creates and starts STT.
    stt = STT()
    stt.initialize_STT()
    
    while True:
        
        command = input("Press to start or insert \'exit\' to stop program.\n")
        
        if command == "exit":
            break
        
        # converts speech to text.
        start = time()
        text = stt.get_text_from_mic()
        print(f"Tempo di analisi vocale: {(time() - start):.2f} s")
        print("USER: ", text)
        
        # analyzes text.
        start = time()
        nlp_result = NLP.get_response(text)        
        actions_result = actions.handle_action(nlp_result.action, nlp_result.params)
        print(f"Tempo di analisi NLP: {(time() - start):.2f} s")
        
        if isinstance(actions_result, str):
            print("ASSISTANT: ", nlp_result.reply_text, actions_result)
        
            # synthetizes response.
            TTS.speak(nlp_result.reply_text + actions_result)