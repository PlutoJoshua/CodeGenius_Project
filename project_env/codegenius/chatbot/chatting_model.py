import torch
from tokenizer import koGPT2_TOKENIZER, Q_TKN, A_TKN, SENT, EOS
from model import KoGPT2ChatbotModel

def chatting_model(user_input, model_path):
    chatbot_model = KoGPT2ChatbotModel()
    checkpoint = torch.load(model_path)
    chatbot_model.model.load_state_dict(checkpoint['model_state_dict'])
    chatbot_model.model.eval()

    device = chatbot_model.device

    response = ""  

    with torch.no_grad():
        q = user_input.strip() 
        a = ""  
        while True:
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
        response = a.strip()

    return response