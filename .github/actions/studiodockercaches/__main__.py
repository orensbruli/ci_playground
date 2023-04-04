import sys
import json

if __name__ == "__main__":
    parent = argv[1]
    current = arg[2]
    image = argv[3]
    regs=( 'DOCKERUSER', "ghcr.io/GITHUBORG" )
    caches=( "main", parent, current )
    result = []
    for registry in regs:
        for cache in caches:
            result.append(f"type=registry,ref={registry}/{image}:{cache}-buildcache")
    json.dumps(result)

