import difflib

def split_into_paragraphs(text):
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    return paragraphs

def compare_documents(text_v1, text_v2, similarity_threshold=0.8):
    v1_paragraphs = split_into_paragraphs(text_v1)
    v2_paragraphs = split_into_paragraphs(text_v2)

    matched_v1 = set()
    matched_v2 = set()

    changes = []

    for i2, p2 in enumerate(v2_paragraphs):
        best_ratio = 0
        best_i1 = -1
        for i1, p1 in enumerate(v1_paragraphs):
            ratio = difflib.SequenceMatcher(None, p1, p2).ratio()
            if ratio > best_ratio:
                best_ratio = ratio
                best_i1 = i1

        if best_ratio >= similarity_threshold:
            matched_v1.add(best_i1)
            matched_v2.add(i2)
            if best_ratio < 0.99:
                changes.append({
                    'change_type': 'Modified',
                    'old_text': v1_paragraphs[best_i1],
                    'new_text': p2
                })
        else:
            changes.append({
                'change_type': 'Added',
                'new_text': p2
            })

    for i1, p1 in enumerate(v1_paragraphs):
        if i1 not in matched_v1:
            changes.append({
                'change_type': 'Deleted',
                'old_text': p1
            })

    return changes
