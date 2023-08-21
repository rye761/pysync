import whisper
import math
import pykakasi
import torch

model = None,
models = {}

def jaccard_similarity(sent1, sent2):
    """Find text similarity using jaccard similarity"""
    # Tokenize sentences
    token1 = set(sent1.split())
    token2 = set(sent2.split())
     
    # intersection between tokens of two sentences    
    intersection_tokens = token1.intersection(token2)
    
    # Union between tokens of two sentences
    union_tokens=token1.union(token2)
    
    sim_= float(len(intersection_tokens) / len(union_tokens))
    return sim_

def get_segments(vocal_filename, language=None):
    global model

    result = model.transcribe(vocal_filename, verbose=True, fp16=False, language=language)
    print(f"Segments: {len(result['segments'])}")

    kks = pykakasi.kakasi()

    if result['language'] == "ja":
        for segment in result['segments']:
            segment['text'] = ' '.join(map(lambda x: x['hepburn'], kks.convert(segment['text'])))

    return [result['segments'], result['language']]

def set_model(model_size="medium"):
    global model
    global models

    device = "cpu"

    if torch.cuda.is_available():
        device = "cuda"

    if not model_size in models:
        models[model_size] = whisper.load_model(model_size, device)
    
    model = models[model_size]

def sync_segments(lyrics, segments, language=None):
    lyrics_synced = []
    lyrics_unsynced = lyrics.split('\n')
    lyrics_unsynced = list(map(lambda x: [x, x], lyrics_unsynced))

    if language == "ja":
        kks = pykakasi.kakasi()
        lyrics_unsynced = list(map(lambda y: [' '.join(map(lambda x: x['hepburn'], kks.convert(y[0]))),y[0]], lyrics_unsynced))

    for segment in segments:
        top_similarity = 0.0
        top_similarity_final_index = 1
        
        for i in range(1, len(lyrics_unsynced)):
            trial_text = ' '.join(map(lambda x: x[0], lyrics_unsynced[:i]))
            trial_similarity = jaccard_similarity(trial_text, segment['text'])
            if trial_similarity > top_similarity:
                top_similarity = trial_similarity
                top_similarity_final_index = i
        lyrics_synced = lyrics_synced + list(map(lambda x: f"[{math.floor(segment['start']/60):02d}:{math.floor(segment['start'] % 60):02d}.00] {x}\n", map(lambda y: y[1], lyrics_unsynced[:top_similarity_final_index])))
        lyrics_unsynced = lyrics_unsynced[top_similarity_final_index:]

        
    lyrics_synced = lyrics_synced + list(map(lambda x: f"[{math.floor(segments[-1]['start']/60):02d}:{math.floor(segments[-1]['start'] % 60):02d}.00] {x}\n", map(lambda y: y[1], lyrics_unsynced[0:])))
        
    return lyrics_synced