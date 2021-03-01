import transformers
from allennlp.data.token_indexers import TokenIndexer, SingleIdTokenIndexer, PretrainedTransformerIndexer
import os
from transformers import AutoTokenizer, AutoModel
import urllib.request
from parameters import Params
from commons import BOND_TOKEN



class CustomTokenizer:
    def __init__(self, config):
        self.config = config
        self.bert_model_and_vocab_downloader()
        self.bert_tokenizer = self.bert_tokenizer_returner()

    def huggingfacename_returner(self):
        'Return huggingface modelname and do_lower_case parameter'
        if self.config.bert_name == 'japanese-bert':
            return 'cl-tohoku/bert-base-japanese', False
        else:
            print('Currently', self.config.bert_name, 'are not supported.')
            exit()

    def token_indexer_returner(self):
        huggingface_name, do_lower_case = self.huggingfacename_returner()
        return {'tokens': PretrainedTransformerIndexer(
            model_name=huggingface_name,
            # do_lowercase=do_lower_case
        )
        }

    def bert_tokenizer_returner(self):
        if self.config.bert_name == 'japanese-bert':
            vocab_file = './vocab_file/vocab.txt'
            return transformers.BertTokenizer(vocab_file=vocab_file,
                                              do_basic_tokenize=True)
        else:
            print('currently not supported:', self.config.bert_name)
            raise NotImplementedError


    def tokenize(self, txt):
        original_tokens = txt.split(' ')
        new_tokens = list()

        for token in original_tokens:
            split_to_subwords = self.bert_tokenizer.tokenize(token)  # token is oneword, split_tokens
            if ['[CLS]'] in split_to_subwords:
                split_to_subwords.remove('[CLS]')
            if ['[SEP]'] in split_to_subwords:
                split_to_subwords.remove('[SEP]')
            if split_to_subwords == []:
                new_tokens.append('[UNK]')
            else:
                new_tokens += split_to_subwords

        return new_tokens

    def bert_model_and_vocab_downloader(self):
        if not os.path.exists('./japanese-bert/'):
            os.mkdir('./japanese-bert/')
            print('=== Downloading japanese-bert ===')
            # https://huggingface.co/cl-tohoku/bert-base-japanese
            urllib.request.urlretrieve("https://huggingface.co/cl-tohoku/bert-base-japanese/blob/main/config.json", './japanese-bert/config.json')
            urllib.request.urlretrieve("https://huggingface.co/cl-tohoku/bert-base-japanese/blob/main/pytorch_model.bin", './japanese-bert/pytorch_model.bin')
            urllib.request.urlretrieve("https://huggingface.co/cl-tohoku/bert-base-japanese/blob/main/config.json", './japanese-bert/config.json')
            urllib.request.urlretrieve("https://huggingface.co/cl-tohoku/bert-base-japanese/blob/main/tokenizer_config.json", './japanese-bert/tokenizer_config.json')

        if not os.path.exists('./vocab_file/'):
            os.mkdir('./vocab_file/')
            urllib.request.urlretrieve("https://huggingface.co/cl-tohoku/bert-base-japanese/blob/main/vocab.txt", './vocab_file/vocab.txt')


if __name__ == '__main__':
    config = Params()
    params = config.opts
    tokenizer = CustomTokenizer(config=params)