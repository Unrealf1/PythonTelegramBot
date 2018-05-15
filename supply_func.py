import matplotlib.pyplot as plt
import os
import peewee
import bot_parser


def clean_all_texts():
    db = peewee.SqliteDatabase('news.db')
    bot_parser.Docs.create_table()
    docs = bot_parser.Docs.select()
    for doc in docs:
        doc.text = bot_parser.clean_text(doc.text)
        doc.save()


def clear_plots(plots):
    for plot in plots:
        os.remove(plot)


def get_docs_plot(lens):
    max_len = max(lens.keys())
    amount_len = [0] * (max_len + 1)
    for i in range(max_len + 1):
        if i in lens:
            amount_len[i] = lens[i]

    plt.scatter(range(max_len + 1), amount_len)
    plt.savefig("doc_len.png")
    plt.close()
    return "doc_len.png"


def get_plots(words, lens):
    max_len = max(lens.keys())
    amount_len = [0]*(max_len + 1)
    for i in range(max_len + 1):
        if i in lens:
            amount_len[i] = lens[i]

    plt.scatter(range(max_len + 1), amount_len)
    plt.savefig("len.png")
    plt.close()

    plt.scatter(words.keys(), words.values())
    plt.savefig("word.png")
    plt.close()
    return ("len.png", "word.png")