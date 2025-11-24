from flask import Flask, request, jsonify
import re
from spellchecker import SpellChecker
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

app = Flask(__name__)
sentiment_analyzer = SentimentIntensityAnalyzer()
spell_checker = SpellChecker()

def process_text(text):
    text = ' '.join(text.split())
    sentences = []
    for sentence in text.split('.'):
        if sentence.strip():
            sentences.append(sentence.strip())
    
    words = []
    for word in re.findall(r'\b\w+\b', text.lower()):
        words.append(word)
    
    return {
        'original_text': text,
        'sentences': sentences,
        'words': words,
        'word_count': len(words),
        'sentence_count': len(sentences)
    }

def score_salutation(text_data):
    if not text_data['sentences']:
        return 0
        
    first_sentence = text_data['sentences'][0].lower()
    
    if "i am excited" in first_sentence or "feeling great" in first_sentence:
        return 5
    
    good_phrases = ["good morning", "good afternoon", "good evening", "good day", "hello everyone"]
    for phrase in good_phrases:
        if phrase in first_sentence:
            return 4
    
    if "hi" in first_sentence or "hello" in first_sentence:
        return 2
    
    return 0

def score_keyword_presence(text_data):
    text = ' '.join(text_data['sentences']).lower()
    score = 0
    
    must_have_found = []
    
    if "myself" in text or "my name is" in text or "i am" in text:
        score += 4
        must_have_found.append("name")
    
    if "years old" in text or "age" in text:
        score += 4
        must_have_found.append("age")
    
    if "school" in text or "class" in text or "studying" in text:
        score += 4
        must_have_found.append("school/class")
    
    if "family" in text or "mother" in text or "father" in text or "parents" in text:
        score += 4
        must_have_found.append("family")
    
    if "hobby" in text or "hobbies" in text or "enjoy" in text or "like to" in text or "playing" in text or "interest" in text:
        score += 4
        must_have_found.append("hobbies")
    
    good_to_have_found = []
    
    if "about my family" in text or "special thing about my family" in text:
        score += 2
        good_to_have_found.append("about family")
    
    if "i am from" in text or "from" in text or "parents are from" in text:
        score += 2
        good_to_have_found.append("origin")
    
    if "dream" in text or "goal" in text or "ambition" in text or "want to be" in text:
        score += 2
        good_to_have_found.append("ambition")
    
    if "fun fact" in text or "interesting thing" in text or "unique" in text or "people don't know" in text:
        score += 2
        good_to_have_found.append("fun fact")
    
    if "strength" in text or "achievement" in text or "good at" in text or "proud of" in text:
        score += 2
        good_to_have_found.append("strengths")
    
    return {
        'score': score,
        'must_have_found': must_have_found,
        'good_to_have_found': good_to_have_found
    }

def score_flow(text_data):
    sentences = text_data['sentences']
    if len(sentences) < 2:
        return 0
    
    found_salutation = False
    found_basic_details = False
    found_additional_details = False
    found_closing = False
    
    for i, sentence in enumerate(sentences):
        sentence_lower = sentence.lower()
        
        if i < 2:
            if any(word in sentence_lower for word in ["hello", "hi", "good morning", "good afternoon", "good evening"]):
                found_salutation = True
        
        if any(word in sentence_lower for word in ["myself", "my name", "i am", "years old", "class", "school", "age", "from"]):
            found_basic_details = True
        
        if found_basic_details and any(word in sentence_lower for word in ["family", "hobby", "like", "enjoy", "fun fact", "favorite", "dream", "goal"]):
            found_additional_details = True
        
        if i >= len(sentences) - 2:
            if any(word in sentence_lower for word in ["thank you", "thanks", "thank"]):
                found_closing = True
    
    if found_salutation and found_basic_details and found_additional_details and found_closing:
        return 5
    else:
        return 0

def score_speech_rate(text_data, duration):
    if duration == 0:
        return 2
    
    wpm = (text_data['word_count'] / duration) * 60
    
    if wpm > 161:
        return 2
    elif wpm >= 141 and wpm <= 160:
        return 6
    elif wpm >= 111 and wpm <= 140:
        return 10
    elif wpm >= 81 and wpm <= 110:
        return 6
    else:
        return 2

def score_grammar(text_data):
    words = text_data['words']
    if len(words) == 0:
        return 2
    
    misspelled_words = spell_checker.unknown(words)
    error_count = len(misspelled_words)
    
    errors_per_100_words = (error_count / len(words)) * 100
    
    grammar_score = 1 - min(errors_per_100_words / 10, 1)
    
    if grammar_score >= 0.9:
        return 10
    elif grammar_score >= 0.7:
        return 8
    elif grammar_score >= 0.5:
        return 6
    elif grammar_score >= 0.3:
        return 4
    else:
        return 2

def score_vocabulary(text_data):
    words = text_data['words']
    if len(words) == 0:
        return 2
    
    unique_words = set()
    for word in words:
        unique_words.add(word)
    
    ttr = len(unique_words) / len(words)
    
    if ttr >= 0.9:
        return 10
    elif ttr >= 0.7:
        return 8
    elif ttr >= 0.5:
        return 6
    elif ttr >= 0.3:
        return 4
    else:
        return 2

def score_filler_words(text_data):
    filler_words_list = ["um", "uh", "like", "you know", "so", "actually", "basically", "right", "i mean", "well", "kinda", "sort of", "okay", "hmm", "ah"]
    
    words = text_data['words']
    if len(words) == 0:
        return 15
    
    filler_count = 0
    filler_words_found = []
    for word in words:
        if word in filler_words_list:
            filler_count += 1
            filler_words_found.append(word)
    
    filler_rate = (filler_count / len(words)) * 100
    
    if filler_rate <= 3:
        return 15
    elif filler_rate <= 6:
        return 12
    elif filler_rate <= 9:
        return 9
    elif filler_rate <= 12:
        return 6
    else:
        return 3

def score_sentiment(text_data):
    text = ' '.join(text_data['sentences'])
    if not text.strip():
        return 3
    
    scores = sentiment_analyzer.polarity_scores(text)
    positive_probability = scores['pos']
    
    if positive_probability >= 0.9:
        return 15
    elif positive_probability >= 0.7:
        return 12
    elif positive_probability >= 0.5:
        return 9
    elif positive_probability >= 0.3:
        return 6
    else:
        return 3

def get_detailed_analysis(text_data, duration, keyword_result):
    analysis = {}
    
    analysis['word_count'] = text_data['word_count']
    analysis['sentence_count'] = text_data['sentence_count']
    analysis['wpm'] = round((text_data['word_count'] / duration) * 60, 1) if duration > 0 else 0
    
    analysis['must_have_found'] = keyword_result['must_have_found']
    analysis['good_to_have_found'] = keyword_result['good_to_have_found']
    
    misspelled_words = spell_checker.unknown(text_data['words'])
    analysis['spelling_errors'] = len(misspelled_words)
    analysis['misspelled_words'] = list(misspelled_words)
    analysis['error_rate'] = round((len(misspelled_words) / text_data['word_count']) * 100, 1) if text_data['word_count'] > 0 else 0
    
    unique_words = set(text_data['words'])
    analysis['unique_words'] = len(unique_words)
    analysis['ttr'] = round(len(unique_words) / text_data['word_count'], 3) if text_data['word_count'] > 0 else 0
    
    filler_words_list = ["um", "uh", "like", "you know", "so", "actually", "basically", "right", "i mean", "well", "kinda", "sort of", "okay", "hmm", "ah"]
    filler_found = []
    for word in text_data['words']:
        if word in filler_words_list:
            filler_found.append(word)
    analysis['filler_words_found'] = filler_found
    analysis['filler_count'] = len(filler_found)
    analysis['filler_rate'] = round((len(filler_found) / text_data['word_count']) * 100, 1) if text_data['word_count'] > 0 else 0
    
    overall_sentiment = sentiment_analyzer.polarity_scores(' '.join(text_data['sentences']))
    analysis['sentiment'] = {
        'positive': round(overall_sentiment['pos'], 3),
        'neutral': round(overall_sentiment['neu'], 3),
        'negative': round(overall_sentiment['neg'], 3),
        'compound': round(overall_sentiment['compound'], 3)
    }
    
    sentence_sentiments = []
    for sentence in text_data['sentences']:
        sentiment_scores = sentiment_analyzer.polarity_scores(sentence)
        sentence_sentiments.append({
            'sentence': sentence,
            'positive': round(sentiment_scores['pos'], 3),
            'neutral': round(sentiment_scores['neu'], 3),
            'negative': round(sentiment_scores['neg'], 3),
            'compound': round(sentiment_scores['compound'], 3)
        })
    analysis['sentence_sentiments'] = sentence_sentiments
    
    return analysis

def calculate_total_score(transcript, duration=52):
    text_data = process_text(transcript)
    
    salutation_score = score_salutation(text_data)
    keyword_result = score_keyword_presence(text_data)
    keyword_score = keyword_result['score']
    flow_score = score_flow(text_data)
    speech_rate_score = score_speech_rate(text_data, duration)
    grammar_score = score_grammar(text_data)
    vocabulary_score = score_vocabulary(text_data)
    filler_words_score = score_filler_words(text_data)
    sentiment_score = score_sentiment(text_data)
    
    detailed_analysis = get_detailed_analysis(text_data, duration, keyword_result)
    
    scores = {
        'Salutation': salutation_score,
        'Keyword Presence': keyword_score,
        'Flow': flow_score,
        'Speech Rate': speech_rate_score,
        'Grammar': grammar_score,
        'Vocabulary': vocabulary_score,
        'Filler Words': filler_words_score,
        'Sentiment': sentiment_score
    }
    
    weights = {
        'Salutation': 5, 'Keyword Presence': 30, 'Flow': 5, 
        'Speech Rate': 10, 'Grammar': 10, 'Vocabulary': 10,
        'Filler Words': 15, 'Sentiment': 15
    }
    
    total_score = 0
    for score in scores.values():
        total_score = total_score + score
    
    max_score = 0
    for weight in weights.values():
        max_score = max_score + weight
    
    final_score = (total_score / max_score) * 100
    
    return {
        'overall_score': round(final_score, 1),
        'word_count': text_data['word_count'],
        'criteria_order': ['Salutation', 'Keyword Presence', 'Flow', 'Speech Rate', 'Grammar', 'Vocabulary', 'Filler Words', 'Sentiment'],
        'criteria_scores': scores,
        'weights': weights,
        'detailed_analysis': detailed_analysis
    }

@app.route('/')
def home():
    # Serve the HTML file directly
    with open('index.html', 'r', encoding='utf-8') as file:
        html_content = file.read()
    return html_content

@app.route('/score', methods=['POST'])
def score_transcript():
    try:
        data = request.json
        transcript = data.get('transcript', '')
        duration = int(data.get('duration', 52))
        
        if not transcript.strip():
            return jsonify({'error': 'Please enter a transcript'}), 400
        
        result = calculate_total_score(transcript, duration)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
