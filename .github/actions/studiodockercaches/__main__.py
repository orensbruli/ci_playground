import argparse
import json
import re
import sys

# https://docs.docker.com/engine/reference/commandline/tag/#description
# String that not start with a period or a hyphen, and can contain any combination of
# lowercase and uppercase letters, digits, underscores, periods and dashes.
docker_tag_regex = r"(?![.-])[a-zA-Z0-9_.-]{1,128}"


def validate_docker_tag(tag):
    """
    Validate docker image URI tag
    """
    tag = re.search(docker_tag_regex, tag)
    if tag is not None and tag.group() == tag.string:
        return True
    else:
        return False


def fix_docker_tag(tag, replacement="_"):
    """
    Fix docker image URI tag if it contains invalid characters.
    Replace invalid characters with "_" by default
    """
    pattern = r"[^a-zA-Z0-9._-]"
    return re.sub(pattern, replacement, tag)

def fix_docker_uri(image_uri):
    """
    Fix docker image URI tag if it contains invalid characters
    """
    if ":" in image_uri:
        image_name, tag = image_uri.split(":")
        if not validate_docker_tag(tag):
            print(f"Detected invalid tag: {tag}. Fixed.", file=sys.stderr)
            tag = fix_docker_tag(tag)
    else:
        tag = "latest"
    return f"{image_name}:{tag}"


if __name__ == "__main__":
    """
    Create a json with the cache-from and cache-to options for docker buildx
    
    Usage:
        python3 <this_file>.py parent_branch current_branch image_name registry1 registry2 registry3
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("parent")
    parser.add_argument("current")
    parser.add_argument("image")
    parser.add_argument("regs", nargs="+")
    args = parser.parse_args()

    caches = ("main", args.parent, args.current)
    result = {'cache-from':[], "cache-to":[]}
    for registry in args.regs:
        for cache in caches:
            ref = fix_docker_uri(f"{registry}/{args.image}:{cache}-buildcache")
            result["cache-from"].append(f"type=registry,ref={ref}")
            if cache == args.current:
                result["cache-to"].append(f"type=registry,ref={ref}")
    result["cache-from"] = "\n".join(set(result["cache-from"]))
    result["cache-to"] = "\n".join(set(result["cache-to"]))
    print(json.dumps(result))
