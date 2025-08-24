"""Configuration file for Twitter ingestion to allow easy customization."""

# Rate limiting configuration
BATCH_SIZE = 5  # Process users in smaller batches
DELAY_BETWEEN_BATCHES = 30  # seconds between batches
DELAY_BETWEEN_USERS = 2  # seconds between individual users
MAX_RETRIES = 3  # number of retries for failed requests
RETRY_DELAY = 60  # seconds to wait before retrying

# Cache configuration
CACHE_FILE = 'sample_data/user_cache.json'
CACHE_ENABLED = True

# API configuration
MAX_TWEETS_PER_USER = 50  # maximum tweets to fetch per user
USE_CUSTOM_RATE_LIMITING = True  # Use custom rate limiting instead of tweepy's built-in

# User lists - you can customize these based on your needs
ESSENTIAL_USERS = [
    'AdamSchefter',      # ESPN - Most important NFL news
    'RapSheet',          # Ian Rapoport, NFL Network - Breaking news
    'FieldYates',        # ESPN - Fantasy-focused
    'TomPelissero',      # NFL Network - Breaking news
]

FANTASY_ANALYSTS = [
    'MikeClayNFL',       # ESPN - Fantasy analysis
    'MatthewBerryTMR',   # Fantasy Analyst - High value
    'EvanSilva',         # Fantasy Analyst - High value
    'PFF',               # Pro Football Focus - Analytics
]

EXTENDED_USERS = [
    'JayGlazer',         # FOX Sports
    'MySportsUpdate',    # NFL News aggregator
    'ProFootballTalk',   # NBC Sports
    'AroundTheNFL',      # NFL Network
    'NFL',               # Official NFL
    'Rotoworld_FB',      # Rotoworld Football
    'Rotounderworld',    # Fantasy Analyst
]

# Default user list (essential + fantasy analysts for good balance)
DEFAULT_USERS = ESSENTIAL_USERS + FANTASY_ANALYSTS

# Full user list (for when you have good API limits and want comprehensive coverage)
ALL_USERS = ESSENTIAL_USERS + FANTASY_ANALYSTS + EXTENDED_USERS

def get_user_list(tier='default'):
    """
    Get user list based on tier:
    - 'essential': Only the most critical breaking news accounts (4 users)
    - 'default': Essential + fantasy analysts (8 users) 
    - 'extended': All users for comprehensive coverage (15 users)
    """
    if tier == 'essential':
        return ESSENTIAL_USERS
    elif tier == 'default':
        return DEFAULT_USERS
    elif tier == 'extended':
        return ALL_USERS
    else:
        raise ValueError(f"Unknown tier: {tier}. Use 'essential', 'default', or 'extended'")