import sys
import json

if __name__ == "__main__":
    parent = sys.argv[1]
    current = sys.argv[2]
    image = sys.argv[3]
    regs=sys.argv[4].split(',')
    caches=( "main", parent, current )
    result = []
    for registry in regs:
        for cache in caches:
            print(f"type=registry,ref={registry}/{image}:{cache}-buildcache")
    

