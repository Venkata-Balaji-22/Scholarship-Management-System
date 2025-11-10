from typing import List, Dict

SCHOLARSHIPS: List[Dict] = [
    {
        "name": "National Merit Scholarship (Engineering)",
        "track": "engineering",
        "min_10_cgpa": 8.5,
        "min_inter_cgpa": 8.0,
        "min_btech_cgpa": 7.5,
        "max_income": 800000,
        "category": ["GEN", "OBC", "SC", "ST"],
        "states": ["ALL"],
        "url": "https://example.org/national-merit-engineering",
        "posted_at": "2025-07-15T09:00:00Z"
    },
    {
        "name": "State Talent Scholarship (Intermediate)",
        "track": "intermediate",
        "min_10_cgpa": 8.8,
        "min_inter_cgpa": 0.0,
        "min_btech_cgpa": 0.0,
        "max_income": 1000000,
        "category": ["GEN", "OBC", "SC", "ST"],
        "states": ["TS", "AP"],
        "url": "https://example.org/state-talent-intermediate",
        "posted_at": "2025-08-01T10:30:00Z"
    },
    {
        "name": "Tech Excellence Grant", 
        "track": "engineering",
        "min_10_cgpa": 9.0,
        "min_inter_cgpa": 8.5,
        "min_btech_cgpa": 8.0,
        "max_income": 1500000,
        "category": ["GEN", "OBC", "SC", "ST"],
        "states": ["ALL"],
        "url": "https://example.org/tech-excellence",
        "posted_at": "2025-07-28T14:15:00Z"
    },
    {
        "name": "Girl Child Scholarship",
        "track": "engineering",
        "min_10_cgpa": 7.5,
        "min_inter_cgpa": 7.0,
        "min_btech_cgpa": 7.0,
        "max_income": 1200000,
        "category": ["GEN", "OBC", "SC", "ST"],
        "states": ["ALL"],
        "url": "https://example.org/girl-child-scholarship",
        "posted_at": "2025-08-10T08:45:00Z"
    },
    {
        "name": "Undergraduate Aid (Intermediate)",
        "track": "intermediate",
        "min_10_cgpa": 8.0,
        "min_inter_cgpa": 0.0,
        "min_btech_cgpa": 0.0,
        "max_income": 1200000,
        "category": ["GEN", "OBC", "SC", "ST"],
        "states": ["ALL"],
        "url": "https://example.org/ug-aid-inter",
        "posted_at": "2025-08-05T11:20:00Z"
    }
]
