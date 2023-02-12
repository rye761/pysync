import whisper
import math

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

def get_segments(vocal_filename, model_size="medium"):
    model = whisper.load_model(model_size)
    result = model.transcribe(vocal_filename)
    print(f"Segments: {len(result['segments'])}")
    return result['segments']

def sync_segments(lyrics, segments):
    lyrics_synced = []
    lyrics_unsynced = lyrics.split('\n')

    for segment in segments:
        top_similarity = 0.0
        top_similarity_final_index = 1
        
        for i in range(1, len(lyrics_unsynced)):
            trial_text = ' '.join(lyrics_unsynced[:i])
            trial_similarity = jaccard_similarity(trial_text, segment['text'])
            if trial_similarity > top_similarity:
                top_similarity = trial_similarity
                top_similarity_final_index = i
        lyrics_synced = lyrics_synced + list(map(lambda x: f"[{math.floor(segment['start']/60):02d}:{math.floor(segment['start'] % 60):02d}.00] {x}\n", lyrics_unsynced[:top_similarity_final_index]))
        lyrics_unsynced = lyrics_unsynced[top_similarity_final_index:]

        
    lyrics_synced = lyrics_synced + list(map(lambda x: f"[{math.floor(segments[-1]['start']/60):02d}:{math.floor(segments[-1]['start'] % 60):02d}.00] {x}\n", lyrics_unsynced[0:]))
        
    return lyrics_synced