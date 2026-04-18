#!/usr/bin/env python3
"""
LINGUISTIC PRIMITIVES - All Language Structures Made Explicit

Not describing language. Measuring it.
How language gets structured at every level.
"""

import re
from collections import defaultdict

# ============================================================================
# PHONETIC STRUCTURES (How sound/symbols combine)
# ============================================================================

PHONETIC_PRIMITIVES = {
    # Vowels - carriers (sustain signal)
    "VOWEL": {"type": "carrier", "signal_strength": 0.9},
    "A_SOUND": {"type": "carrier", "resonance": "low"},
    "E_SOUND": {"type": "carrier", "resonance": "mid"},
    "I_SOUND": {"type": "carrier", "resonance": "high"},
    "O_SOUND": {"type": "carrier", "resonance": "low-mid"},
    "U_SOUND": {"type": "carrier", "resonance": "high-back"},
    
    # Consonants - structure (shape signal)
    "CONSONANT": {"type": "structure", "signal_strength": 0.5},
    "STOP": {"type": "consonant_class", "clarity": "high"},        # p, t, k
    "FRICATIVE": {"type": "consonant_class", "clarity": "mid"},    # s, f, sh
    "NASAL": {"type": "consonant_class", "clarity": "low"},        # m, n
    "LIQUID": {"type": "consonant_class", "clarity": "fluid"},     # r, l
    
    # Stress patterns
    "STRESS": {"type": "prosody", "emphasis": "marker"},
    "SYLLABLE": {"type": "prosody", "unit": "minimal"},
    "RHYTHM": {"type": "prosody", "pattern": "temporal"},
}

# ============================================================================
# MORPHOLOGICAL STRUCTURES (How words are built)
# ============================================================================

MORPHOLOGICAL_PRIMITIVES = {
    # Root structures
    "ROOT": {"type": "morpheme", "layer": "core", "meaning_carrier": True},
    "STEM": {"type": "morpheme", "layer": "intermediate"},
    "BOUND_MORPHEME": {"type": "morpheme", "layer": "attachment"},
    
    # Prefixes (modify before)
    "PREFIX": {"type": "modifier", "position": "pre", "typical_purpose": "negation|intensification|direction"},
    "PREFIX_UN": {"type": "negation", "example": "un+happy"},
    "PREFIX_RE": {"type": "repetition", "example": "re+do"},
    "PREFIX_PRE": {"type": "temporal", "example": "pre+view"},
    
    # Suffixes (modify after)
    "SUFFIX": {"type": "modifier", "position": "post", "typical_purpose": "tense|aspect|derivation"},
    "SUFFIX_ED": {"type": "tense", "meaning": "past"},
    "SUFFIX_ING": {"type": "aspect", "meaning": "ongoing"},
    "SUFFIX_LY": {"type": "derivation", "meaning": "adverbial"},
    "SUFFIX_TION": {"type": "nominalization", "meaning": "abstract noun"},
    
    # Compounding
    "COMPOUND": {"type": "composition", "parts": "two_or_more_roots"},
    "BLEND": {"type": "composition", "parts": "partial_fusion"},
}

# ============================================================================
# SYNTACTIC STRUCTURES (How elements arrange in valid patterns)
# ============================================================================

SYNTACTIC_PRIMITIVES = {
    # Part of speech - role in structure
    "NOUN": {"role": "argument", "function": "entity"},
    "VERB": {"role": "predicate", "function": "action|state"},
    "ADJECTIVE": {"role": "modifier", "function": "property"},
    "ADVERB": {"role": "modifier", "function": "manner|degree"},
    "PREPOSITION": {"role": "relation", "function": "spatial|temporal"},
    "CONJUNCTION": {"role": "linker", "function": "logical_connection"},
    "DETERMINER": {"role": "specifier", "function": "definiteness|quantification"},
    "PRONOUN": {"role": "argument_proxy", "function": "reference_link"},
    
    # Phrase structures
    "NOUN_PHRASE": {"type": "phrase", "head": "NOUN", "carriers": ["determiner", "adjective"]},
    "VERB_PHRASE": {"type": "phrase", "head": "VERB", "carriers": ["object", "adverb"]},
    "PREPOSITIONAL_PHRASE": {"type": "phrase", "head": "PREPOSITION", "carriers": ["noun_phrase"]},
    
    # Clause structures
    "INDEPENDENT_CLAUSE": {"type": "clause", "completeness": "full", "autonomy": True},
    "DEPENDENT_CLAUSE": {"type": "clause", "completeness": "partial", "autonomy": False},
    "RELATIVE_CLAUSE": {"type": "dependent_clause", "function": "adjectival"},
    "ADVERBIAL_CLAUSE": {"type": "dependent_clause", "function": "adverbial"},
    
    # Sentence structures
    "SIMPLE_SENTENCE": {"clauses": 1, "complexity": "low"},
    "COMPOUND_SENTENCE": {"clauses": 2, "jointure": "coordinating"},
    "COMPLEX_SENTENCE": {"clauses": 2, "jointure": "subordinating"},
    "COMPOUND_COMPLEX": {"clauses": 3, "jointure": "mixed"},
    
    # Subject-Verb-Object patterns
    "SUBJECT": {"position": "initial_typical", "role": "agent|theme"},
    "VERB": {"position": "medial_typical", "role": "predicate"},
    "OBJECT": {"position": "final_typical", "role": "patient|recipient"},
    "SVO": {"pattern": "English_typical", "language_type": "analytic"},
    "SOV": {"pattern": "Japanese_typical", "language_type": "agglutinative"},
}

# ============================================================================
# SEMANTIC STRUCTURES (How meaning is built and connected)
# ============================================================================

SEMANTIC_PRIMITIVES = {
    # Entity and reference
    "REFERENT": {"type": "meaning", "level": "basic_unit"},
    "DENOTATION": {"type": "meaning", "level": "extension"},
    "CONNOTATION": {"type": "meaning", "level": "association"},
    
    # Relationships between meanings
    "SYNONYMY": {"type": "relation", "similarity": "high", "substitutable": True},
    "ANTONYMY": {"type": "relation", "similarity": "opposite", "exclusivity": True},
    "HYPERNYMY": {"type": "relation", "direction": "general→specific"},
    "HYPONYMY": {"type": "relation", "direction": "specific→general"},
    "MERONYMY": {"type": "relation", "structure": "part→whole"},
    "HOLONYMY": {"type": "relation", "structure": "whole→part"},
    
    # Semantic roles (who does what to whom)
    "AGENT": {"role": "actor", "volition": "intentional"},
    "PATIENT": {"role": "undergoer", "volition": "affected"},
    "INSTRUMENT": {"role": "tool", "volition": "inanimate"},
    "PATIENT_BENEFICIARY": {"role": "recipient", "volition": "receives"},
    "LOCATION": {"role": "where", "feature": "spatial"},
    "TEMPORAL": {"role": "when", "feature": "temporal"},
    "CAUSE": {"role": "why", "feature": "causal"},
    "PURPOSE": {"role": "goal", "feature": "intentional"},
    
    # Semantic fields (related meanings cluster)
    "SEMANTIC_FIELD": {"type": "cluster", "proximity": "high"},
    "COLLOCATION": {"type": "co_occurrence", "probability": "statistical"},
}

# ============================================================================
# PRAGMATIC STRUCTURES (How language does things in context)
# ============================================================================

PRAGMATIC_PRIMITIVES = {
    # Speech acts - what language does
    "ASSERTION": {"type": "illocution", "aim": "state_fact", "truth_conditional": True},
    "QUESTION": {"type": "illocution", "aim": "request_information", "truth_conditional": False},
    "COMMAND": {"type": "illocution", "aim": "direct_action", "authority": "required"},
    "PROMISE": {"type": "illocution", "aim": "commit_future", "commitment": True},
    "GREETING": {"type": "illocution", "aim": "establish_contact", "social": True},
    "APOLOGY": {"type": "illocution", "aim": "express_regret", "social": True},
    "THANK": {"type": "illocution", "aim": "express_gratitude", "social": True},
    
    # Implicature - what's NOT said but implied
    "IMPLICATURE": {"type": "inference", "explicit": False, "contextual": True},
    "PRESUPPOSITION": {"type": "inference", "assumed": True, "failure": "infelicity"},
    "ENTAILMENT": {"type": "inference", "logical": True, "necessity": "truth_conditional"},
    
    # Politeness and register
    "POLITENESS": {"type": "social", "dimension": "direct↔indirect"},
    "REGISTER": {"type": "social", "dimension": "formal↔casual"},
    "HONORIFIC": {"type": "social", "function": "respect_marking"},
    
    # Discourse moves
    "INITIATE": {"type": "discourse", "position": "opening"},
    "RESPOND": {"type": "discourse", "position": "reply"},
    "ELABORATE": {"type": "discourse", "position": "extension"},
    "CLARIFY": {"type": "discourse", "position": "repair"},
}

# ============================================================================
# DISCOURSE STRUCTURES (How ideas sequence and connect across sentences)
# ============================================================================

DISCOURSE_PRIMITIVES = {
    # Coherence relations
    "TEMPORAL": {"type": "relation", "connection": "before→after"},
    "CAUSAL": {"type": "relation", "connection": "cause→effect"},
    "CONTRASTIVE": {"type": "relation", "connection": "A vs B"},
    "ELABORATIVE": {"type": "relation", "connection": "detail→general"},
    "PARALLEL": {"type": "relation", "connection": "similar_structure"},
    
    # Cohesion devices
    "ANAPHORA": {"type": "cohesion", "mechanism": "reference_backwards"},
    "CATAPHORA": {"type": "cohesion", "mechanism": "reference_forwards"},
    "ELLIPSIS": {"type": "cohesion", "mechanism": "omission_understood"},
    "CONJUNCTION": {"type": "cohesion", "mechanism": "explicit_connector"},
    "PRONOUN_CHAIN": {"type": "cohesion", "mechanism": "pronoun_continuity"},
    
    # Rhetorical structure
    "TOPIC": {"type": "structure", "role": "main_idea"},
    "FOCUS": {"type": "structure", "role": "emphasized_element"},
    "GIVEN": {"type": "structure", "status": "previously_mentioned"},
    "NEW": {"type": "structure", "status": "introduced_now"},
}

# ============================================================================
# META-LINGUISTIC STRUCTURES (How language talks about language)
# ============================================================================

META_LINGUISTIC_PRIMITIVES = {
    "QUOTATION": {"type": "meta", "mechanism": "direct_representation"},
    "PARAPHRASE": {"type": "meta", "mechanism": "meaning_preservation"},
    "METAPHOR": {"type": "meta", "mechanism": "meaning_transfer"},
    "METONYMY": {"type": "meta", "mechanism": "substitution"},
    "IRONY": {"type": "meta", "mechanism": "meaning_inversion"},
    "ALLUSION": {"type": "meta", "mechanism": "implicit_reference"},
    "HOMONYMY": {"type": "meta", "mechanism": "form_identity"},
    "AMBIGUITY": {"type": "meta", "mechanism": "multiple_parses"},
}

# ============================================================================
# LANGUAGE STRUCTURE ANALYZER
# ============================================================================

class LanguageStructureAnalyzer:
    """
    Extract linguistic structure from text.
    Measure all 8 layers: phonetic → meta-linguistic
    """
    
    def __init__(self):
        self.all_primitives = {
            "phonetic": PHONETIC_PRIMITIVES,
            "morphological": MORPHOLOGICAL_PRIMITIVES,
            "syntactic": SYNTACTIC_PRIMITIVES,
            "semantic": SEMANTIC_PRIMITIVES,
            "pragmatic": PRAGMATIC_PRIMITIVES,
            "discourse": DISCOURSE_PRIMITIVES,
            "meta_linguistic": META_LINGUISTIC_PRIMITIVES,
        }
    
    def analyze_text(self, text):
        """
        Measure linguistic complexity across all 7 layers.
        Return structure summary.
        """
        results = {
            "text": text,
            "layers_detected": [],
            "complexity": {},
            "linguistic_activation": {}
        }
        
        # Phonetic layer
        phonetic_score = self._analyze_phonetic(text)
        results["complexity"]["phonetic"] = phonetic_score
        
        # Morphological layer
        morphological_score = self._analyze_morphological(text)
        results["complexity"]["morphological"] = morphological_score
        
        # Syntactic layer
        syntactic_score = self._analyze_syntactic(text)
        results["complexity"]["syntactic"] = syntactic_score
        
        # Semantic layer
        semantic_score = self._analyze_semantic(text)
        results["complexity"]["semantic"] = semantic_score
        
        # Pragmatic layer
        pragmatic_score = self._analyze_pragmatic(text)
        results["complexity"]["pragmatic"] = pragmatic_score
        
        # Discourse layer
        discourse_score = self._analyze_discourse(text)
        results["complexity"]["discourse"] = discourse_score
        
        # Meta-linguistic layer
        meta_score = self._analyze_meta_linguistic(text)
        results["complexity"]["meta_linguistic"] = meta_score
        
        # Overall linguistic complexity
        scores = list(results["complexity"].values())
        results["overall_complexity"] = sum(scores) / len(scores) if scores else 0
        
        return results
    
    def _analyze_phonetic(self, text):
        """Measure phonetic complexity: vowel/consonant ratio, syllable count."""
        vowels = len(re.findall(r'[aeiou]', text.lower()))
        consonants = len(re.findall(r'[bcdfghjklmnpqrstvwxyz]', text.lower()))
        total_chars = len(text)
        
        if total_chars == 0:
            return 0
        
        # Complexity: varied vowel/consonant ratio indicates richer phonetic structure
        ratio = vowels / max(1, consonants)
        complexity = min(1.0, ratio / 2)  # Normalize
        return complexity
    
    def _analyze_morphological(self, text):
        """Measure morphological complexity: affixes, compounding."""
        words = text.lower().split()
        affix_count = 0
        
        affixes = ['un', 're', 'pre', 'dis', 'ed', 'ing', 'ly', 'tion', 'ness']
        for word in words:
            for affix in affixes:
                if affix in word:
                    affix_count += 1
        
        complexity = min(1.0, affix_count / max(1, len(words)))
        return complexity
    
    def _analyze_syntactic(self, text):
        """Measure syntactic complexity: clause count, sentence length."""
        sentences = re.split(r'[.!?;]', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if not sentences:
            return 0
        
        # Multiple clauses indicated by conjunctions and subordinators
        coord_conj = len(re.findall(r'\b(and|but|or|nor)\b', text.lower()))
        subord_conj = len(re.findall(r'\b(because|although|since|if|while)\b', text.lower()))
        
        total_conj = coord_conj + subord_conj
        complexity = min(1.0, (total_conj / len(sentences)) / 3)
        return complexity
    
    def _analyze_semantic(self, text):
        """Measure semantic complexity: lexical diversity, semantic relationships."""
        words = text.lower().split()
        unique_words = len(set(words))
        
        if not words:
            return 0
        
        # Lexical diversity: unique words / total words (Type/Token ratio)
        complexity = unique_words / len(words)
        return min(1.0, complexity)
    
    def _analyze_pragmatic(self, text):
        """Measure pragmatic complexity: speech acts, politeness markers."""
        text_lower = text.lower()
        
        # Speech act markers
        questions = len(re.findall(r'\?', text))
        commands = len(re.findall(r'(please|must|should)', text_lower))
        politeness = len(re.findall(r'(please|thank|sorry|excuse)', text_lower))
        
        total = questions + commands + politeness
        complexity = min(1.0, total / max(1, len(text.split())))
        return complexity
    
    def _analyze_discourse(self, text):
        """Measure discourse complexity: coherence markers, reference chains."""
        text_lower = text.lower()
        
        # Discourse markers
        markers = len(re.findall(r'\b(however|therefore|moreover|thus|hence)\b', text_lower))
        
        # Reference chains (pronouns)
        pronouns = len(re.findall(r'\b(he|she|it|they|this|that|these|those)\b', text_lower))
        
        total = markers + pronouns
        complexity = min(1.0, total / max(1, len(text.split())))
        return complexity
    
    def _analyze_meta_linguistic(self, text):
        """Measure meta-linguistic complexity: figures of speech, citations."""
        text_lower = text.lower()
        
        # Quotation marks and meta-discourse
        quotes = len(re.findall(r'["\']', text))
        meta = len(re.findall(r'\b(like|as|says|means|implies)\b', text_lower))
        
        total = quotes + meta
        complexity = min(1.0, total / max(1, len(text.split())))
        return complexity


# ============================================================================
# EXPORT FOR INTEGRATION
# ============================================================================

def get_all_linguistic_primitives():
    """Return all linguistic primitives organized by layer."""
    analyzer = LanguageStructureAnalyzer()
    return analyzer.all_primitives

def analyze_linguistic_structure(text):
    """Analyze text for all linguistic structures."""
    analyzer = LanguageStructureAnalyzer()
    return analyzer.analyze_text(text)
