import torch
from tokenizer import koGPT2_TOKENIZER, Q_TKN, A_TKN, SENT, EOS
import parameter
from model import KoGPT2ChatbotModel

def chat():
    chatbot_model = KoGPT2ChatbotModel()
    checkpoint = torch.load(parameter.model_save_path)
    chatbot_model.model.load_state_dict(checkpoint['model_state_dict'])
    chatbot_model.model.eval()

    device = chatbot_model.device

    with torch.no_grad():
        while 1:
            q = input("user > ").strip()
            if q == "quit":
                break
            a = ""
            while 1:
                input_ids = torch.LongTensor(koGPT2_TOKENIZER.encode(Q_TKN + q + SENT + A_TKN + a)).unsqueeze(dim=0).to(device)
                pred = chatbot_model.model(input_ids)
                logits = pred.logits
                logits = logits[:, -1, :]
                probs = logits.softmax(dim=-1)
                top_prob, top_idx = torch.topk(probs, k=1, dim=-1)
                gen_token_id = top_idx.item()
                gen = koGPT2_TOKENIZER.convert_ids_to_tokens(gen_token_id)
                if gen == EOS:
                    break
                a += gen.replace("▁", " ")
            print("Chatbot > {}".format(a.strip()))

if __name__ == "__main__":
    chat()