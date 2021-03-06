import json
from graphenebase.types import *
from graphenebase.objects import GrapheneObject, isArgsThisClass

#: Operation ids
operations = {}
operations["vote"] = 0
operations["comment"] = 1
operations["transfer"] = 2
operations["transfer_to_vesting"] = 3
operations["withdraw_vesting"] = 4
operations["limit_order_create"] = 5
operations["limit_order_cancel"] = 6
operations["feed_publish"] = 7
operations["convert"] = 8
operations["account_create"] = 9
operations["account_update"] = 10
operations["witness_update"] = 11
operations["account_witness_vote"] = 12
operations["account_witness_proxy"] = 13
operations["pow"] = 14
operations["custom"] = 15
operations["report_over_production"] = 16
operations["fill_convert_request"] = 17
operations["comment_reward"] = 18
operations["curate_reward"] = 19
operations["liquidity_reward"] = 20
operations["interest"] = 21
operations["fill_vesting_withdraw"] = 22
operations["fill_order"] = 23


def getOperationNameForId(i) :
    """ Convert an operation id into the corresponding string
    """
    for key in operations :
        if int(operations[key]) is int(i) :
            return key
    return "Unknown Operation ID %d" % i


class Operation() :
    def __init__(self, op) :
        if isinstance(op, list) and len(op) == 2:
            self.opId = operations[op[0]]
            name = op[0]
            self.name = name[0].upper() + name[1:]
            try:
                klass = eval(self.name)
            except:
                raise NotImplementedError("Unimplemented Operation %s" % self.name)
            self.op = klass(op[1])
        else:
            self.op = op
            self.name = type(self.op).__name__.lower()  # also store name
            print(self.name)
            self.opId = operations[self.name]

    def __bytes__(self) :
        return bytes(Id(self.opId)) + bytes(self.op)

    def __str__(self) :
        return json.dumps([getOperationNameForId(self.opId), JsonObj(self.op)])

"""
    Actual Operations
"""


class Vote(GrapheneObject) :
    def __init__(self, *args, **kwargs) :
        if isArgsThisClass(self, args):
                self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(OrderedDict([
                ('voter'    , String(kwargs["voter"])),
                ('author'   , String(kwargs["author"])),
                ('permlink' , String(kwargs["permlink"])),
                ('weight'   , Int16(kwargs["weight"])),
            ]))


class Comment(GrapheneObject) :
    def __init__(self, *args, **kwargs) :
        if isArgsThisClass(self, args):
                self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(OrderedDict([
                ('parent_author'   , String(kwargs["parent_author"])),
                ('parent_permlink' , String(kwargs["parent_permlink"])),
                ('author'          , String(kwargs["author"])),
                ('permlink'        , String(kwargs["permlink"])),
                ('title'           , String(kwargs["title"])),
                ('body'            , String(kwargs["body"])),
                ('json_metadata'   , String(kwargs["json_metadata"])),
            ]))
