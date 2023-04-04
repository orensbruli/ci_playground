import sys
import json

if __name__ == "__main__":
    parent = sys.argv[1]
    current = sys.argv[2]
    image = sys.argv[3]
    regs=( 'DOCKERUSER', "ghcr.io/GITHUBORG" )
    caches=( "main", parent, current )
    result = []
    for registry in regs:
        for cache in caches:
            result.append(f"type=registry,ref={registry}/{image}:{cache}-buildcache")
    json.dumps(result)

