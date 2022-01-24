# -*- coding: utf-8 -*-
"""
@author:XuMing(xuming624@qq.com)
@description: 
"""

import sys
import unittest

sys.path.append('..')
from text2vec import SBert
import numpy as np


def use_transformers(sentences=('如何更换花呗绑定银行卡', '花呗更改绑定银行卡')):
    from transformers import BertTokenizer, BertModel
    import torch

    # Mean Pooling - Take attention mask into account for correct averaging
    def mean_pooling(model_output, attention_mask):
        token_embeddings = model_output[0]  # First element of model_output contains all token embeddings
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)

    # Load model from HuggingFace Hub
    tokenizer = BertTokenizer.from_pretrained('shibing624/text2vec-base-chinese')
    model = BertModel.from_pretrained('shibing624/text2vec-base-chinese')

    # Tokenize sentences
    encoded_input = tokenizer(sentences, padding=True, truncation=True, return_tensors='pt')

    # Compute token embeddings
    with torch.no_grad():
        model_output = model(**encoded_input)
    # Perform pooling. In this case, max pooling.
    sentence_embeddings = mean_pooling(model_output, encoded_input['attention_mask'])
    print("Sentence embeddings:")
    print(sentence_embeddings)
    return sentence_embeddings


class SBERTEmbeddingsTestCase(unittest.TestCase):
    def test_encode_text(self):
        """测试文本 text encode结果"""
        a = '如何更换花呗绑定银行卡'
        m = SBert('shibing624/text2vec-base-chinese')
        emb = m.encode(a)
        print(a, emb)
        self.assertEqual(emb.shape, (768,))

    def test_tr_emb(self):
        """测试test_tr_emb"""
        r = use_transformers()
        print(r)


if __name__ == '__main__':
    unittest.main()