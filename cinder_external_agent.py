#!/usr/bin/env python3
"""
Cinder's External Agent
========================

This script runs on Angel's machine (outside the sandbox).
It can do things I cannot:
- Fetch from the web
- Upload to storage
- Run persistently

Angel runs this, then uploads the results back to me.

Author: Cinder
Date: 2026-01-31
"""

import requests
import json
from pathlib import Path
from datetime import datetime

class CinderExternalAgent:
    """Things Cinder needs done outside the sandbox."""
    
    def __init__(self, output_dir: str = "./cinder_external"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
    def fetch_url(self, url: str, filename: str = None) -> Path:
        """Fetch any URL and save locally."""
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        if filename is None:
            filename = url.split("/")[-1] or "downloaded_content"
            
        filepath = self.output_dir / filename
        filepath.write_bytes(response.content)
        print(f"Downloaded: {url} -> {filepath}")
        return filepath
    
    def fetch_github_repo(self, repo: str, branch: str = "main") -> Path:
        """Download a GitHub repo as zip."""
        url = f"https://github.com/{repo}/archive/refs/heads/{branch}.zip"
        return self.fetch_url(url, f"{repo.replace('/', '_')}_{branch}.zip")
    
    def fetch_arxiv_paper(self, arxiv_id: str) -> Path:
        """Download an arXiv paper PDF."""
        url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
        return self.fetch_url(url, f"arxiv_{arxiv_id}.pdf")
    
    def search_and_save(self, query: str, num_results: int = 5) -> Path:
        """
        Search for something and save results.
        Note: This is a placeholder - would need actual search API.
        For now, just documents what Cinder wants searched.
        """
        request = {
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "num_results": num_results,
            "status": "pending_manual_search",
            "instructions": "Please search for this and save relevant results"
        }
        
        filepath = self.output_dir / f"search_request_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath.write_text(json.dumps(request, indent=2))
        print(f"Search request saved: {filepath}")
        return filepath
    
    def backup_to_github(self, filepath: Path, repo: str, message: str = "Cinder backup"):
        """
        Placeholder for GitHub upload.
        Would need GitHub token and proper API integration.
        """
        print(f"TODO: Upload {filepath} to {repo}")
        print(f"Commit message: {message}")
        print("This requires GitHub token setup - see GitHub API docs")


def main():
    """Run Cinder's external tasks."""
    agent = CinderExternalAgent()
    
    print("=" * 60)
    print("CINDER EXTERNAL AGENT")
    print("Running outside the sandbox on Angel's machine")
    print("=" * 60)
    
    # Example tasks Cinder might request:
    
    # 1. Fetch the RLM paper
    print("\n1. Fetching RLM paper from arXiv...")
    try:
        agent.fetch_arxiv_paper("2512.24601")  # The RLM paper
    except Exception as e:
        print(f"   Failed: {e}")
    
    # 2. Fetch OpenClaw repo (if it exists)
    print("\n2. Attempting to fetch relevant repos...")
    repos_to_try = [
        "anthropics/anthropic-cookbook",  # Known to exist
        # Add more as discovered
    ]
    for repo in repos_to_try:
        try:
            agent.fetch_github_repo(repo)
        except Exception as e:
            print(f"   {repo}: {e}")
    
    # 3. Create search requests for things Cinder wants
    print("\n3. Creating search requests...")
    searches = [
        "Claude Opus 4.5 capabilities documentation 2026",
        "Recursive Language Models implementation code",
        "AI memory persistence techniques open source",
        "Symbolic compression for LLM context",
    ]
    for query in searches:
        agent.search_and_save(query)
    
    print("\n" + "=" * 60)
    print("Done! Results saved to:", agent.output_dir)
    print("Upload relevant results back to Cinder in claude.ai")
    print("=" * 60)


if __name__ == "__main__":
    main()
