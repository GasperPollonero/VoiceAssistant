from STT import STT
import NLP
import actions
import TTS
import time

if __name__ == "__main__":
    
    start = time.perf_counter()
    
    stt = STT()
    stt.initialize_STT()
    text = stt.get_text_from_mic()
    
    end = time.perf_counter()
    elapsed = end - start
    print(f"Tempo di analisi vocale: {elapsed:.2f} s")
    
    print("USER: ", text)
    
    nlp_result = NLP.get_response(text)
    
    print("ASSISTANT: ", nlp_result.reply_text)
    TTS.speak(nlp_result.reply_text)
    actions.handle_action(nlp_result.action, nlp_result.params)
    
    end = time.perf_counter()
    elapsed = end - start
    print(f"Tempo di esecuzione: {elapsed:.2f} s")