"""Classification rules of The AI Crawler Identity Report, round one.

These are the exact rules behind every published figure. analyze.py imports
them; nothing in the tables is set by hand.
"""
import re

# (substring in the user agent, crawler name, operator). Matched without regard
# to case. First match wins, so the more specific names come first.
# ChatGPT-User and OAI-SearchBot stay separate on purpose: one is a live fetch
# for a person's question, the other is the index crawler.
CRAWLERS = [
    ("chatgpt-user", "ChatGPT-User", "OpenAI"),
    ("oai-searchbot", "OAI-SearchBot", "OpenAI"),
    ("gptbot", "GPTBot", "OpenAI"),
    ("claude-user", "Claude-User", "Anthropic"),
    ("claude-searchbot", "Claude-SearchBot", "Anthropic"),
    ("claudebot", "ClaudeBot", "Anthropic"),
    ("anthropic-ai", "anthropic-ai", "Anthropic"),
    ("perplexity-user", "Perplexity-User", "Perplexity"),
    ("perplexitybot", "PerplexityBot", "Perplexity"),
    ("meta-externalfetcher", "Meta-ExternalFetcher", "Meta"),
    ("meta-externalagent", "Meta-ExternalAgent", "Meta"),
    ("facebookbot", "FacebookBot", "Meta"),
    ("applebot", "Applebot", "Apple"),
    ("amazonbot", "Amazonbot", "Amazon"),
    ("bytespider", "Bytespider", "ByteDance"),
    ("ccbot", "CCBot", "CommonCrawl"),
    ("googlebot", "Googlebot", "Google"),
    ("bingpreview", "BingPreview", "Microsoft"),
    ("bingbot", "BingBot", "Microsoft"),
    ("baiduspider", "Baiduspider", "Baidu"),
]

# Cloudflare verified none of these crawlers' requests in this data. An
# unverified request carrying one of these names is kept on its own line,
# unless it asks for a secret file, in which case it counts as impersonation.
UNVERIFIABLE = {"PerplexityBot", "Perplexity-User"}

# Well-known secret files and routes, hidden or not.
SECRET_FILE = re.compile(
    r"(^|/)\.(env|git|ssh|aws|azure|docker|kube|codeium|cursor|streamlit|vscode|npmrc|pypirc)(/|$|\.)"
    r"|/@fs/|(^|/)id_(rsa|ed25519)|terraform\.tfstate|(^|/)credentials(\.[a-z]+)?$"
    r"|secrets?\.(toml|json|ya?ml)$|google-cloud-key|(^|/)wp-config|/etc/passwd|/proc/self"
    r"|(^|/)[a-z0-9_-]*\.env$", re.I)

# Any hidden file or folder (a path segment that starts with a dot), except
# /.well-known/, the standard public location. A static site serves no hidden
# files, so no legitimate visitor has a reason to ask for one.
HIDDEN_PATH = re.compile(r"(^|/)\.(?!well-known/)[A-Za-z0-9_-]")

# A user agent that names some bot other than the crawlers above.
BOTLIKE = re.compile(r"bot|crawl|spider|agent|fetch|scrap|preview", re.I)

# What a secret-file probe was after. Checked in this order; first match wins.
TARGETS = [
    ("AI tool and agent credentials", re.compile(
        r"\.claude|\.anthropic|openai|\.codex|\.cursor|\.windsurf|\.codeium|\.continue|\.aider"
        r"|\.gemini|opencode|\.openclaw|\.hermes|\.mcp|mcp\.json|mcp_config", re.I)),
    ("cloud credentials", re.compile(
        r"\.aws|\.azure|google-cloud|gcloud|application_default_credentials|\.vultr|\.kube|\.docker"
        r"|terraform|\.boto|credentials", re.I)),
    ("SSH keys", re.compile(r"\.ssh|id_rsa|id_ed25519", re.I)),
    ("environment files", re.compile(r"\.env|/proc/self/environ", re.I)),
    ("version control and CI", re.compile(r"(^|/)\.(git|svn|hg)(/|$)|\.gitlab-ci|\.github/", re.I)),
    ("shell history and password files", re.compile(
        r"_history|\.htpasswd|\.netrc|\.msmtprc|\.pgpass|\.npmrc|\.pypirc|\.bash_profile|\.bashrc|\.zshrc|\.profile", re.I)),
    ("app and server config", re.compile(r"wp-config|/etc/passwd|secrets?\.(toml|json|ya?ml)|\.streamlit", re.I)),
]
VITE_FS = re.compile(r"/@fs/")


def classify(user_agent):
    """Return (crawler, operator) for the first crawler name in the user agent, or (None, None)."""
    lowered = (user_agent or "").lower()
    for token, crawler, operator in CRAWLERS:
        if token in lowered:
            return crawler, operator
    return None, None


def is_probe(path):
    """True when the request asks for a secret file."""
    return bool(SECRET_FILE.search(path) or HIDDEN_PATH.search(path))


def target(path):
    for name, rx in TARGETS:
        if rx.search(path):
            return name
    return "other"


def disguise(agent, crawler):
    if crawler:
        return "AI crawler name"
    if not agent:
        return "no user agent"
    if BOTLIKE.search(agent):
        return "other bot name"
    return "no bot name in the user agent"
