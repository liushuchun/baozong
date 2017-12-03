import jieba
from jieba import posseg as psg
import operator


def load_stop_words(path="stop_words.utf8"):
    from codecs import open
    stop_words = set()
    with open(path, 'r', encoding='utf8') as f:
        for l in f:
            l = l.strip()
            stop_words.add(l)
    return stop_words


class WordAnalyzer:
    def __init__(self):
        self.stop_words = load_stop_words()

    def cut_words(self, words):
        words = psg.cut(words)
        return [w for w, t in words if w not in self.stop_words]

    def process(self, file_name, top_k=-1):
        """
        
        :param file_name: file path
        :param top_k: if top_k=-1 print all, else top k
        :return: tuple
        """
        article = ""
        with open(file_name, encoding='utf8') as f:
            for line in f:
                article += line.strip('\n')
        print("here")
        print(article)

        words = self.cut_words(article)

        word_statics = {}

        for word in words:
            counts = word_statics.get(word, 0)
            word_statics[word] = counts + 1

        sorted_words = sorted(word_statics.items(), key=operator.itemgetter(1), reverse=True)

        assert (isinstance(top_k, int))

        if top_k < 0:
            return sorted_words
        else:
            return sorted_words[0:top_k]

    def show_plt(self, word_count):
        import matplotlib.pyplot as plt
        from pylab import mpl
        mpl.rcParams['font.sans-serif'] = ['FangSong']
        mpl.rcParams['axes.unicode_minus'] = False

        label = list(map(lambda x: x[0], word_count))
        value = list(map(lambda y: y[1], word_count))
        plt.bar(range(len(value)), value, tick_label=label)
        plt.show()


if __name__ == "__main__":
    analyzer = WordAnalyzer()

    words_tuple = analyzer.process("ocr_v4_recog/weibo/005Zu0d2ly1fliuvdf9k8j30hs2p515r.jpg.txt")

    print(words_tuple)
    analyzer.show_plt(words_tuple[:10])


