from typing import List

def as_dto_factory_fn(slot_type):
    return lambda slot: as_dto(slot, slot_type)
    
def as_dto(slot, slot_type):
    slot_mask = { "slotNo": None }
    slot = deep_mask(slot, slot_mask)

    slot["type"] = slot_type

    return slot

def create_schedule(blocked_slots: List[dict], bookings: List[dict], as_dto_factory_fn_arg=None) -> List[dict]:
    if not as_dto_factory_fn_arg:
        as_dto_factory_fn_arg = as_dto_factory_fn
    
    key_fn = lambda slot: slot["slotNo"]
    
    blocked_slots.sort(key=key_fn)
    bookings.sort(key=key_fn)

    blocked_slots = list(map(as_dto_factory_fn_arg("blocked_slot"), blocked_slots))
    bookings = list(map(as_dto_factory_fn_arg("booking"), bookings))

    return merge(blocked_slots, bookings, key_fn)
    
def create_full_schedule(blocked_slots: List[dict], bookings: List[dict]) -> List[dict]:
    return create_schedule(blocked_slots, bookings, lambda x: (lambda y: y))

def deep_mask(dic, mask_dic: dict):
    
    if not isinstance(dic, dict):
        return dic
    
    out_dic = dict()
    
    for key in mask_dic:
        item = dic[key]
        out_dic[key] = deep_mask(item, mask_dic[key])

    return out_dic


def merge(left, right, key=lambda x: x):
    left_ptr = right_ptr = 0

    merged = []
    
    while left_ptr < len(left) and right_ptr < len(right):
        left_val, right_val = left[left_ptr], right[right_ptr]
        left_cmp, right_cmp = key(left_val), key(right_val)

        if left_cmp < right_cmp:
            merged.append(left_val)
            left_ptr += 1
        else:
            merged.append(right_val)
            right_ptr += 1
    
    # Returns empty slice if out of index
    merged += left[left_ptr: ]
    merged += right[right_ptr: ]
    
    return merged

