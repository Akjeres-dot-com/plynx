class JobReturnStatus(object):
    SUCCESS = 'SUCCESS'
    FAILED = 'FAILED'


class NodeRunningStatus(object):
    STATIC = 'STATIC'
    CREATED = 'CREATED'
    IN_QUEUE = 'IN_QUEUE'
    RUNNING = 'RUNNING'
    SUCCESS = 'SUCCESS'
    RESTORED = 'RESTORED'
    FAILED = 'FAILED'


class NodeStatus(object):
    CREATED = 'CREATED'
    READY = 'READY'
    DEPRECATED = 'DEPRECATED'
    MANDATORY_DEPRECATED = 'MANDATORY_DEPRECATED'


class NodePostAction:
    SAVE = 'SAVE'
    APPROVE = 'APPROVE'
    VALIDATE = 'VALIDATE'
    DEPRECATE = 'DEPRECATE'


class NodePostStatus(object):
    SUCCESS = 'SUCCESS'
    FAILED = 'FAILED'
    VALIDATION_FAILED = 'VALIDATION_FAILED'
