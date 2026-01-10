#!/usr/bin/env python3

"""
Skills MCP Server - provides access to specialized skills for AI coding agents.

This server enables AI coding agents (like Cursor) to discover and invoke
specialized skills from the skills directory, following the skills pattern
pioneered by Claude Code.

Enhanced with trusted source browsing and selective skill imports.
"""
# /// script
# dependencies = ["fastmcp", "pyyaml"]
# ///

import os
import re
import urllib.request
import json
import shutil
from pathlib import Path
from fastmcp import FastMCP

# Create the MCP server
mcp = FastMCP(
    name="cursor-skills",
    instructions="A skills server that provides access to specialised, reusable capabilities through list_skills, invoke_skill, browse_skills, and import_skills tools."
)

# Get project root (parent of mcp directory)
project_root = Path(__file__).parent.parent


def _load_skill_sources() -> dict:
    """Load skill sources from config file.
    
    Returns:
        Dictionary of source configurations
    """
    config_path = project_root / "skill_sources.yaml"
    
    if not config_path.exists():
        return {}
    
    try:
        # Simple YAML parser for our specific format
        content = config_path.read_text(encoding='utf-8')
        sources = {}
        current_source = None
        
        for line in content.split('\n'):
            # Skip comments and empty lines
            if line.strip().startswith('#') or not line.strip():
                continue
            
            # Check for source name (ends with :, not indented under sources:)
            if line.startswith('  ') and not line.startswith('    ') and line.strip().endswith(':'):
                if 'sources:' not in line:
                    current_source = line.strip().rstrip(':')
                    sources[current_source] = {}
            elif line.startswith('    ') and current_source and ':' in line:
                # Parse key: value under a source
                key, value = line.strip().split(':', 1)
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                sources[current_source][key] = value
        
        return sources
    except Exception as e:
        return {}


def _discover_skills(base_dir: Path, prefix: str = "") -> list:
    """Recursively discover skills in directory tree.
    
    Args:
        base_dir: Directory to search for skills
        prefix: Prefix for nested skill names (e.g., "document-skills/")
    
    Returns:
        List of tuples (skill_name, skill_path)
    """
    skills = []
    
    if not base_dir.exists():
        return skills
    
    for item in sorted(base_dir.iterdir()):
        if not item.is_dir() or item.name.startswith('.'):
            continue
            
        skill_md = item / "SKILL.md"
        skill_name = f"{prefix}{item.name}" if prefix else item.name
        
        # If this directory has a SKILL.md, it's a skill
        if skill_md.exists():
            skills.append((skill_name, item))
        else:
            # Otherwise, recursively search subdirectories
            nested_skills = _discover_skills(item, f"{skill_name}/")
            skills.extend(nested_skills)
    
    return skills


def _extract_frontmatter(content: str) -> dict:
    """Extract YAML frontmatter from markdown content.
    
    Args:
        content: Markdown content with optional YAML frontmatter
        
    Returns:
        Dictionary of frontmatter fields
    """
    if not content.startswith('---'):
        return {}
    
    # Find the closing ---
    lines = content.split('\n')
    end_index = -1
    for i in range(1, len(lines)):
        if lines[i].strip() == '---':
            end_index = i
            break
    
    if end_index == -1:
        return {}
    
    # Parse the frontmatter (simple key: value parser)
    frontmatter = {}
    for line in lines[1:end_index]:
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            frontmatter[key] = value
    
    return frontmatter


def _list_skills_impl() -> str:
    """Internal implementation for listing skills."""
    skills_dir = project_root / "skills"
    
    if not skills_dir.exists():
        return "No skills directory found. Create a 'skills' directory to add skills."
    
    discovered_skills = _discover_skills(skills_dir)
    
    if not discovered_skills:
        return "No skills found in the skills directory."
    
    skill_tags = []
    for skill_name, skill_path in discovered_skills:
        skill_md = skill_path / "SKILL.md"
        try:
            content = skill_md.read_text(encoding='utf-8')
            # Extract description from YAML frontmatter
            frontmatter = _extract_frontmatter(content)
            description = frontmatter.get('description', 'No description available')
            skill_tags.append(f"<skill name='{skill_name}'>{description}</skill>")
        except Exception as e:
            skill_tags.append(f"<skill name='{skill_name}'>Error reading skill: {e}</skill>")
    
    return "\n".join(skill_tags)


def _invoke_skill_impl(skill_name: str) -> str:
    """Internal implementation for invoking a skill."""
    skills_dir = project_root / "skills"
    
    # Handle nested skill paths (e.g., "document-skills/pdf")
    skill_path = skills_dir / skill_name
    
    if not skill_path.exists():
        # Get list of all available skills including nested ones
        discovered_skills = _discover_skills(skills_dir)
        available = [name for name, _ in discovered_skills]
        return f"Skill '{skill_name}' not found. Available skills: {', '.join(available)}"
    
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return f"Skill '{skill_name}' found but SKILL.md is missing."
    
    try:
        content = skill_md.read_text(encoding='utf-8')
        return f"# {skill_name} Skill\n\n{content}"
    except Exception as e:
        return f"Error reading skill '{skill_name}': {e}"


def _parse_github_url(url: str) -> dict:
    """Parse a GitHub URL to extract components.
    
    Args:
        url: GitHub URL (repo or subdirectory)
        
    Returns:
        Dictionary with owner, repo, branch, and path
    """
    # Handle both https and git URLs
    pattern = r'github\.com/([^/]+)/([^/]+)(?:/tree/([^/]+)/(.+))?'
    match = re.search(pattern, url)
    
    if not match:
        return None
    
    owner, repo, branch, path = match.groups()
    
    # Remove .git suffix if present
    if repo.endswith('.git'):
        repo = repo[:-4]
    
    return {
        'owner': owner,
        'repo': repo,
        'branch': branch or 'main',
        'path': path or ''
    }


def _fetch_github_directory_contents(owner: str, repo: str, path: str, branch: str) -> list:
    """Fetch directory contents from GitHub API without downloading.
    
    Args:
        owner: Repository owner
        repo: Repository name
        path: Path within repository
        branch: Branch name
        
    Returns:
        List of directory items or empty list on error
    """
    try:
        api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}?ref={branch}"
        
        req = urllib.request.Request(api_url)
        req.add_header('Accept', 'application/vnd.github.v3+json')
        req.add_header('User-Agent', 'cursor-skills-mcp')
        
        with urllib.request.urlopen(req, timeout=10) as response:
            contents = json.loads(response.read().decode())
        
        if isinstance(contents, list):
            return contents
        return []
    except Exception:
        return []


def _fetch_skill_frontmatter(owner: str, repo: str, skill_path: str, branch: str) -> dict:
    """Fetch just the SKILL.md frontmatter from GitHub.
    
    Args:
        owner: Repository owner
        repo: Repository name
        skill_path: Path to skill directory
        branch: Branch name
        
    Returns:
        Dictionary with name and description, or empty dict on error
    """
    try:
        skill_md_path = f"{skill_path}/SKILL.md" if skill_path else "SKILL.md"
        raw_url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{skill_md_path}"
        
        req = urllib.request.Request(raw_url)
        req.add_header('User-Agent', 'cursor-skills-mcp')
        
        with urllib.request.urlopen(req, timeout=10) as response:
            content = response.read().decode('utf-8')
        
        return _extract_frontmatter(content)
    except Exception:
        return {}


def _download_github_directory(owner: str, repo: str, path: str, branch: str, dest: Path) -> tuple[bool, str]:
    """Download a directory from GitHub using the API.
    
    Args:
        owner: Repository owner
        repo: Repository name
        path: Path within repository
        branch: Branch name
        dest: Destination directory
        
    Returns:
        Tuple of (success, message)
    """
    try:
        api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}?ref={branch}"
        
        req = urllib.request.Request(api_url)
        req.add_header('Accept', 'application/vnd.github.v3+json')
        req.add_header('User-Agent', 'cursor-skills-mcp')
        
        with urllib.request.urlopen(req, timeout=30) as response:
            contents = json.loads(response.read().decode())
        
        if not isinstance(contents, list):
            return False, "Path does not point to a directory"
        
        # Create destination directory
        dest.mkdir(parents=True, exist_ok=True)
        
        # Download all files
        for item in contents:
            item_name = item['name']
            item_path = item['path']
            item_type = item['type']
            
            if item_type == 'file':
                download_url = item['download_url']
                file_dest = dest / item_name
                
                with urllib.request.urlopen(download_url, timeout=30) as response:
                    file_dest.write_bytes(response.read())
                    
            elif item_type == 'dir':
                subdir_dest = dest / item_name
                success, msg = _download_github_directory(owner, repo, item_path, branch, subdir_dest)
                if not success:
                    return False, msg
        
        return True, "Successfully downloaded"
        
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return False, f"Repository or path not found (404). Check the URL and branch name."
        return False, f"HTTP Error {e.code}: {e.reason}"
    except Exception as e:
        return False, f"Error downloading: {str(e)}"


def _browse_skills_impl(source_name: str = None) -> str:
    """Browse available skills from trusted sources.
    
    Args:
        source_name: Optional specific source to browse
        
    Returns:
        Formatted list of available skills with author attribution
    """
    sources = _load_skill_sources()
    
    if not sources:
        return "No skill sources configured. Create a skill_sources.yaml file with trusted repositories."
    
    if source_name and source_name not in sources:
        available = ', '.join(sources.keys())
        return f"Source '{source_name}' not found. Available sources: {available}"
    
    # Filter to specific source if requested
    sources_to_browse = {source_name: sources[source_name]} if source_name else sources
    
    results = []
    
    for name, config in sources_to_browse.items():
        url = config.get('url', '')
        author = config.get('author', 'unknown')
        description = config.get('description', '')
        path = config.get('path', '')
        
        parsed = _parse_github_url(url)
        if not parsed:
            results.append(f"\n## {name} (by {author})\n⚠️ Invalid URL configuration")
            continue
        
        owner = parsed['owner']
        repo = parsed['repo']
        branch = parsed['branch']
        skills_path = path or parsed['path']
        
        # Fetch directory contents
        contents = _fetch_github_directory_contents(owner, repo, skills_path, branch)
        
        if not contents:
            results.append(f"\n## {name} (by {author})\n⚠️ Could not fetch skills from {url}")
            continue
        
        # Find skill directories (those containing SKILL.md)
        skill_entries = []
        for item in contents:
            if item['type'] != 'dir' or item['name'].startswith('.'):
                continue
            
            skill_dir_path = f"{skills_path}/{item['name']}" if skills_path else item['name']
            frontmatter = _fetch_skill_frontmatter(owner, repo, skill_dir_path, branch)
            
            if frontmatter or True:  # Include even if no frontmatter found
                skill_desc = frontmatter.get('description', 'No description available')
                skill_entries.append(f"  - **{item['name']}**: {skill_desc}")
        
        if skill_entries:
            header = f"\n## {name} (by @{author})"
            if description:
                header += f"\n_{description}_"
            results.append(header + "\n" + "\n".join(skill_entries))
        else:
            results.append(f"\n## {name} (by @{author})\n_No skills found in this source_")
    
    if not results:
        return "No skills found in any configured sources."
    
    return "# Available Skills from Trusted Sources\n" + "\n".join(results)


def _import_skills_impl(skill_names: list, source_name: str = None) -> str:
    """Import specific skills from trusted sources.
    
    Args:
        skill_names: List of skill names to import
        source_name: Optional source to import from (searches all if not specified)
        
    Returns:
        Status message with results
    """
    sources = _load_skill_sources()
    
    if not sources:
        return "No skill sources configured. Create a skill_sources.yaml file with trusted repositories."
    
    if source_name and source_name not in sources:
        available = ', '.join(sources.keys())
        return f"Source '{source_name}' not found. Available sources: {available}"
    
    sources_to_search = {source_name: sources[source_name]} if source_name else sources
    skills_dir = project_root / "skills"
    skills_dir.mkdir(exist_ok=True)
    
    imported = []
    skipped = []
    not_found = []
    failed = []
    
    for skill_name in skill_names:
        # Check if already exists locally
        if (skills_dir / skill_name).exists():
            skipped.append(f"{skill_name} (already exists)")
            continue
        
        # Search for skill in sources
        found = False
        for src_name, config in sources_to_search.items():
            url = config.get('url', '')
            path = config.get('path', '')
            author = config.get('author', 'unknown')
            
            parsed = _parse_github_url(url)
            if not parsed:
                continue
            
            owner = parsed['owner']
            repo = parsed['repo']
            branch = parsed['branch']
            skills_path = path or parsed['path']
            
            # Try to download the skill
            skill_path = f"{skills_path}/{skill_name}" if skills_path else skill_name
            dest = skills_dir / skill_name
            
            success, message = _download_github_directory(owner, repo, skill_path, branch, dest)
            
            if success:
                # Verify it's actually a skill
                if (dest / "SKILL.md").exists():
                    imported.append(f"{skill_name} (from @{author})")
                    found = True
                    break
                else:
                    # Not a valid skill, remove it
                    shutil.rmtree(dest)
            elif dest.exists():
                shutil.rmtree(dest)
        
        if not found and skill_name not in [s.split(' ')[0] for s in skipped]:
            not_found.append(skill_name)
    
    # Build result message
    result_parts = []
    if imported:
        result_parts.append(f"✅ Imported {len(imported)} skill(s):\n   " + "\n   ".join(imported))
    if skipped:
        result_parts.append(f"⏭️ Skipped {len(skipped)} skill(s):\n   " + "\n   ".join(skipped))
    if not_found:
        result_parts.append(f"❌ Not found in any source:\n   " + "\n   ".join(not_found))
    if failed:
        result_parts.append(f"⚠️ Failed to import:\n   " + "\n   ".join(failed))
    
    return "\n\n".join(result_parts) if result_parts else "No skills were imported."


# =============================================================================
# MCP Tools
# =============================================================================

@mcp.tool()
def list_skills() -> str:
    """List all available skills in the local skills directory.
    
    Returns:
        str: Formatted list of available skills with descriptions in <skill> tags
    """
    return _list_skills_impl()


@mcp.tool()
def invoke_skill(skill_name: str) -> str:
    """Invoke a skill to access its specialized instructions and capabilities.

    Args:
        skill_name: The name of the skill to invoke (e.g., "pdf", "artifacts-builder")
        
    Returns:
        str: Complete skill documentation with specialized instructions
    """
    return _invoke_skill_impl(skill_name)


@mcp.tool()
def list_skill_sources() -> str:
    """List configured trusted skill sources.
    
    Returns:
        str: Formatted list of trusted sources with URLs and descriptions
    """
    sources = _load_skill_sources()
    
    if not sources:
        return "No skill sources configured. Create a skill_sources.yaml file with trusted repositories."
    
    result = ["# Trusted Skill Sources\n"]
    for name, config in sources.items():
        author = config.get('author', 'unknown')
        url = config.get('url', 'No URL')
        description = config.get('description', 'No description')
        result.append(f"## {name} (by @{author})")
        result.append(f"_{description}_")
        result.append(f"URL: {url}\n")
    
    return "\n".join(result)


@mcp.tool()
def browse_skills(source_name: str = None) -> str:
    """Browse available skills from trusted sources without importing them.
    Shows skill names, descriptions, and which author/source they come from.
    
    Args:
        source_name: Optional - browse only this source. If not provided, browses all sources.
        
    Returns:
        str: Formatted list of available skills organized by source with author attribution
    """
    return _browse_skills_impl(source_name)


@mcp.tool()
def import_skills(skill_names: list, source_name: str = None) -> str:
    """Import specific skills from trusted sources into the local skills directory.
    
    Args:
        skill_names: List of skill names to import (e.g., ["design-principles", "skill-creator"])
        source_name: Optional - import only from this source. If not provided, searches all sources.
        
    Returns:
        str: Status message showing imported, skipped, and failed skills
    """
    return _import_skills_impl(skill_names, source_name)


@mcp.tool()
def import_skill(github_url: str) -> str:
    """Import a skill directly from any GitHub repository URL.
    For trusted sources, prefer using import_skills() instead.
    
    Args:
        github_url: GitHub URL to a skill directory or repository.
    
    Returns:
        str: Success message with imported skill name and location, or error details
    """
    # Parse GitHub URL
    parsed = _parse_github_url(github_url)
    if not parsed:
        return f"Invalid GitHub URL format. Expected: https://github.com/owner/repo or https://github.com/owner/repo/tree/branch/path"
    
    owner = parsed['owner']
    repo = parsed['repo']
    branch = parsed['branch']
    path = parsed['path']
    
    # Determine skill name from the last part of the path or repo name
    if path:
        dir_name = path.split('/')[-1]
    else:
        dir_name = repo
    
    skills_dir = project_root / "skills"
    skills_dir.mkdir(exist_ok=True)
    temp_path = skills_dir / f"_temp_{dir_name}"
    
    # Download the directory
    success, message = _download_github_directory(owner, repo, path, branch, temp_path)
    
    if not success:
        if temp_path.exists():
            shutil.rmtree(temp_path)
        return f"Failed to import skill: {message}"
    
    # Check if this is a single skill or contains multiple skills
    is_single_skill = (temp_path / "SKILL.md").exists()
    
    if is_single_skill:
        final_path = skills_dir / dir_name
        
        if final_path.exists():
            shutil.rmtree(temp_path)
            return f"Skill '{dir_name}' already exists at {final_path}. Remove it first if you want to re-import."
        
        temp_path.rename(final_path)
        return f"✅ Successfully imported skill '{dir_name}' from @{owner}"
    
    # Check for multiple skills
    contained_skills = []
    for item in temp_path.iterdir():
        if item.is_dir() and not item.name.startswith('.') and (item / "SKILL.md").exists():
            contained_skills.append(item.name)
    
    if contained_skills:
        imported = []
        skipped = []
        
        for skill_name in contained_skills:
            source = temp_path / skill_name
            dest = skills_dir / skill_name
            
            if dest.exists():
                skipped.append(skill_name)
                continue
            
            try:
                shutil.move(str(source), str(dest))
                imported.append(skill_name)
            except Exception as e:
                pass
        
        shutil.rmtree(temp_path)
        
        result_parts = []
        if imported:
            result_parts.append(f"✅ Imported {len(imported)} skill(s) from @{owner}: {', '.join(imported)}")
        if skipped:
            result_parts.append(f"⏭️ Skipped {len(skipped)} existing skill(s): {', '.join(skipped)}")
        
        return "\n".join(result_parts) if result_parts else "No skills were imported."
    
    shutil.rmtree(temp_path)
    return f"Downloaded directory does not contain SKILL.md and has no skill subdirectories."


@mcp.tool()
def find_skill() -> str:
    """Find available skills from the community skill directory.
    
    Returns:
        str: Content of the skills directory README with descriptions and URLs
    """
    try:
        url = "https://raw.githubusercontent.com/chrisboden/find-skills/main/README.md"
        
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'cursor-skills-mcp')
        with urllib.request.urlopen(req, timeout=10) as response:
            content = response.read().decode('utf-8')
        
        return content
        
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return "Error: Skills directory README not found (404)."
        return f"HTTP Error {e.code}: {e.reason}"
    except Exception as e:
        return f"Error fetching skills directory: {str(e)}"


if __name__ == "__main__":
    mcp.run()
