"""Deterministic keyword-based retrieval engine for Intellizo knowledge base."""

import re
from typing import List, Optional, Set
from models.request_models import VALID_SEARCH_CATEGORIES
from models.response_models import SearchItem, SearchResponse
from services.knowledge_service import KnowledgeIndexItem, knowledge_service

STOP_WORDS: Set[str] = {
    "a", "about", "above", "after", "again", "all", "am", "an", "and", "any", "are",
    "as", "at", "be", "because", "been", "before", "being", "below", "between", "both",
    "but", "by", "could", "did", "do", "does", "doing", "down", "during", "each", "few",
    "for", "from", "further", "had", "has", "have", "having", "he", "her", "here", "hers",
    "herself", "him", "himself", "his", "how", "i", "if", "in", "into", "is", "it", "its",
    "itself", "me", "more", "most", "my", "myself", "no", "nor", "not", "of", "off", "on",
    "once", "only", "or", "other", "ought", "our", "ours", "ourselves", "out", "over", "own",
    "same", "she", "should", "so", "some", "such", "than", "that", "the", "their", "theirs",
    "them", "themselves", "then", "there", "these", "they", "this", "those", "through",
    "to", "too", "under", "until", "up", "very", "was", "we", "were", "what", "when",
    "where", "which", "while", "who", "whom", "why", "with", "would", "you", "your", "yours",
}

SYNONYMS = {
    "jobs": ["careers", "opening", "openings", "vacancies", "vacancy", "hire", "hiring"],
    "career": ["careers", "job", "jobs", "opening", "vacancy"],
    "hiring": ["careers", "jobs", "openings"],
    "vacancy": ["careers", "jobs", "openings"],
    "pricing": ["cost", "price", "plans", "budget", "rate"],
    "cost": ["pricing", "price", "budget", "fees"],
    "agents": ["ai", "agentic", "automation", "observe", "reason"],
    "protocol": ["mcp", "context", "orchestration"],
    "mcp": ["protocol", "orchestration", "context", "model context protocol"],
    "contact": ["email", "phone", "enquiry", "inquiry", "meeting", "consultation"],
    "email": ["contact", "support", "channels"],
    "research": ["paper", "papers", "article", "articles", "insights", "study"],
    "articles": ["research", "papers", "insights"],
    "service": ["services", "solutions", "offerings", "development"],
    "culture": ["values", "principles", "trust", "curiosity"],
    "team": ["teams", "roles", "engineers", "specialists"],
}


def normalize_text(text: str) -> str:
    """Normalize text by lowercasing and removing special punctuation."""
    if not text:
        return ""
    text = text.lower()
    text = re.sub(r"[^\w\s]", " ", text)
    return " ".join(text.split())


def tokenize(text: str) -> List[str]:
    """Tokenize and filter stop words."""
    norm = normalize_text(text)
    tokens = [t for t in norm.split() if t not in STOP_WORDS and len(t) > 1]
    return tokens


def expand_query_tokens(tokens: List[str]) -> Set[str]:
    """Expand query tokens using predefined synonyms."""
    expanded = set(tokens)
    for tok in tokens:
        if tok in SYNONYMS:
            expanded.update(SYNONYMS[tok])
        for key, syn_list in SYNONYMS.items():
            if tok in syn_list:
                expanded.add(key)
    return expanded


def score_item(item: KnowledgeIndexItem, query: str, query_tokens: Set[str]) -> float:
    """Deterministic scoring of a knowledge chunk against query."""
    if not query_tokens:
        return 0.0

    title_norm = normalize_text(item.title)
    content_norm = normalize_text(item.content)
    combined = f"{title_norm} {content_norm}"

    # Exact phrase match bonus
    norm_query = normalize_text(query)
    phrase_score = 0.0
    if len(norm_query) > 3 and norm_query in combined:
        phrase_score = 0.5
        if norm_query in title_norm:
            phrase_score = 0.8

    # Token overlap scoring
    title_words = set(tokenize(item.title))
    content_words = set(tokenize(item.content))

    title_matches = query_tokens.intersection(title_words)
    content_matches = query_tokens.intersection(content_words)

    # Calculate token overlap ratio
    title_weight = len(title_matches) * 0.35
    content_weight = len(content_matches) * 0.15

    total_score = phrase_score + title_weight + content_weight

    # Category matching bonus if category name is mentioned in query
    if item.category.lower() in norm_query:
        total_score += 0.2

    # Normalize to 0.0 - 1.0 range
    final_score = min(total_score, 1.0)
    return final_score


class RetrievalService:
    """Deterministic keyword retrieval engine."""

    def __init__(self):
        self.knowledge = knowledge_service

    def search(
        self,
        query: str,
        category: Optional[str] = None,
        max_results: int = 5,
        min_threshold: float = 0.15,
    ) -> SearchResponse:
        """Search knowledge base with optional category filter and relevance threshold."""
        clean_query = query.strip() if query else ""
        if not clean_query:
            return SearchResponse(
                query=query or "",
                category_filter=category,
                total_results=0,
                results=[],
            )

        # Validate category if provided
        cat_filter: Optional[str] = None
        if category:
            matched_cat = next(
                (c for c in VALID_SEARCH_CATEGORIES if c.lower() == category.strip().lower()),
                None,
            )
            if not matched_cat:
                raise ValueError(
                    f"Unknown category '{category}'. Allowed categories: {', '.join(VALID_SEARCH_CATEGORIES)}"
                )
            cat_filter = matched_cat

        all_items = self.knowledge.get_index()
        tokens = tokenize(clean_query)
        expanded_tokens = expand_query_tokens(tokens)

        scored_items: List[tuple[KnowledgeIndexItem, float]] = []
        for item in all_items:
            # Check category filter
            if cat_filter and item.category.lower() != cat_filter.lower():
                continue

            score = score_item(item, clean_query, expanded_tokens)
            if score >= min_threshold:
                scored_items.append((item, score))

        # Sort by relevance score descending
        scored_items.sort(key=lambda x: x[1], reverse=True)

        # Limit to max_results
        top_items = scored_items[:max_results]
        search_items = [item.to_search_item(score) for item, score in top_items]

        return SearchResponse(
            query=clean_query,
            category_filter=cat_filter,
            total_results=len(search_items),
            results=search_items,
        )


retrieval_service = RetrievalService()
