



def runPipeline( pipeline, records):
    # load dependency pipelines, recursively
    depends = buildDependsOrder(pipeline, repo)
    for level in depends:
        for upstream in level: # could/should be randomly ordered
            upstream.process( records, repo)

    # the depends order does NOT include the original pipeline
    pipeline.process(records, repo)

    
def buildDependsOrder( pipeline, repo, partialOrder=[], level=0):
    if len(partialOrder) < (level + 1):
        partialOrder.append(set())

    for dependsName, endpts in pipeline.depends():
        if not dependsName:
            continue
        depends = mu.loadPipeline(dependsName, endpts, repo=repo)
        partialOrder[level].add(depends)
        buildDependsGraph( depends, repo, partialOrder=partialOrder, level=level+1)

    # if a recursion depth error occurs then we have a dependency cycle
    # otherwise we need to do some processing to clean up the final
    # result
    if level != 0:
        return

    partialOrder = partialOrder[::-1]
    cleaned = []
    addedPipelines = {}
    for i, order in enumerate(partialOrder):
        for upstream in order:
            if upstream.name() in addedPipelines:
                addedPipelines[ upstream.name()].addEndPoints( upstream.requestedEndPoints())
                continue
            if (i+1) > len(cleaned):
                cleaned.append([])
            cleaned[-1].append(upstream)
            addedPipelines[ upstream.name()] = upstream
    return cleaned

    
    
