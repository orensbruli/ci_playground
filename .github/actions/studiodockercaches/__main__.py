import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("parent")
    parser.add_argument("current")
    parser.add_argument("image")
    parser.add_argument("regs", nargs="+")
    args = parser.parse_args()

    caches = ("main", arg.parent, arg.current)
    result = {'cache-from':[], "cache-to":[]}
    for registry in args.regs:
        for cache in caches:
            result["cache-from"].append(f"type=registry,ref={registry}/{args.image}:{cache}-buildcache")
            if cache == arg.current:
                result["cache-to"].append(f"type=registry,ref={registry}/{args.image}:{cache}-buildcache")
    result["cache-from"] = "\n".join(result["cache-from"])
    result["cache-to"] = "\n".join(result["cache-to"])
