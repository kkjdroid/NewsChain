def markov():
    import markovify
    from sample import sample_from_file
    from scrape import remove_emoji
    sample = filter_headlines(sample_from_file())['headlines']
    #markov_lines = remove_emoji('\n'.join(sample))
    markov_lines = '\n'.join(sample)
    text_model = markovify.NewlineText(markov_lines)
    return text_model.make_short_sentence(50, tries=100)

def filter_headlines(lines):
    quizzes = [_ for _ in lines if 'Quiz' in _ or 'And We\'ll' in _]
    lists = [_ for _ in lines if _[0].isdigit()]
    headlines = [_ for _ in lines if _ not in quizzes and _ not in lists]
    return ({'headlines': headlines, 'lists': lists, 'quizzes': quizzes})
